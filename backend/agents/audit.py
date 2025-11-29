"""AuditAgent - Provenance recorder using MongoDB"""
from fastapi import APIRouter, HTTPException
import logging
import os
import json
from datetime import datetime, timezone

from schemas import (
    AuditLogInput,
    AuditLogOutput,
    AuditVerifyInput,
    AuditVerifyOutput
)
from database import get_mongo_db
from canonical_json import hmac_sign, canonical_json

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/audit", tags=["audit"])

# HMAC key for signing provenance
HMAC_KEY = os.environ.get('EMERGENT_LLM_KEY', 'default-hmac-key').encode()


@router.post("/log", response_model=AuditLogOutput)
async def log_provenance(input_data: AuditLogInput):
    """Create immutable provenance record in MongoDB"""
    try:
        # Ensure timestamp is UTC
        if input_data.timestamp.tzinfo is None:
            timestamp_utc = input_data.timestamp.replace(tzinfo=timezone.utc)
        else:
            timestamp_utc = input_data.timestamp.astimezone(timezone.utc)
        
        # Generate HMAC signature
        signature_data = canonical_json({
            "provenance_id": input_data.provenance_id,
            "input_hash": input_data.input_hash,
            "output_hash": input_data.output_hash,
            "timestamp_utc": timestamp_utc.isoformat()
        })
        hmac_signature = hmac_sign(HMAC_KEY, signature_data)
        
        # Store in MongoDB (single source of truth)
        db = get_mongo_db()
        await db.audit_log.insert_one({
            "provenance_id": input_data.provenance_id,
            "agent_id": input_data.agent_id,
            "agent_version": input_data.agent_version,
            "input_hash": input_data.input_hash,
            "output_hash": input_data.output_hash,
            "s3_input_path": input_data.s3_input_path,
            "s3_output_path": input_data.s3_output_path,
            "db_refs": input_data.db_refs,
            "legal_db_version": input_data.legal_db_version,
            "cfp_version": input_data.cfp_version,
            "timestamp_utc": timestamp_utc.isoformat(),
            "display_ts": timestamp_utc.isoformat(),
            "human_reviewed": input_data.human_reviewed,
            "hmac_signature": hmac_signature,
            "created_at": datetime.now(timezone.utc).isoformat()
        })
        
        result = AuditLogOutput(
            ok=True,
            provenance_id=input_data.provenance_id,
            hmac_signature=hmac_signature
        )
        
        logger.info(f"Provenance logged: {input_data.provenance_id}")
        
        return result
        
    except Exception as e:
        logger.error(f"Provenance logging failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{provenance_id}")
async def get_provenance(provenance_id: str):
    """
    Retrieve full provenance record
    """
    try:
        pool = get_pg_pool()
        async with pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM audit_log WHERE provenance_id = $1",
                provenance_id
            )
            
            if not row:
                raise HTTPException(status_code=404, detail="Provenance record not found")
            
            return dict(row)
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get provenance: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/verify", response_model=AuditVerifyOutput)
async def verify_provenance(input_data: AuditVerifyInput):
    """
    Verify that output matches stored provenance hash
    
    Detects tampering or unauthorized modifications
    """
    try:
        pool = get_pg_pool()
        
        # Get stored provenance
        async with pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT output_hash, hmac_signature FROM audit_log WHERE provenance_id = $1",
                input_data.provenance_id
            )
            
            if not row:
                return AuditVerifyOutput(
                    ok=True,
                    verified=False,
                    message="Provenance record not found"
                )
            
            stored_hash = row['output_hash']
            
            # Compare hashes
            verified = stored_hash == input_data.output_hash
            
            if verified:
                message = "Output verified - hash matches provenance record"
            else:
                message = f"VERIFICATION FAILED - Hash mismatch. Expected: {stored_hash}, Got: {input_data.output_hash}"
            
            result = AuditVerifyOutput(
                ok=True,
                verified=verified,
                message=message
            )
            
            logger.info(f"Provenance verification: {message}")
            
            return result
            
    except Exception as e:
        logger.error(f"Verification failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/recent/{limit}")
async def get_recent_provenance(limit: int = 10):
    """
    Get recent provenance records
    """
    try:
        if limit > 100:
            limit = 100
        
        pool = get_pg_pool()
        async with pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT * FROM audit_log ORDER BY created_at DESC LIMIT $1",
                limit
            )
            
            return [dict(row) for row in rows]
            
    except Exception as e:
        logger.error(f"Failed to get recent provenance: {e}")
        raise HTTPException(status_code=500, detail=str(e))
