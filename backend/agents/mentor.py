"""MentorAgent - Micro-learning and task generation - CLEAN VERSION"""
from fastapi import APIRouter, HTTPException
import logging
import uuid
from datetime import datetime, timezone

from schemas import (
    MentorGenerateTasksInput,
    MentorGenerateTasksOutput,
    MentorTask,
    MentorLesson
)
from database import get_mongo_db

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/mentor", tags=["mentor"])

# Simplified lesson templates
LESSON_TEMPLATES = {
    "emergency_fund_basics": {
        "title": "Emergency Fund Basics",
        "category": "savings",
        "duration_min": 5,
        "html": "<h2>Build Your Safety Net</h2><p>Start with $1000 goal. Save weekly. Keep separate.</p>"
    },
    "debt_rights": {
        "title": "Your FDCPA Rights",
        "category": "debt",
        "duration_min": 3,
        "html": "<h2>Debt Collector Rights</h2><p>Request validation. They must stop until they prove it.</p>"
    }
}

@router.post("/generate-tasks", response_model=MentorGenerateTasksOutput)
async def generate_tasks(input_data: MentorGenerateTasksInput):
    """Generate daily tasks"""
    try:
        tasks = [
            MentorTask(
                task_id=str(uuid.uuid4()),
                description="Set up emergency savings",
                time_est_min=10,
                resources=[],
                provenance_ref=f"mentor_{input_data.trace_id}"
            ),
            MentorTask(
                task_id=str(uuid.uuid4()),
                description="Calculate monthly surplus",
                time_est_min=5,
                resources=[],
                provenance_ref=f"mentor_{input_data.trace_id}"
            ),
            MentorTask(
                task_id=str(uuid.uuid4()),
                description="Make first $10 deposit",
                time_est_min=2,
                resources=[],
                provenance_ref=f"mentor_{input_data.trace_id}"
            )
        ]
        
        db = get_mongo_db()
        task_docs = [{
            "task_id": task.task_id,
            "user_id": input_data.user_id,
            "plan_id": input_data.plan_id,
            "milestone_id": input_data.milestone_id,
            "description": task.description,
            "time_est_min": task.time_est_min,
            "resources": task.resources,
            "status": "pending",
            "created_at": datetime.now(timezone.utc).isoformat()
        } for task in tasks]
        
        await db.mentor_tasks.insert_many(task_docs)
        
        result = MentorGenerateTasksOutput(
            tasks=tasks,
            lesson_of_day=MentorLesson(id="emergency_fund_basics", html=LESSON_TEMPLATES["emergency_fund_basics"]["html"])
        )
        
        return result
    except Exception as e:
        logger.error(f"Task generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/lesson/{lesson_id}")
async def get_lesson(lesson_id: str):
    """Get lesson"""
    if lesson_id in LESSON_TEMPLATES:
        return LESSON_TEMPLATES[lesson_id]
    raise HTTPException(status_code=404, detail="Not found")

@router.get("/lessons/list")
async def get_all_lessons():
    """Get all lessons"""
    lessons = [{"id": lid, **data} for lid, data in LESSON_TEMPLATES.items()]
    return {"lessons": lessons, "total": len(lessons)}

@router.post("/tasks/{task_id}/complete")
async def mark_task_complete(task_id: str, user_id: str):
    """Mark task complete"""
    db = get_mongo_db()
    await db.mentor_tasks.update_one(
        {"task_id": task_id, "user_id": user_id},
        {"$set": {"status": "completed", "completed_at": datetime.now(timezone.utc).isoformat()}}
    )
    return {"message": "Task complete"}

@router.get("/tasks/active")
async def get_active_tasks(user_id: str):
    """Get active tasks"""
    db = get_mongo_db()
    tasks = await db.mentor_tasks.find({"user_id": user_id, "status": {"$ne": "completed"}}, {"_id": 0}).to_list(50)
    return {"tasks": tasks, "count": len(tasks)}
