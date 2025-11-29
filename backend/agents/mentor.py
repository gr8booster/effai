"""MentorAgent - Micro-learning and daily task generator"""
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

# Lesson templates
LESSON_TEMPLATES = {
    "emergency_fund_basics": {
        "title": "Why You Need an Emergency Fund",
        "html": """<div class="lesson">
            <h2>Why You Need an Emergency Fund</h2>
            <p><strong>Objective:</strong> Protect yourself from unexpected expenses</p>
            <p><strong>Why it matters:</strong> Without emergency savings, one unexpected car repair or medical bill can spiral into debt.</p>
            <p><strong>The 3-Step Plan:</strong></p>
            <ol>
                <li>Start with a goal of $1,000 (covers most emergencies)</li>
                <li>Save small amounts weekly ($25-50)</li>
                <li>Keep it separate from spending money</li>
            </ol>
            <p><strong>Next Action:</strong> Set aside $10 right now, even if it's in a jar. That's your start.</p>
        </div>"""
    },
    "debt_validation_rights": {
        "title": "Your Rights Under the FDCPA",
        "html": """<div class="lesson">
            <h2>Your Rights When Debt Collectors Call</h2>
            <p><strong>Objective:</strong> Understand your legal protections</p>
            <p><strong>Why it matters:</strong> Debt collectors can't harass you, and you have the right to verify any debt.</p>
            <p><strong>The 3-Step Response:</strong></p>
            <ol>
                <li>Request validation in writing within 30 days</li>
                <li>They must STOP collecting until they provide proof</li>
                <li>Keep records of all communications</li>
            </ol>
            <p><strong>Next Action:</strong> If you got a collection letter, request validation today. We'll help you write it.</p>
        </div>"""
    }
}


@router.post("/generate-tasks", response_model=MentorGenerateTasksOutput)
async def generate_tasks(input_data: MentorGenerateTasksInput):
    """
    Generate daily micro-tasks from plan milestone
    """
    try:
        # For POC, generate template tasks based on milestone
        tasks = []
        
        if "emergency" in input_data.milestone_id.lower():
            tasks = [
                MentorTask(
                    task_id=str(uuid.uuid4()),
                    description="Set up a separate savings account or jar for emergency fund",
                    time_est_min=10,
                    resources=["https://www.consumer.gov/articles/saving-emergency-fund"],
                    provenance_ref=f"mentor_{input_data.trace_id}"
                ),
                MentorTask(
                    task_id=str(uuid.uuid4()),
                    description="Calculate your monthly surplus (income - expenses)",
                    time_est_min=5,
                    resources=[],
                    provenance_ref=f"mentor_{input_data.trace_id}"
                ),
                MentorTask(
                    task_id=str(uuid.uuid4()),
                    description="Make your first $10 deposit",
                    time_est_min=2,
                    resources=[],
                    provenance_ref=f"mentor_{input_data.trace_id}"
                )
            ]
            
            lesson = MentorLesson(
                id="emergency_fund_basics",
                html=LESSON_TEMPLATES["emergency_fund_basics"]["html"]
            )
        
        elif "debt" in input_data.milestone_id.lower():
            tasks = [
                MentorTask(
                    task_id=str(uuid.uuid4()),
                    description="Gather all debt collection letters you've received",
                    time_est_min=5,
                    resources=[],
                    provenance_ref=f"mentor_{input_data.trace_id}"
                ),
                MentorTask(
                    task_id=str(uuid.uuid4()),
                    description="Check the date on each letter (you have 30 days to request validation)",
                    time_est_min=3,
                    resources=["https://www.ftc.gov/debt-collection"],
                    provenance_ref=f"mentor_{input_data.trace_id}"
                ),
                MentorTask(
                    task_id=str(uuid.uuid4()),
                    description="Upload one debt letter to start your defense plan",
                    time_est_min=2,
                    resources=[],
                    provenance_ref=f"mentor_{input_data.trace_id}"
                )
            ]
            
            lesson = MentorLesson(
                id="debt_validation_rights",
                html=LESSON_TEMPLATES["debt_validation_rights"]["html"]
            )
        
        else:
            # Generic tasks
            tasks = [
                MentorTask(
                    task_id=str(uuid.uuid4()),
                    description="Review your current financial situation",
                    time_est_min=5,
                    resources=[],
                    provenance_ref=f"mentor_{input_data.trace_id}"
                )
            ]
            lesson = None
        
        # Store tasks in database
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
        
        if task_docs:
            await db.mentor_tasks.insert_many(task_docs)
        
        result = MentorGenerateTasksOutput(
            tasks=tasks,
            lesson_of_day=lesson
        )
        
        logger.info(f"Generated {len(tasks)} tasks for milestone {input_data.milestone_id}")
        
        return result
        
    except Exception as e:
        logger.error(f"Task generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/lesson/{lesson_id}")
async def get_lesson(lesson_id: str):
    """Get lesson by ID"""
    try:
        if lesson_id in LESSON_TEMPLATES:
            return LESSON_TEMPLATES[lesson_id]
        
        raise HTTPException(status_code=404, detail="Lesson not found")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get lesson: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/tasks/{task_id}/complete")
async def mark_task_complete(task_id: str, user_id: str):
    """Mark task as completed"""
    try:
        db = get_mongo_db()
        
        result = await db.mentor_tasks.update_one(
            {"task_id": task_id, "user_id": user_id},
            {
                "$set": {
                    "status": "completed",
                    "completed_at": datetime.now(timezone.utc).isoformat()
                }
            }
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Task not found")
        
        return {"message": "Task marked complete", "task_id": task_id}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to mark task complete: {e}")
        raise HTTPException(status_code=500, detail=str(e))
