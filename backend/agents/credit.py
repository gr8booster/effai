"""Credit Improvement AI - Complete credit repair module"""
from fastapi import APIRouter, HTTPException
import logging
from typing import List
from datetime import datetime, timezone
import uuid

from database import get_mongo_db
from ai_utils import AIProvider

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/credit", tags=["credit"])


from fastapi import APIRouter, HTTPException, Body

@router.post("/analyze")
async def analyze_credit_report(user_id: str, report_data: dict = Body(...)):
    """
    Analyze credit report  
    
    Query params: user_id
    Body: report_data with current_score, accounts array
    """
    try:
        db = get_mongo_db()
        
        # Get user state
        user_state = await db.eefai_state.find_one({"user_id": user_id})
        if not user_state:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Analyze credit factors
        analysis = {
            "analysis_id": str(uuid.uuid4()),
            "user_id": user_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "current_score_estimate": report_data.get("current_score", 0),
            "negative_items": [],
            "recommendations": [],
            "action_plan": []
        }
        
        # Identify negative items
        for item in report_data.get("accounts", []):
            if item.get("status") in ["collections", "charge-off", "late"]:
                analysis["negative_items"].append({
                    "type": item["status"],
                    "creditor": item.get("creditor"),
                    "amount": item.get("balance", 0),
                    "date": item.get("date"),
                    "disputable": True
                })
        
        # Generate recommendations
        if analysis["negative_items"]:
            analysis["recommendations"].append({
                "priority": "high",
                "action": "Dispute inaccurate items",
                "description": f"Found {len(analysis['negative_items'])} negative items that may be inaccurate",
                "impact": "+20 to +50 points if successful"
            })
        
        # Calculate credit utilization
        total_balance = sum(item.get("balance", 0) for item in report_data.get("accounts", []) if item.get("type") == "revolving")
        total_limit = sum(item.get("limit", 0) for item in report_data.get("accounts", []) if item.get("type") == "revolving")
        
        if total_limit > 0:
            utilization = (total_balance / total_limit) * 100
            analysis["utilization_rate"] = round(utilization, 2)
            
            if utilization > 30:
                analysis["recommendations"].append({
                    "priority": "high",
                    "action": "Reduce credit utilization",
                    "description": f"Current utilization: {utilization:.1f}%. Aim for under 30%.",
                    "impact": "+10 to +30 points"
                })
        
        # Generate 60-day action plan
        plan_days = [
            {"day": 1, "task": "Request free credit reports from all 3 bureaus", "duration": "15 min"},
            {"day": 3, "task": "Review reports for errors and inaccuracies", "duration": "30 min"},
            {"day": 7, "task": "Draft dispute letters for inaccurate items", "duration": "20 min"},
            {"day": 10, "task": "Send dispute letters via certified mail", "duration": "15 min"},
            {"day": 30, "task": "Pay down high-utilization credit cards", "duration": "ongoing"},
            {"day": 40, "task": "Follow up on dispute investigations", "duration": "10 min"},
            {"day": 45, "task": "Request credit limit increases on good accounts", "duration": "15 min"},
            {"day": 60, "task": "Review updated reports and measure progress", "duration": "20 min"},
        ]
        
        analysis["action_plan"] = plan_days
        
        # Store analysis
        await db.credit_analyses.insert_one(analysis)
        
        logger.info(f"Credit analysis completed for {user_id}: {len(analysis['negative_items'])} issues found")
        
        return analysis
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Credit analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/dispute/generate")
async def generate_credit_dispute(user_id: str, dispute_data: dict):
    """
    Generate credit bureau dispute letter
    
    Accepts:
    - bureau: Equifax, Experian, TransUnion
    - disputed_item: Description of item
    - reason: Why it's inaccurate
    """
    try:
        # This calls WriterAgent with credit_dispute template
        import requests
        
        response = requests.post("http://localhost:8001/api/writer/generate", json={
            "template_id": "credit_dispute_v1",
            "template_version": "1.0.0",
            "fields": {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "bureau_name": dispute_data.get("bureau", "Credit Bureau"),
                "disputed_item": dispute_data.get("disputed_item"),
                "account_number": dispute_data.get("account_number", "N/A"),
                "dispute_reason": dispute_data.get("reason"),
                "consumer_name": dispute_data.get("consumer_name"),
                "consumer_address": dispute_data.get("consumer_address")
            },
            "tone": "formal",
            "user_id": user_id,
            "trace_id": f"credit_dispute_{uuid.uuid4()}"
        })
        
        return response.json()
        
    except Exception as e:
        logger.error(f"Credit dispute generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/score/estimate")
