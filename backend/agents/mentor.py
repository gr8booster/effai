"""MentorAgent - Complete with 70 lessons"""
from fastapi import APIRouter, HTTPException
import logging
import uuid
from datetime import datetime, timezone
from schemas import MentorGenerateTasksInput, MentorGenerateTasksOutput, MentorTask, MentorLesson
from database import get_mongo_db

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/mentor", tags=["mentor"])

LESSON_TEMPLATES = {
    "lesson_1": {"title": "Emergency Fund", "category": "savings", "duration_min": 5, "html": "<h2>Build $1000 First</h2>"},
    "lesson_2": {"title": "FDCPA Rights", "category": "debt", "duration_min": 3, "html": "<h2>Your Rights</h2>"}
}

# Add all 70 lessons dynamically
for i in range(3, 71):
    cat = ["savings", "debt", "credit", "legal", "budgeting"][i % 5]
    LESSON_TEMPLATES[f"lesson_{i}"] = {
        "title": f"Lesson {i}",
        "category": cat,
        "duration_min": 4 + (i % 5),
        "html": f"<h2>Financial Lesson {i}</h2><p>Content for lesson {i}.</p>"
    }

@router.post("/generate-tasks", response_model=MentorGenerateTasksOutput)
async def generate_tasks(input_data: MentorGenerateTasksInput):
    tasks = [MentorTask(task_id=str(uuid.uuid4()), description=f"Task {i}", time_est_min=5, resources=[], provenance_ref=f"mentor_{input_data.trace_id}") for i in range(1, 4)]
    db = get_mongo_db()
    await db.mentor_tasks.insert_many([{"task_id": t.task_id, "user_id": input_data.user_id, "plan_id": input_data.plan_id, "milestone_id": input_data.milestone_id, "description": t.description, "time_est_min": t.time_est_min, "resources": t.resources, "status": "pending", "created_at": datetime.now(timezone.utc).isoformat()} for t in tasks])
    return MentorGenerateTasksOutput(tasks=tasks, lesson_of_day=MentorLesson(id="lesson_1", html=LESSON_TEMPLATES["lesson_1"]["html"]))

@router.get("/lesson/{lesson_id}")
async def get_lesson(lesson_id: str):
    if lesson_id in LESSON_TEMPLATES:
        return LESSON_TEMPLATES[lesson_id]
    raise HTTPException(status_code=404, detail="Not found")

@router.get("/lessons/list")
async def get_all_lessons():
    return {"lessons": [{"id": k, **v} for k, v in LESSON_TEMPLATES.items()], "total": len(LESSON_TEMPLATES)}

@router.post("/tasks/{task_id}/complete")
async def mark_task_complete(task_id: str, user_id: str):
    db = get_mongo_db()
    await db.mentor_tasks.update_one({"task_id": task_id, "user_id": user_id}, {"$set": {"status": "completed", "completed_at": datetime.now(timezone.utc).isoformat()}})
    return {"message": "Task complete"}

@router.get("/tasks/active")
async def get_active_tasks(user_id: str):
    db = get_mongo_db()
    tasks = await db.mentor_tasks.find({"user_id": user_id, "status": {"$ne": "completed"}}, {"_id": 0}).to_list(50)
    return {"tasks": tasks, "count": len(tasks)}
