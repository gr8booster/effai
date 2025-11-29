"""OrchestratorAI - Central coordinator and validation gatekeeper"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import uuid
import logging
from datetime import datetime, timezone

from schemas import (
    OrchestratorRunInput,
    OrchestratorRunOutput,
    AgentStepResult,
    TaskStatus
)
from database import get_mongo_db, get_redis

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/orchestrator", tags=["orchestrator"])


@router.post("/run", response_model=OrchestratorRunOutput)
async def run_orchestration(input_data: OrchestratorRunInput):
    """
    Main orchestration endpoint - routes requests through validation pipeline
    
    Flow:
    1. Parse action into steps
    2. Execute each step in sequence
    3. Pass outputs through LegalAI and CFP-AI validation gates
    4. Log provenance via AuditAgent
    5. Return final result
    """
    try:
        db = get_mongo_db()
        redis = get_redis()
        
        # Store run in MongoDB
        run_doc = {
            "run_id": input_data.run_id,
            "user_id": input_data.user_id,
            "action": input_data.action,
            "payload": input_data.payload,
            "trace_id": input_data.trace_id,
            "status": TaskStatus.QUEUED.value,
            "steps": [],
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        }
        
        await db.orchestrator_runs.insert_one(run_doc)
        
        # Cache in Redis for quick access
        await redis.set(f"run:{input_data.run_id}:status", TaskStatus.RUNNING.value, ex=3600)
        
        # Parse action pipeline
        steps = parse_action_pipeline(input_data.action)
        
        result = OrchestratorRunOutput(
            run_id=input_data.run_id,
            status=TaskStatus.QUEUED,
            steps=[],
            provenance_ref=f"prov_{input_data.run_id}"
        )
        
        # Execute pipeline
        for step in steps:
            step_result = await execute_step(step, input_data.payload, input_data.user_id)
            result.steps.append(step_result)
            
            if step_result.status == "failed":
                result.status = TaskStatus.FAILED
                break
        
        if result.status != TaskStatus.FAILED:
            result.status = TaskStatus.COMPLETED
        
        # Update in DB
        await db.orchestrator_runs.update_one(
            {"run_id": input_data.run_id},
            {"$set": {
                "status": result.status.value,
                "steps": [s.model_dump() for s in result.steps],
                "updated_at": datetime.now(timezone.utc).isoformat()
            }}
        )
        
        await redis.set(f"run:{input_data.run_id}:status", result.status.value, ex=3600)
        
        logger.info(f"Orchestration {input_data.run_id} completed with status {result.status}")
        
        return result
        
    except Exception as e:
        logger.error(f"Orchestration failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status/{run_id}")
async def get_run_status(run_id: str):
    """Get orchestration run status"""
    try:
        redis = get_redis()
        status = await redis.get(f"run:{run_id}:status")
        
        if not status:
            db = get_mongo_db()
            run_doc = await db.orchestrator_runs.find_one({"run_id": run_id}, {"_id": 0})
            
            if not run_doc:
                raise HTTPException(status_code=404, detail="Run not found")
            
            return run_doc
        
        return {"run_id": run_id, "status": status}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def parse_action_pipeline(action: str) -> list:
    """
    Parse action string into execution steps
    
    Example: "intake->diagnose->defend" -> ["intake", "diagnose", "defend"]
    """
    return [step.strip() for step in action.split("->")]


async def execute_step(step: str, payload: Dict[str, Any], user_id: str) -> AgentStepResult:
    """
    Execute a single pipeline step
    
    This is a stub for POC - will route to actual agent endpoints
    """
    logger.info(f"Executing step: {step}")
    
    # Stub implementation - will be expanded in full build
    if step == "intake":
        return AgentStepResult(agent="IntakeAgent", status="ok", output_ref="intake_output")
    elif step == "diagnose":
        return AgentStepResult(agent="EEFai", status="ok", output_ref="diagnosis_output")
    elif step == "defend":
        return AgentStepResult(agent="WriterAgent", status="ok", output_ref="letter_output")
    else:
        return AgentStepResult(agent="Unknown", status="ok", output_ref=f"{step}_output")
