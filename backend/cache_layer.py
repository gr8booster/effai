"""
Redis caching layer for high-performance lookups
Caches: SOL lookups, legal rules, CFP calculations, letter templates
"""
import logging
from typing import Optional, Any
import json
from database import get_redis

logger = logging.getLogger(__name__)

DEFAULT_TTL = 600  # 10 minutes


async def cache_get(key: str) -> Optional[Any]:
    """Get value from cache"""
    redis = get_redis()
    if not redis:
        return None
    
    try:
        value = await redis.get(key)
        if value:
            logger.debug(f"Cache HIT: {key}")
            return json.loads(value)
        logger.debug(f"Cache MISS: {key}")
        return None
    except Exception as e:
        logger.warning(f"Cache get error: {e}")
        return None


async def cache_set(key: str, value: Any, ttl: int = DEFAULT_TTL):
    """Set value in cache with TTL"""
    redis = get_redis()
    if not redis:
        return False
    
    try:
        await redis.setex(key, ttl, json.dumps(value))
        logger.debug(f"Cache SET: {key} (TTL: {ttl}s)")
        return True
    except Exception as e:
        logger.warning(f"Cache set error: {e}")
        return False


async def cache_delete(key: str):
    """Delete key from cache"""
    redis = get_redis()
    if not redis:
        return False
    
    try:
        await redis.delete(key)
        logger.debug(f"Cache DELETE: {key}")
        return True
    except Exception as e:
        logger.warning(f"Cache delete error: {e}")
        return False


async def cache_sol_lookup(state: str, debt_type: str, result: dict):
    """Cache statute of limitations lookup"""
    key = f"sol:{state}:{debt_type}"
    await cache_set(key, result, ttl=86400)  # 24 hours


async def get_cached_sol(state: str, debt_type: str) -> Optional[dict]:
    """Get cached SOL lookup"""
    key = f"sol:{state}:{debt_type}"
    return await cache_get(key)


async def cache_legal_rule(rule_code: str, rule: dict):
    """Cache legal rule"""
    key = f"legal_rule:{rule_code}"
    await cache_set(key, rule, ttl=86400)  # 24 hours


async def get_cached_legal_rule(rule_code: str) -> Optional[dict]:
    """Get cached legal rule"""
    key = f"legal_rule:{rule_code}"
    return await cache_get(key)


async def cache_cfp_calculation(user_id: str, scenario_hash: str, result: dict):
    """Cache CFP calculation"""
    key = f"cfp:{user_id}:{scenario_hash}"
    await cache_set(key, result, ttl=300)  # 5 minutes


async def get_cached_cfp(user_id: str, scenario_hash: str) -> Optional[dict]:
    """Get cached CFP calculation"""
    key = f"cfp:{user_id}:{scenario_hash}"
    return await cache_get(key)
