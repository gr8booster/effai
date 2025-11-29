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

# Complete Lesson Library - 20+ lessons
LESSON_TEMPLATES = {
    "emergency_fund_basics": {
        "title": "Why You Need an Emergency Fund",
        "category": "savings",
        "duration_min": 5,
        "html": """<div class="lesson">
            <h2>Why You Need an Emergency Fund</h2>
            <p><strong>Objective:</strong> Protect yourself from unexpected expenses</p>
            <p><strong>Why it matters:</strong> Without emergency savings, one car repair can spiral into debt.</p>
            <p><strong>3-Step Plan:</strong></p>
            <ol>
                <li>Start with $1,000 goal</li>
                <li>Save $25-50 weekly</li>
                <li>Keep separate from spending</li>
            </ol>
            <p><strong>Next Action:</strong> Set aside $10 right now.</p>
        </div>"""
    },
    "debt_validation_rights": {
        "title": "Your Rights Under the FDCPA",
        "category": "debt",
        "duration_min": 3,
        "html": """<div class="lesson">
            <h2>Your Rights When Debt Collectors Call</h2>
            <p><strong>Objective:</strong> Know your legal protections</p>
            <p><strong>Why it matters:</strong> Collectors can't harass you.</p>
            <p><strong>3-Step Response:</strong></p>
            <ol>
                <li>Request validation in writing within 30 days</li>
                <li>They must STOP until they provide proof</li>
                <li>Keep records of all communications</li>
            </ol>
        </div>"""
    },
    "credit_score_factors": {
        "title": "5 Factors That Affect Your Credit Score",
        "category": "credit",
        "duration_min": 7,
        "html": """<div class="lesson">
            <h2>Understanding Credit Scores</h2>
            <p><strong>The 5 factors:</strong></p>
            <ol>
                <li><strong>Payment History (35%)</strong> - Pay on time, every time</li>
                <li><strong>Credit Utilization (30%)</strong> - Keep balances under 30% of limits</li>
                <li><strong>Credit Age (15%)</strong> - Keep old accounts open</li>
                <li><strong>Credit Mix (10%)</strong> - Different types of credit</li>
                <li><strong>New Credit (10%)</strong> - Don't open too many at once</li>
            </ol>
            <p><strong>Quick Win:</strong> Pay down high-balance cards first.</p>
        </div>"""
    },
    "statute_of_limitations": {
        "title": "Time-Barred Debts Explained",
        "category": "debt",
        "duration_min": 5,
        "html": """<div class="lesson">
            <h2>Statute of Limitations on Debt</h2>
            <p><strong>Key Concept:</strong> Old debts can't be sued for collection.</p>
            <p><strong>How it works:</strong></p>
            <ul>
                <li>Each state has time limits (3-10 years)</li>
                <li>After that, debt is "time-barred"</li>
                <li>Collectors can still ask, but can't sue</li>
                <li>Never restart the clock by making payments</li>
            </ul>
        </div>"""
    },
    "credit_utilization": {
        "title": "Mastering Credit Utilization",
        "category": "credit",
        "duration_min": 4,
        "html": """<div class="lesson">
            <h2>The 30% Rule</h2>
            <p><strong>Simple Rule:</strong> Keep balances below 30% of credit limits.</p>
            <p><strong>Why:</strong> High utilization = 30% of your score!</p>
            <p><strong>Action Steps:</strong></p>
            <ol>
                <li>Calculate current utilization: (balance / limit) × 100</li>
                <li>Pay down highest-utilization cards first</li>
                <li>Request credit limit increases (don't use the extra!)</li>
            </ol>
        </div>"""
    },
    "debt_snowball_method": {
        "title": "Debt Snowball vs Avalanche",
        "category": "debt",
        "duration_min": 6,
        "html": """<div class="lesson">
            <h2>Two Proven Payoff Strategies</h2>
            <p><strong>Snowball Method:</strong> Pay smallest balance first</p>
            <ul><li>Pro: Quick wins, motivation</li><li>Con: May pay more interest</li></ul>
            <p><strong>Avalanche Method:</strong> Pay highest APR first</p>
            <ul><li>Pro: Save most money</li><li>Con: Slower initial progress</li></ul>
            <p><strong>Choose based on:</strong> Need motivation? Snowball. Want to save money? Avalanche.</p>
        </div>"""
    },
    "building_credit_from_scratch": {
        "title": "Building Credit With No History",
        "category": "credit",
        "duration_min": 5,
        "html": """<div class="lesson">
            <h2>Starting From Zero</h2>
            <p><strong>Step-by-step plan:</strong></p>
            <ol>
                <li>Get a secured credit card ($200-500 deposit)</li>
                <li>Use it for small purchases monthly</li>
                <li>Pay in FULL each month</li>
                <li>After 6 months, apply for regular card</li>
                <li>Request credit limit increases every 6 months</li>
            </ol>
            <p><strong>Timeline:</strong> 12-18 months to build good score.</p>
        </div>"""
    },
    "dealing_with_collectors": {
        "title": "How to Talk to Debt Collectors",
        "category": "debt",
        "duration_min": 4,
        "html": """<div class="lesson">
            <h2>Stay In Control</h2>
            <p><strong>Do:</strong></p>
            <ul>
                <li>Ask for written validation</li>
                <li>Keep records of every call</li>
                <li>Stay calm and polite</li>
                <li>Request communication by mail only</li>
            </ul>
            <p><strong>Don't:</strong></p>
            <ul>
                <li>Admit the debt is yours</li>
                <li>Make promises you can't keep</li>
                <li>Give access to your bank account</li>
                <li>Accept verbal agreements</li>
            </ul>
        </div>"""
    },
    "credit_report_errors": {
        "title": "Common Credit Report Errors",
        "category": "credit",
        "duration_min": 6,
        "html": """<div class="lesson">
            <h2>What to Look For</h2>
            <p><strong>Common Errors:</strong></p>
            <ol>
                <li>Accounts that aren't yours</li>
                <li>Wrong account status</li>
                <li>Duplicate accounts</li>
                <li>Incorrect balances or limits</li>
                <li>Outdated information (>7 years)</li>
            </ol>
            <p><strong>Action:</strong> Dispute any error within 30 days of finding it.</p>
        </div>"""
    },
    "50_30_20_budget": {
        "title": "The 50/30/20 Budget Rule",
        "category": "savings",
        "duration_min": 5,
        "html": """<div class="lesson">
            <h2>Simple Budget Framework</h2>
            <p><strong>Allocate your income:</strong></p>
            <ul>
                <li><strong>50% Needs</strong> - Housing, utilities, food, transport</li>
                <li><strong>30% Wants</strong> - Entertainment, dining out, hobbies</li>
                <li><strong>20% Savings</strong> - Emergency fund, retirement, debt payoff</li>
            </ul>
            <p><strong>Quick Check:</strong> Is your rent more than 50% of income? Adjust.</p>
        </div>"""
    },
    "disputing_credit_bureaus": {
        "title": "How to Dispute Credit Bureau Errors",
        "category": "credit",
        "duration_min": 8,
        "html": """<div class="lesson">
            <h2>Filing Effective Disputes</h2>
            <p><strong>Process:</strong></p>
            <ol>
                <li>Get free reports from all 3 bureaus</li>
                <li>Identify specific inaccuracies</li>
                <li>Write dispute letter (use our template)</li>
                <li>Send certified mail with return receipt</li>
                <li>Bureau has 30 days to investigate</li>
                <li>They must correct or delete if unverifiable</li>
            </ol>
        </div>"""
    },
    "pay_for_delete": {
        "title": "Pay-for-Delete Negotiations",
        "category": "debt",
        "duration_min": 7,
        "html": """<div class="lesson">
            <h2>Getting Collections Removed</h2>
            <p><strong>Strategy:</strong> Offer payment in exchange for deletion</p>
            <p><strong>Steps:</strong></p>
            <ol>
                <li>Verify debt is yours and accurate</li>
                <li>Offer 40-60% of balance</li>
                <li>Request deletion from all bureaus IN WRITING</li>
                <li>Get agreement BEFORE paying</li>
                <li>Keep all documentation</li>
            </ol>
            <p><strong>Note:</strong> Not all collectors will agree, but many do.</p>
        </div>"""
    },
    "building_emergency_fund": {
        "title": "Your First $1000",
        "category": "savings",
        "duration_min": 4,
        "html": """<div class="lesson">
            <h2>Small Steps to Big Safety Net</h2>
            <p><strong>Why $1000?</strong> Covers 80% of emergencies</p>
            <p><strong>How to get there:</strong></p>
            <ul>
                <li>Week 1-4: Save $50/week = $200</li>
                <li>Week 5-8: Save $50/week = $400 total</li>
                <li>Week 9-12: Save $50/week = $600 total</li>
                <li>Week 13-20: Save $50/week = $1000!</li>
            </ul>
            <p><strong>5 months to financial peace.</strong></p>
        </div>"""
    },
    "goodwill_letters": {
        "title": "Goodwill Letters for Late Payments",
        "category": "credit",
        "duration_min": 5,
        "html": """<div class="lesson">
            <h2>Asking for Forgiveness</h2>
            <p><strong>What:</strong> Polite letter asking creditor to remove late payment</p>
            <p><strong>When to use:</strong> One-time late payment, good history otherwise</p>
            <p><strong>Key points to include:</strong></p>
            <ul>
                <li>Acknowledge the late payment</li>
                <li>Explain the reason (medical, job loss)</li>
                <li>Emphasize your good history</li>
                <li>Request removal as courtesy</li>
            </ul>
        </div>"""
    },
    "authorized_user_strategy": {
        "title": "Boost Score as Authorized User",
        "category": "credit",
        "duration_min": 4,
        "html": """<div class="lesson">
            <h2>Piggybacking on Good Credit</h2>
            <p><strong>Strategy:</strong> Get added to someone's old, good account</p>
            <p><strong>Requirements:</strong></p>
            <ul>
                <li>Find someone with excellent credit</li>
                <li>Their account must be 5+ years old</li>
                <li>Low utilization on that account</li>
                <li>Perfect payment history</li>
            </ul>
            <p><strong>Impact:</strong> Can add 50-100 points in 30-60 days</p>
        </div>"""
    },
    "settlement_negotiations": {
        "title": "Negotiating Debt Settlements",
        "category": "debt",
        "duration_min": 8,
        "html": """<div class="lesson">
            <h2>Getting 40-60% Off Your Debt</h2>
            <p><strong>When collectors will settle:</strong> Old debts, charged-off accounts</p>
            <p><strong>Negotiation tactics:</strong></p>
            <ol>
                <li>Start at 25-30% of balance</li>
                <li>Never go above 50%</li>
                <li>Get EVERYTHING in writing first</li>
                <li>Request "Paid in Full" reporting</li>
                <li>Pay by money order (never bank access)</li>
            </ol>
        </div>"""
    },
    "credit_mix_optimization": {
        "title": "Optimizing Your Credit Mix",
        "category": "credit",
        "duration_min": 5,
        "html": """<div class="lesson">
            <h2>Variety Matters (10% of Score)</h2>
            <p><strong>Types of credit:</strong></p>
            <ul>
                <li>Revolving (credit cards)</li>
                <li>Installment (car loans, personal loans)</li>
                <li>Mortgage</li>
            </ul>
            <p><strong>Strategy:</strong> If you only have cards, consider a small installment loan.</p>
            <p><strong>Warning:</strong> Don't take debt just for mix - only if needed.</p>
        </div>"""
    },
    "stopping_wage_garnishment": {
        "title": "Stopping Wage Garnishment",
        "category": "debt",
        "duration_min": 6,
        "html": """<div class="lesson">
            <h2>Your Options When Wages Are Garnished</h2>
            <p><strong>Options:</strong></p>
            <ol>
                <li><strong>Exemptions:</strong> Some income is protected (SSI, disability)</li>
                <li><strong>Negotiate:</strong> Work out payment plan before judgment</li>
                <li><strong>Bankruptcy:</strong> Stops garnishment immediately</li>
                <li><strong>Contest:</strong> Challenge if debt is invalid</li>
            </ol>
            <p><strong>Time-sensitive:</strong> Act before garnishment starts.</p>
        </div>"""
    },
    "hard_vs_soft_inquiries": {
        "title": "Hard vs Soft Credit Inquiries",
        "category": "credit",
        "duration_min": 3,
        "html": """<div class="lesson">
            <h2>Protecting Your Score</h2>
            <p><strong>Soft Inquiries (No Impact):</strong></p>
            <ul><li>Checking your own score</li><li>Pre-approved offers</li><li>Background checks</li></ul>
            <p><strong>Hard Inquiries (Small Impact):</strong></p>
            <ul><li>Credit card applications</li><li>Loan applications</li><li>-5 to -10 points each</li></ul>
            <p><strong>Rule:</strong> Limit hard pulls to 1-2 per year.</p>
        </div>"""
    },
    "medical_debt_rights": {
        "title": "Special Rules for Medical Debt",
        "category": "debt",
        "duration_min": 5,
        "html": """<div class="lesson">
            <h2>Medical Bills Are Different</h2>
            <p><strong>Your Rights:</strong></p>
            <ul>
                <li>180-day waiting period before credit reporting</li>
                <li>Paid medical collections must be removed</li>
                <li>Under $500 not reported (as of 2023)</li>
                <li>Negotiate before it hits credit report</li>
            </ul>
        </div>"""
    },
    "savings_automation": {
        "title": "Automate Your Way to Savings",
        "category": "savings",
        "duration_min": 4,
        "html": """<div class="lesson">
            <h2>Set It and Forget It</h2>
            <p><strong>Automation strategies:</strong></p>
            <ol>
                <li>Direct deposit split (10-20% to savings)</li>
                <li>Round-up apps (save spare change)</li>
                <li>Scheduled transfers (day after payday)</li>
                <li>Cash-back rewards to savings</li>
            </ol>
        </div>"""
    },
    "bankruptcy_basics": {
        "title": "When to Consider Bankruptcy",
        "category": "debt",
        "duration_min": 7,
        "html": """<div class="lesson">
            <h2>Last Resort, Fresh Start</h2>
            <p><strong>Chapter 7:</strong> Wipes out most debts in 3-4 months</p>
            <p><strong>Chapter 13:</strong> Repayment plan over 3-5 years</p>
            <p><strong>Consider if:</strong></p>
            <ul>
                <li>Debt > 50% of annual income</li>
                <li>Lawsuits or garnishments active</li>
                <li>Can't pay minimums</li>
            </ul>
            <p><strong>Cost:</strong> $1000-2000 in legal fees</p>
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
        
        else:
            # Generic tasks
            tasks = [
                MentorTask(
                    task_id=str(uuid.uuid4()),
                    description="Review your financial situation",
                    time_est_min=5,
                    resources=[],
                    provenance_ref=f"mentor_{input_data.trace_id}"
                )
            ]
            lesson = None
        
        # Store tasks
        db = get_mongo_db()
        task_docs = [{\n            \"task_id\": task.task_id,
            \"user_id\": input_data.user_id,
            \"plan_id\": input_data.plan_id,
            \"milestone_id\": input_data.milestone_id,
            \"description\": task.description,
            \"time_est_min\": task.time_est_min,
            \"resources\": task.resources,
            \"status\": \"pending\",
            \"created_at\": datetime.now(timezone.utc).isoformat()
        } for task in tasks]
        
        if task_docs:
            await db.mentor_tasks.insert_many(task_docs)
        
        result = MentorGenerateTasksOutput(
            tasks=tasks,
            lesson_of_day=lesson
        )
        
        logger.info(f\"Generated {len(tasks)} tasks for milestone {input_data.milestone_id}\")
        
        return result
        
    except Exception as e:
        logger.error(f\"Task generation failed: {e}\")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/lessons/list")
async def get_all_lessons():
    """Get list of all available lessons"""
    try:
        lessons = []
        for lesson_id, lesson_data in LESSON_TEMPLATES.items():
            lessons.append({
                "id": lesson_id,
                "title": lesson_data["title"],
                "category": lesson_data.get("category", "general"),
                "duration_min": lesson_data.get("duration_min", 5)
            })
        
        return {"lessons": lessons, "total": len(lessons)}
        
    except Exception as e:
        logger.error(f"Failed to get lessons: {e}")
        raise HTTPException(status_code=500, detail=str(e))

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
    """Mark task as completed and update user streak"""
    try:
        db = get_mongo_db()
        
        # Mark task complete
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
        
        # Update user streak
        await update_user_streak(user_id)
        
        # Get updated streak info
        streak_info = await get_user_streak(user_id)
        
        return {
            "message": "Task marked complete",
            "task_id": task_id,
            "streak": streak_info
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to mark task complete: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tasks/active")
async def get_active_tasks(user_id: str):
    """Get all active tasks for user"""
    try:
        db = get_mongo_db()
        
        tasks = await db.mentor_tasks.find(
            {"user_id": user_id, "status": {"$ne": "completed"}},
            {"_id": 0}
        ).sort("created_at", 1).to_list(50)
        
        return {"tasks": tasks, "count": len(tasks)}
        
    except Exception as e:
        logger.error(f"Failed to get tasks: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/streak")
async def get_streak(user_id: str):
    """Get user's current streak"""
    try:
        streak_info = await get_user_streak(user_id)
        return streak_info
    except Exception as e:
        logger.error(f"Failed to get streak: {e}")
        raise HTTPException(status_code=500, detail=str(e))


async def update_user_streak(user_id: str):
    """Update user's task completion streak"""
    db = get_mongo_db()
    
    # Get user state
    user_state = await db.eefai_state.find_one({"user_id": user_id})
    if not user_state:
        return
    
    # Get completed tasks today
    today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
    
    completed_today = await db.mentor_tasks.count_documents({
        "user_id": user_id,
        "status": "completed",
        "completed_at": {"$gte": today_start}
    })
    
    # Update streak in profile
    current_streak = user_state.get("streak", {})
    
    if completed_today > 0:
        # User completed at least one task today
        last_activity = current_streak.get("last_activity_date")
        
        if last_activity:
            last_date = datetime.fromisoformat(last_activity).date()
            today = datetime.now(timezone.utc).date()
            
            if (today - last_date).days == 1:
                # Consecutive day - increment streak
                current_count = current_streak.get("current_streak", 0) + 1
            elif (today - last_date).days == 0:
                # Same day - maintain streak
                current_count = current_streak.get("current_streak", 1)
            else:
                # Streak broken - restart
                current_count = 1
        else:
            # First day
            current_count = 1
        
        new_streak = {
            "current_streak": current_count,
            "longest_streak": max(current_count, current_streak.get("longest_streak", 0)),
            "total_tasks_completed": current_streak.get("total_tasks_completed", 0) + 1,
            "last_activity_date": datetime.now(timezone.utc).isoformat()
        }
        
        await db.eefai_state.update_one(
            {"user_id": user_id},
            {"$set": {"streak": new_streak}}
        )


async def get_user_streak(user_id: str) -> dict:
    """Get user's streak information"""
    db = get_mongo_db()
    
    user_state = await db.eefai_state.find_one({"user_id": user_id})
    if not user_state:
        return {"current_streak": 0, "longest_streak": 0, "total_tasks_completed": 0}
    
    return user_state.get("streak", {"current_streak": 0, "longest_streak": 0, "total_tasks_completed": 0})
