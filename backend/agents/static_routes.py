"""Static onboarding endpoint for no-JS form submission"""
from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse, RedirectResponse
import logging
from database import get_mongo_db
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/onboarding", tags=["static"])


@router.post("/submit", response_class=HTMLResponse)
async def submit_onboarding_static(
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    state: str = Form(...),
    income: str = Form(...),
    expenses: str = Form(...)
):
    """
    Handle static onboarding form submission (no JS)
    
    Creates EEFai instance and redirects to dashboard
    """
    try:
        db = get_mongo_db()
        
        # Create EEFai instance
        instance = {
            "user_id": email,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "conversation_history": [],
            "current_plan_id": None,
            "stage": "stabilize",
            "profile": {
                "name": name,
                "email": email,
                "phone": phone,
                "state": state,
                "income": float(income),
                "expenses": float(expenses),
                "debts": [],
                "goals": []
            },
            "context_refs": {
                "short_term_memory": [],
                "long_term_memory": []
            }
        }
        
        await db.eefai_state.insert_one(instance)
        
        logger.info(f"Static onboarding completed for {email}")
        
        # Return success HTML
        return HTMLResponse(content=f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="utf-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1" />
            <title>Welcome to EEFai</title>
            <meta http-equiv="refresh" content="3;url=/dashboard" />
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                    margin: 0;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    min-height: 100vh;
                    background: #F9FAFB;
                }}
                .success-container {{
                    text-align: center;
                    padding: 40px;
                    background: white;
                    border-radius: 12px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                    max-width: 500px;
                }}
                h1 {{ color: #2B8BA8; margin-bottom: 16px; }}
                p {{ color: #6B7280; line-height: 1.6; }}
            </style>
        </head>
        <body>
            <div class="success-container">
                <h1>Welcome, {name}!</h1>
                <p>Your EEFai account has been created successfully.</p>
                <p>Redirecting to your dashboard in 3 seconds...</p>
                <p><a href="/dashboard" style="color: #2B8BA8;">Click here if not redirected</a></p>
            </div>
        </body>
        </html>
        """)
        
    except Exception as e:
        logger.error(f"Static onboarding error: {e}")
        return HTMLResponse(content=f"""
        <!DOCTYPE html>
        <html>
        <head><title>Error</title></head>
        <body>
            <h1>Error</h1>
            <p>There was an error creating your account: {str(e)}</p>
            <p><a href="/onboarding">Try again</a></p>
        </body>
        </html>
        """, status_code=500)