async def estimate_credit_score(user_id: str):
    """
    Estimate credit score using AI analysis of user profile
    """
    try:
        from ai_utils import AIProvider
        
        db = get_mongo_db()
        user_state = await db.eefai_state.find_one({"user_id": user_id})
        if not user_state:
            raise HTTPException(status_code=404, detail="User not found")
        
        profile = user_state.get("profile", {})
        
        # Use AI to analyze credit profile
        provider = AIProvider(temperature=0.3)
        
        system_prompt = """You are CreditAI, an expert credit analyst.
        Analyze this user's financial profile and estimate their credit score.
        Consider: payment history, debt levels, savings habits.
        
        Respond in JSON format:
        {
          "estimated_score": 720,
          "score_range": "Good",
          "reasoning": "Brief explanation",
          "recommendations": ["Recommendation 1", "Recommendation 2", "Recommendation 3"]
        }
        """
        
        user_prompt = f"""
        User Profile:
        - Monthly Income: ${profile.get('income', 0)}
        - Monthly Expenses: ${profile.get('expenses', 0)}
        - Current Savings: ${profile.get('savings', 0)}
        - Active Debts: {len(profile.get('debts', []))}
        - Total Debt: ${sum(d.get('balance', 0) for d in profile.get('debts', []))}
        
        Estimate their credit score and provide recommendations.
        """
        
        ai_response = await provider.generate(system_prompt, user_prompt, f"credit_{user_id}_{datetime.now().timestamp()}")
        
        # Parse AI response
        import json
        import re
        
        json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
        if json_match:
            ai_data = json.loads(json_match.group())
            estimated_score = ai_data.get('estimated_score', 680)
            recommendations = ai_data.get('recommendations', [])
            score_range = ai_data.get('score_range', get_score_range(estimated_score))
        else:
            # Fallback calculation
            base_score = 300
            if len(profile.get('debts', [])) == 0:
                base_score += 250
            elif len(profile.get('debts', [])) < 3:
                base_score += 200
            else:
                base_score += 150
            
            savings = profile.get('savings', 0)
            if savings > 2000:
                base_score += 100
            elif savings > 500:
                base_score += 75
            else:
                base_score += 50
            
            base_score += 100
            estimated_score = min(base_score, 850)
            recommendations = generate_score_recommendations(estimated_score, user_state)
            score_range = get_score_range(estimated_score)
        
        return {
            "estimated_score": estimated_score,
            "score_range": score_range,
            "factors": {
                "payment_history": "Good" if len(profile.get('debts', [])) < 2 else "Fair",
                "utilization": "Good" if profile.get('savings', 0) > 1000 else "Needs improvement",
                "credit_age": "Average",
                "credit_mix": "Average",
                "new_credit": "Average"
            },
            "recommendations": recommendations,
            "ai_powered": True
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Score estimation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def get_score_range(score: int) -> str:
    """Get credit score range category"""
    if score >= 800:
        return "Exceptional"
    elif score >= 740:
        return "Very Good"
    elif score >= 670:
        return "Good"
    elif score >= 580:
        return "Fair"
    else:
        return "Poor"


def generate_score_recommendations(score: int, user_state: dict) -> list:
    """Generate personalized recommendations based on score"""
    recommendations = []
    
    if score < 670:
        recommendations.append("Dispute any inaccurate negative items on your report")
        recommendations.append("Set up automatic payments to avoid late payments")
    
    if score < 740:
        recommendations.append("Reduce credit card balances to under 30% of limits")
        recommendations.append("Request credit limit increases on good accounts")
    
    recommendations.append("Check your credit reports regularly for errors")
    recommendations.append("Keep old accounts open to maintain credit history")
    
    return recommendations
