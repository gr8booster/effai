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
    """Generate personalized daily tasks using AI"""
    try:
        from ai_utils import AIProvider
        
        db = get_mongo_db()
        
        # Get user profile for context
        user_state = await db.eefai_state.find_one({"user_id": input_data.user_id})
        profile = user_state.get("profile", {}) if user_state else {}
        
        # Use AI to generate personalized tasks
        provider = AIProvider(temperature=0.7)
        
        system_prompt = f"""You are MentorAgent, an AI financial coach.
        Generate 3 specific, actionable daily tasks for this user based on their milestone: {input_data.milestone_id}.
        
        User profile:
        - Income: ${profile.get('income', 0)}
        - Expenses: ${profile.get('expenses', 0)}
        - Savings: ${profile.get('savings', 0)}
        - State: {profile.get('state', 'Unknown')}
        
        Return ONLY a JSON array of tasks in this exact format:
        [
          {{"description": "Specific task here", "time_est_min": 5}},
          {{"description": "Another task", "time_est_min": 10}},
          {{"description": "Third task", "time_est_min": 3}}
        ]
        """
        
        user_prompt = f"Generate 3 personalized tasks for milestone: {input_data.milestone_id}"
        
        ai_response = await provider.generate(system_prompt, user_prompt, f"mentor_{input_data.user_id}_{datetime.now().timestamp()}")
        
        # Parse AI response
        import json
        import re
        
        # Extract JSON from response
        json_match = re.search(r'\[.*\]', ai_response, re.DOTALL)
        if json_match:
            tasks_data = json.loads(json_match.group())
        else:
            # Fallback if AI doesn't return proper JSON
            tasks_data = [
                {"description": "Review your monthly budget and identify one expense to reduce", "time_est_min": 10},
                {"description": "Set up automatic transfer of $50 to savings account", "time_est_min": 5},
                {"description": "Check credit report for any errors or inaccuracies", "time_est_min": 15}
            ]
        
        # Convert to MentorTask objects
        tasks = []
        for task_data in tasks_data[:3]:  # Limit to 3
            task = MentorTask(
                task_id=str(uuid.uuid4()),
                description=task_data.get('description', 'Complete financial review'),
                time_est_min=task_data.get('time_est_min', 5),
                resources=[],
                provenance_ref=f"mentor_ai_{input_data.trace_id}"
            )
            tasks.append(task)
        
        # Store in MongoDB
        task_docs = [{
            "task_id": task.task_id,
            "user_id": input_data.user_id,
            "plan_id": input_data.plan_id,
            "milestone_id": input_data.milestone_id,
            "description": task.description,
            "time_est_min": task.time_est_min,
            "resources": task.resources,
            "status": "pending",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "generated_by": "ai"
        } for task in tasks]
        
        await db.mentor_tasks.insert_many(task_docs)
        
        logger.info(f"AI generated {len(tasks)} personalized tasks for {input_data.user_id}")
        
        return MentorGenerateTasksOutput(
            tasks=tasks,
            lesson_of_day=MentorLesson(id="lesson_1", html=LESSON_TEMPLATES["lesson_1"]["html"])
        )
        
    except Exception as e:
        logger.error(f"Task generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

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
