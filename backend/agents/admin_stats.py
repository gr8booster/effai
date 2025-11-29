"""Admin statistics and analytics endpoint"""
from fastapi import APIRouter
import logging
from database import get_mongo_db
from datetime import datetime, timezone, timedelta

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/stats")
async def get_admin_stats():
    """Get comprehensive admin statistics"""
    try:
        db = get_mongo_db()
        
        # User stats
        total_users = await db.users.count_documents({})
        active_users_7d = await db.eefai_state.count_documents({
            "conversation_history.0.timestamp": {
                "$gte": (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()
            }
        })
        
        # Task stats
        total_tasks = await db.mentor_tasks.count_documents({})
        completed_tasks = await db.mentor_tasks.count_documents({"status": "completed"})
        
        # Letter stats
        total_letters = await db.generated_documents.count_documents({})
        
        # Review queue stats
        pending_reviews = await db.support_queue.count_documents({"status": "pending"})
        
        # Audit stats
        total_audit_logs = await db.audit_log.count_documents({})
        logs_last_24h = await db.audit_log.count_documents({
            "timestamp_utc": {"$gte": (datetime.now(timezone.utc) - timedelta(hours=24)).isoformat()}
        })
        
        return {
            "users": {
                "total": total_users,
                "active_7d": active_users_7d
            },
            "tasks": {
                "total": total_tasks,
                "completed": completed_tasks,
                "completion_rate": round((completed_tasks / total_tasks * 100), 1) if total_tasks > 0 else 0
            },
            "letters": {
                "total": total_letters
            },
            "reviews": {
                "pending": pending_reviews
            },
            "audit": {
                "total_logs": total_audit_logs,
                "last_24h": logs_last_24h
            }
        }
    except Exception as e:
        logger.error(f"Stats error: {e}")
        return {
            "users": {"total": 0, "active_7d": 0},
            "tasks": {"total": 0, "completed": 0, "completion_rate": 0},
            "letters": {"total": 0},
            "reviews": {"pending": 0},
            "audit": {"total_logs": 0, "last_24h": 0}
        }


@router.get("/users/list")
async def list_users(limit: int = 50, offset: int = 0):
    """List all users with pagination"""
    try:
        db = get_mongo_db()
        
        users = await db.users.find(
            {},
            {"_id": 0, "password_hash": 0}
        ).skip(offset).limit(limit).to_list(limit)
        
        total = await db.users.count_documents({})
        
        return {
            "users": users,
            "total": total,
            "limit": limit,
            "offset": offset
        }
    except Exception as e:
        logger.error(f"User list error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health-check")
async def health_check():
    """Comprehensive health check for admin monitoring"""
    try:
        from database import get_mongo_db, get_redis
        
        health = {
            "status": "healthy",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "services": {}
        }
        
        # Check MongoDB
        try:
            db = get_mongo_db()
            await db.command("ping")
            health["services"]["mongodb"] = "healthy"
        except Exception as e:
            health["services"]["mongodb"] = f"unhealthy: {str(e)}"
            health["status"] = "degraded"
        
        # Check Redis
        redis = get_redis()
        if redis:
            try:
                await redis.ping()
                health["services"]["redis"] = "healthy"
            except Exception as e:
                health["services"]["redis"] = f"unhealthy: {str(e)}"
        else:
            health["services"]["redis"] = "not_configured"
        
        # Check AI availability
        try:
            from ai_utils import AIProvider
            provider = AIProvider()
            test_response = await provider.generate("Say OK", "Test", "health_check")
            health["services"]["openai"] = "healthy" if test_response else "unhealthy"
        except Exception as e:
            health["services"]["openai"] = f"unhealthy: {str(e)}"
            health["status"] = "degraded"
        
        return health
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
