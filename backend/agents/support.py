"""SupportAgent - Human review queue and escalation management"""
from fastapi import APIRouter, HTTPException
import logging
from typing import List
from datetime import datetime, timezone

from schemas import (
    SupportReviewInput,
    SupportReviewItem,
    SupportReviewDecision
)
from database import get_mongo_db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/support", tags=["support"])


@router.get("/queue", response_model=List[SupportReviewItem])
async def get_review_queue():
    """
    Get all items needing human review
    """
    try:
        db = get_mongo_db()
        
        # Get all flagged items that are pending review
        items = await db.support_queue.find(
            {"status": "pending"},
            {"_id": 0}
        ).sort("created_at", 1).to_list(100)
        
        # Convert to SupportReviewItem objects
        review_items = []
        for item in items:
            review_items.append(SupportReviewItem(
                item_id=item["item_id"],
                run_id=item["run_id"],
                agent_id=item["agent_id"],
                payload=item["payload"],
                provenance_ref=item["provenance_ref"],
                flagged_reason=item["flagged_reason"],
                created_at=datetime.fromisoformat(item["created_at"])
            ))
        
        logger.info(f"Retrieved {len(review_items)} items from review queue")
        
        return review_items
        
    except Exception as e:
        logger.error(f"Failed to get review queue: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/review/{item_id}")
async def review_item(item_id: str, review: SupportReviewInput):
    """
    Human reviewer decision on flagged item
    
    Decisions:
    - approve: Allow action to proceed
    - reject: Block action
    - edit: Modify and approve
    """
    try:
        db = get_mongo_db()
        
        # Get item
        item = await db.support_queue.find_one({"item_id": item_id})
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        
        # Record review decision
        review_record = {
            "item_id": item_id,
            "reviewer_id": review.reviewer_id,
            "decision": review.decision.value,
            "notes": review.notes,
            "edited_payload": review.edited_payload,
            "reviewed_at": datetime.now(timezone.utc).isoformat()
        }
        
        await db.support_reviews.insert_one(review_record)
        
        # Update queue item status
        await db.support_queue.update_one(
            {"item_id": item_id},
            {
                "$set": {
                    "status": "reviewed",
                    "decision": review.decision.value,
                    "reviewed_at": datetime.now(timezone.utc).isoformat(),
                    "reviewer_id": review.reviewer_id
                }
            }
        )
        
        # If approved or edited, resume orchestration
        if review.decision in [SupportReviewDecision.APPROVE, SupportReviewDecision.EDIT]:
            # Signal orchestrator to continue
            # For POC, just log; Phase 2 will resume actual pipeline
            logger.info(f"Item {item_id} approved, orchestration can resume")
        
        # Update provenance with human review
        await db.audit_log.update_one(
            {"provenance_id": item["provenance_ref"]},
            {"$set": {"human_reviewed": True, "review_decision": review.decision.value}}
        )
        
        logger.info(f"Review completed for item {item_id}: {review.decision.value}")
        
        return {
            "message": "Review recorded",
            "item_id": item_id,
            "decision": review.decision.value
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Review failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/item/{item_id}")
async def get_review_item(item_id: str):
    """
    Get detailed information about a review item including provenance
    """
    try:
        db = get_mongo_db()
        
        item = await db.support_queue.find_one({"item_id": item_id}, {"_id": 0})
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        
        # Get provenance record
        provenance = await db.audit_log.find_one(
            {"provenance_id": item["provenance_ref"]},
            {"_id": 0}
        )
        
        return {
            "item": item,
            "provenance": provenance
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get item: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/flag-item")
async def flag_item_for_review(run_id: str, agent_id: str, payload: dict, reason: str):
    """
    Flag an item for human review
    
    Called by other agents when must_escalate=True
    """
    try:
        db = get_mongo_db()
        
        item = {
            "item_id": f"review_{run_id}_{agent_id}",
            "run_id": run_id,
            "agent_id": agent_id,
            "payload": payload,
            "provenance_ref": f"prov_{run_id}",
            "flagged_reason": reason,
            "status": "pending",
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        
        await db.support_queue.insert_one(item)
        
        logger.info(f"Item flagged for review: {item['item_id']} - {reason}")
        
        return {"message": "Item flagged for review", "item_id": item["item_id"]}
        
    except Exception as e:
        logger.error(f"Failed to flag item: {e}")
        raise HTTPException(status_code=500, detail=str(e))
