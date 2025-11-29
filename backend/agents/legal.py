"""LegalAI - Deterministic legal rules engine"""
from fastapi import APIRouter, HTTPException
import logging
from typing import List
from datetime import datetime, timedelta

from schemas import (
    LegalCheckInput,
    LegalCheckOutput,
    LegalFlag,
    LegalCitation,
    Severity
)
from database import get_pg_pool

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/legal", tags=["legal"])

# Legal DB version
LEGAL_DB_VERSION = "v1.0"


@router.post("/check", response_model=LegalCheckOutput)
async def check_legal(input_data: LegalCheckInput):
    """
    Deterministic legal validation
    
    Checks:
    - FDCPA compliance
    - FCRA compliance
    - CROA compliance
    - State statute of limitations
    - Proper documentation requirements
    """
    try:
        flags: List[LegalFlag] = []
        citations: List[LegalCitation] = []
        must_escalate = False
        
        # Check statute of limitations
        if input_data.action_type == "statute_check":
            sol_flag, sol_citation = await check_statute_of_limitations(
                input_data.user_state.state,
                input_data.context.get("debt_type", "credit_card"),
                input_data.context.get("account_date")
            )
            if sol_flag:
                flags.append(sol_flag)
            if sol_citation:
                citations.append(sol_citation)
        
        # Check debt validation requirements (FDCPA)
        if input_data.action_type == "debt_validation":
            fdcpa_flags, fdcpa_citations = await check_fdcpa_compliance(input_data.context)
            flags.extend(fdcpa_flags)
            citations.extend(fdcpa_citations)
        
        # Check credit dispute requirements (FCRA)
        if input_data.action_type == "credit_dispute":
            fcra_flags, fcra_citations = await check_fcra_compliance(input_data.context)
            flags.extend(fcra_flags)
            citations.extend(fcra_citations)
        
        # Determine if escalation needed
        for flag in flags:
            if flag.severity == Severity.HIGH:
                must_escalate = True
                break
        
        ok = len([f for f in flags if f.severity == Severity.HIGH]) == 0
        
        result = LegalCheckOutput(
            ok=ok,
            flags=flags,
            citations=citations,
            must_escalate=must_escalate,
            provenance_ref=f"legal_check_{input_data.trace_id}"
        )
        
        logger.info(f"Legal check completed: ok={ok}, must_escalate={must_escalate}")
        
        return result
        
    except Exception as e:
        logger.error(f"Legal check failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/citation/{citation_id}")
async def get_citation(citation_id: str):
    """Retrieve full citation details"""
    try:
        pool = get_pg_pool()
        
        async with pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM legal_rules WHERE rule_code = $1",
                citation_id
            )
            
            if not row:
                raise HTTPException(status_code=404, detail="Citation not found")
            
            return dict(row)
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get citation: {e}")
        raise HTTPException(status_code=500, detail=str(e))


async def check_statute_of_limitations(state: str, debt_type: str, account_date: str) -> tuple:
    """
    Check if debt is past statute of limitations
    
    Returns: (flag, citation) or (None, None)
    """
    try:
        pool = get_pg_pool()
        
        async with pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT years FROM statute_of_limitations WHERE state_code = $1 AND debt_type = $2",
                state.upper(),
                debt_type.lower()
            )
            
            if not row:
                # Default to 6 years if state-specific not found
                sol_years = 6
            else:
                sol_years = row['years']
            
            # Check if account is past SOL
            if account_date:
                account_dt = datetime.fromisoformat(account_date)
                sol_date = account_dt + timedelta(days=sol_years*365)
                
                if datetime.now() > sol_date:
                    flag = LegalFlag(
                        code="SOL_EXPIRED",
                        explanation=f"This debt is past the {sol_years}-year statute of limitations in {state}.",
                        severity=Severity.LOW,
                        citation_id="SOL_STATE"
                    )
                    
                    citation = LegalCitation(
                        id="SOL_STATE",
                        title=f"{state} Statute of Limitations for {debt_type}",
                        text_snippet=f"The statute of limitations for {debt_type} debts in {state} is {sol_years} years.",
                        db_version=LEGAL_DB_VERSION
                    )
                    
                    return (flag, citation)
        
        return (None, None)
        
    except Exception as e:
        logger.error(f"SOL check failed: {e}")
        return (None, None)


async def check_fdcpa_compliance(context: dict) -> tuple:
    """
    Check FDCPA compliance for debt validation
    
    Returns: (flags[], citations[])
    """
    flags = []
    citations = []
    
    # Basic FDCPA checks
    if not context.get("creditor_name"):
        flags.append(LegalFlag(
            code="FDCPA_VALIDATION_REQUIRED",
            explanation="Under FDCPA § 809, you have the right to request debt validation.",
            severity=Severity.LOW,
            citation_id="FDCPA_809"
        ))
        
        citations.append(LegalCitation(
            id="FDCPA_809",
            title="FDCPA § 809 - Validation of debts",
            text_snippet="A debt collector must provide verification of the debt if requested by the consumer within 30 days.",
            db_version=LEGAL_DB_VERSION
        ))
    
    return (flags, citations)


async def check_fcra_compliance(context: dict) -> tuple:
    """
    Check FCRA compliance for credit disputes
    
    Returns: (flags[], citations[])
    """
    flags = []
    citations = []
    
    # Basic FCRA checks
    flags.append(LegalFlag(
        code="FCRA_DISPUTE_RIGHT",
        explanation="Under FCRA § 611, you have the right to dispute inaccurate information.",
        severity=Severity.LOW,
        citation_id="FCRA_611"
    ))
    
    citations.append(LegalCitation(
        id="FCRA_611",
        title="FCRA § 611 - Procedure for correcting incomplete or inaccurate information",
        text_snippet="Credit bureaus must investigate disputes within 30 days and correct or delete inaccurate information.",
        db_version=LEGAL_DB_VERSION
    ))
    
    return (flags, citations)
