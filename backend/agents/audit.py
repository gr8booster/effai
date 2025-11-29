"""AuditAgent - Provenance recorder and immutable log manager"""
from fastapi import APIRouter, HTTPException
import logging
import hashlib
import hmac
import os
import json

from schemas import (
    AuditLogInput,
    AuditLogOutput,
    AuditVerifyInput,
    AuditVerifyOutput
)
from database import get_pg_pool, get_mongo_db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/audit", tags=["audit"])

# HMAC key for signing provenance (in production, use KMS)
HMAC_KEY = os.environ.get('EMERGENT_LLM_KEY', 'default-hmac-key').encode()


@router.post("/log", response_model=AuditLogOutput)
async def log_provenance(input_data: AuditLogInput):
    """
    Create immutable provenance record
    
    All agent actions must log provenance before user-facing output
    """
    try:
        # Generate HMAC signature
        signature_data = f"{input_data.provenance_id}:{input_data.input_hash}:{input_data.output_hash}:{input_data.timestamp.isoformat()}"
        hmac_signature = hmac.new(
            HMAC_KEY,
            signature_data.encode(),
            hashlib.sha256
        ).hexdigest()
        
        # Convert timestamp to UTC if needed
        if input_data.timestamp.tzinfo is None:
            # Naive datetime, assume UTC
            timestamp_utc = input_data.timestamp.replace(tzinfo=timezone.utc)
        else:
            timestamp_utc = input_data.timestamp
        
        # Store in PostgreSQL (immutable)
        pool = get_pg_pool()
        async with pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO audit_log (
                    provenance_id, agent_id, agent_version,
                    input_hash, output_hash, s3_input_path, s3_output_path,
                    db_refs, legal_db_version, cfp_version,
                    timestamp, human_reviewed, hmac_signature
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8::jsonb, $9, $10, $11, $12, $13)
            """,
                input_data.provenance_id,
                input_data.agent_id,
                input_data.agent_version,
                input_data.input_hash,
                input_data.output_hash,
                input_data.s3_input_path,
                input_data.s3_output_path,
                json.dumps(input_data.db_refs) if input_data.db_refs else None,
                input_data.legal_db_version,
                input_data.cfp_version,
                timestamp_utc,
                input_data.human_reviewed,
                hmac_signature
            )
        
        # Also store in MongoDB for quick access
        db = get_mongo_db()
        await db.audit_log.insert_one({
            "provenance_id": input_data.provenance_id,
            "agent_id": input_data.agent_id,
            "timestamp": timestamp_utc.isoformat(),
            "hmac_signature": hmac_signature
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
