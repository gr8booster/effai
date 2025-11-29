"""EEFai - Personal financial advisor agent (per-user instance)"""
from fastapi import APIRouter, HTTPException
import logging
import uuid
from datetime import datetime, timezone

from schemas import (
    EEFaiMessageInput,
    EEFaiMessageOutput,
    EEFaiAction
)
from database import get_mongo_db
from ai_utils import extract_intent

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/eefai", tags=["eefai"])


@router.post("/create")
async def create_eefai_instance(user_id: str = None, profile: dict = None):
    """
    Create persistent EEFai instance for user with optional profile data
    
    Accepts either query param user_id OR JSON body with user_id and profile
    """
    try:
        from fastapi import Body
        
        # Handle both old and new API formats
        if user_id is None:
            # New format: JSON body
            request_data = profile or {}
            user_id = request_data.get('user_id')
            profile_data = request_data.get('profile', {})
        else:
            # Old format: query param
            profile_data = profile or {}
        
        if not user_id:
            raise HTTPException(status_code=400, detail="user_id required")
        
        db = get_mongo_db()
        
        # Check if instance already exists
        existing = await db.eefai_state.find_one({"user_id": user_id})
        if existing:
            # Update profile if new data provided
            if profile_data:
                await db.eefai_state.update_one(
                    {"user_id": user_id},
                    {"$set": {"profile": profile_data}}
                )
                return {"message": "EEFai instance updated", "user_id": user_id}
            return {"message": "EEFai instance already exists", "user_id": user_id}
        
        # Create new instance with profile
        instance = {
            "user_id": user_id,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "conversation_history": [],
            "current_plan_id": None,
            "stage": "stabilize",
            "profile": profile_data or {
                "income": 0,
                "expenses": 0,
                "debts": [],
                "goals": []
            },
            "context_refs": {
                "short_term_memory": [],
                "long_term_memory": []
            }
        }
        
        await db.eefai_state.insert_one(instance)
        
        logger.info(f"EEFai instance created for {user_id} with profile: {profile_data}")
        
        return {"message": "EEFai instance created", "user_id": user_id, "profile": profile_data}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to create EEFai instance: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{user_id}/state")
async def get_eefai_state(user_id: str):
    """Get EEFai state for user"""
    try:
        db = get_mongo_db()
        state = await db.eefai_state.find_one({"user_id": user_id}, {"_id": 0})
        
        if not state:
            raise HTTPException(status_code=404, detail="EEFai instance not found")
        
        return state
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get EEFai state: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{user_id}/message", response_model=EEFaiMessageOutput)
async def send_message_to_eefai(user_id: str, input_data: EEFaiMessageInput):
    """
    Send message to EEFai and get response
    
    EEFai routes requests through OrchestratorAI for validation
    """
    try:
        db = get_mongo_db()
        
        # Get EEFai state
        state = await db.eefai_state.find_one({"user_id": user_id})
        if not state:
            # Auto-create if not exists
            await create_eefai_instance(user_id)
            state = await db.eefai_state.find_one({"user_id": user_id})
        
        # Extract intent from message
        available_actions = [
            "upload_debt_letter",
            "create_savings_plan",
            "dispute_credit_item",
            "general_question",
            "check_status"
        ]
        
        intent = await extract_intent(input_data.message, available_actions)
        
        # Generate response based on intent
        response_id = str(uuid.uuid4())
        actions = []
        
        if intent == "upload_debt_letter":
            response_text = """I can help you respond to that debt collection letter. 
            
Under the Fair Debt Collection Practices Act, you have important rights. Let me help you:
            1. Verify this debt is legitimate
            2. Check if it's past the statute of limitations
            3. Draft a proper validation request
            
            Please upload the letter so I can analyze it."""
            actions.append(EEFaiAction(type="task", ref="upload_document"))
        
        elif intent == "create_savings_plan":
            response_text = """Let's build your emergency fund together!
            
            I'll need to understand your situation:
            - What's your monthly income?
            - What are your regular expenses?
            - How much do you want to save?
            - When do you need it by?
            
            Once I have this info, I'll create a realistic plan with small, daily actions."""
            actions.append(EEFaiAction(type="plan", ref="emergency_savings_setup"))
        
        elif intent == "dispute_credit_item":
            response_text = """I can help you dispute inaccurate items on your credit report.
            
            Under the Fair Credit Reporting Act, you have the right to dispute any inaccurate information. 
            I'll help you:
            1. Identify what needs to be disputed
            2. Gather supporting evidence
            3. Draft proper dispute letters to all three bureaus
            
            What item do you want to dispute?"""
            actions.append(EEFaiAction(type="task", ref="credit_dispute_setup"))
        
        else:
            response_text = """I'm here to help you with:
            - Emergency expenses and debt collection issues
            - Building your emergency savings fund
            - Improving your credit score
            - Creating a realistic financial plan
            
            What would you like to work on today?"""
        
        # Update conversation history
        conversation_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "user_message": input_data.message,
            "eefai_response": response_text,
            "intent": intent
        }
        
        await db.eefai_state.update_one(
            {"user_id": user_id},
            {
                "$push": {
                    "conversation_history": {
                        "$each": [conversation_entry],
                        "$slice": -30  # Keep last 30
                    }
                }
            }
        )
        
        result = EEFaiMessageOutput(
            response_id=response_id,
            text=response_text,
            actions=actions,
            provenance_ref=f"eefai_{input_data.trace_id}"
        )
        
        logger.info(f"EEFai responded to user {user_id}: intent={intent}")
        
        return result
        
    except Exception as e:
        logger.error(f"EEFai message failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{user_id}/assign-plan")
async def assign_plan(user_id: str, plan_id: str):
    """Assign plan to user's EEFai"""
    try:
        db = get_mongo_db()
        
        result = await db.eefai_state.update_one(
            {"user_id": user_id},
            {"$set": {"current_plan_id": plan_id}}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="EEFai instance not found")
        
        return {"message": "Plan assigned", "plan_id": plan_id}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to assign plan: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{user_id}/context")
async def get_eefai_context(user_id: str):
    """Get EEFai context and memory references"""
    try:
        db = get_mongo_db()
        state = await db.eefai_state.find_one(
            {"user_id": user_id},
            {"_id": 0, "context_refs": 1, "current_plan_id": 1}
        )
        
        if not state:
            raise HTTPException(status_code=404, detail="EEFai instance not found")
        
        return state
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get context: {e}")
        raise HTTPException(status_code=500, detail=str(e))
