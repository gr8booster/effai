"""Simplified database module - MongoDB only for stability"""
import os
from motor.motor_asyncio import AsyncIOMotorClient
import redis.asyncio as aioredis
from typing import Optional
import logging
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

# MongoDB Connection
mongo_client: Optional[AsyncIOMotorClient] = None
mongo_db = None

# Redis Connection (optional)
redis_client: Optional[aioredis.Redis] = None


async def init_databases():
    """Initialize MongoDB (primary) and Redis (optional)"""
    global mongo_client, mongo_db, redis_client
    
    # MongoDB - PRIMARY DATABASE
    mongo_url = os.environ['MONGO_URL']
    mongo_client = AsyncIOMotorClient(mongo_url)
    mongo_db = mongo_client[os.environ['DB_NAME']]
    logger.info("MongoDB connected")
    
    # Create indexes for performance
    await create_mongo_indexes()
    
    # Redis - OPTIONAL (for caching)
    try:
        redis_client = await aioredis.from_url(
            f"redis://{os.environ.get('REDIS_HOST', 'localhost')}:{os.environ.get('REDIS_PORT', '6379')}/{os.environ.get('REDIS_DB', '0')}",
            encoding="utf-8",
            decode_responses=True,
            socket_connect_timeout=2
        )
        logger.info("Redis connected (caching enabled)")
    except Exception as e:
        logger.warning(f"Redis not available: {e}. Caching disabled.")
        redis_client = None


async def create_mongo_indexes():
    """Create MongoDB indexes for performance"""
    try:
        # EEFai state index
        await mongo_db.eefai_state.create_index("user_id", unique=True)
        
        # Audit log index
        await mongo_db.audit_log.create_index("provenance_id", unique=True)
        await mongo_db.audit_log.create_index("timestamp_utc")
        
        # Legal rules index
        await mongo_db.legal_rules.create_index("rule_code", unique=True)
        await mongo_db.legal_rules.create_index([("state_code", 1), ("rule_type", 1)])
        
        # SOL index
        await mongo_db.statute_of_limitations.create_index([("state_code", 1), ("debt_type", 1)], unique=True)
        
        # Tasks index
        await mongo_db.mentor_tasks.create_index([("user_id", 1), ("status", 1)])
        
        logger.info("MongoDB indexes created")
    except Exception as e:
        logger.warning(f"Index creation warning: {e}")


async def close_databases():
    """Close all database connections"""
    global mongo_client, redis_client
    
    if mongo_client:
        mongo_client.close()
    
    if redis_client:
        await redis_client.close()
    
    logger.info("All databases closed")


def get_mongo_db():
    """Get MongoDB database instance"""
    return mongo_db


def get_redis():
    """Get Redis client (may be None if unavailable)"""
    return redis_client


async def seed_legal_data_mongo():
    """Seed legal rules and SOL data in MongoDB"""
    db = get_mongo_db()
    
    # Seed statute of limitations (all 50 states)
    sol_data = [
        # Original 11 states
        ('AL', 'credit_card', 3), ('AL', 'written_contract', 6),
        ('CA', 'credit_card', 4), ('CA', 'written_contract', 4),
        ('FL', 'credit_card', 4), ('FL', 'written_contract', 5),
        ('IL', 'credit_card', 5), ('IL', 'written_contract', 10),
        ('NY', 'credit_card', 6), ('NY', 'written_contract', 6),
        ('OH', 'credit_card', 6), ('OH', 'written_contract', 8),
        ('TX', 'credit_card', 4), ('TX', 'written_contract', 4),
        ('PA', 'credit_card', 4), ('PA', 'written_contract', 4),
        ('GA', 'credit_card', 4), ('GA', 'written_contract', 6),
        ('NC', 'credit_card', 3), ('NC', 'written_contract', 3),
        ('MI', 'credit_card', 6), ('MI', 'written_contract', 6),
        # Adding remaining 39 states
        ('AK', 'credit_card', 3), ('AK', 'written_contract', 6),
        ('AZ', 'credit_card', 3), ('AZ', 'written_contract', 6),
        ('AR', 'credit_card', 3), ('AR', 'written_contract', 5),
        ('CO', 'credit_card', 3), ('CO', 'written_contract', 6),
        ('CT', 'credit_card', 3), ('CT', 'written_contract', 6),
        ('DE', 'credit_card', 3), ('DE', 'written_contract', 3),
        ('HI', 'credit_card', 6), ('HI', 'written_contract', 6),
        ('ID', 'credit_card', 4), ('ID', 'written_contract', 5),
        ('IN', 'credit_card', 6), ('IN', 'written_contract', 6),
        ('IA', 'credit_card', 5), ('IA', 'written_contract', 10),
        ('KS', 'credit_card', 3), ('KS', 'written_contract', 5),
        ('KY', 'credit_card', 5), ('KY', 'written_contract', 10),
        ('LA', 'credit_card', 3), ('LA', 'written_contract', 10),
        ('ME', 'credit_card', 6), ('ME', 'written_contract', 6),
        ('MD', 'credit_card', 3), ('MD', 'written_contract', 3),
        ('MA', 'credit_card', 6), ('MA', 'written_contract', 6),
        ('MN', 'credit_card', 6), ('MN', 'written_contract', 6),
        ('MS', 'credit_card', 3), ('MS', 'written_contract', 3),
        ('MO', 'credit_card', 5), ('MO', 'written_contract', 5),
        ('MT', 'credit_card', 3), ('MT', 'written_contract', 8),
        ('NE', 'credit_card', 4), ('NE', 'written_contract', 5),
        ('NV', 'credit_card', 4), ('NV', 'written_contract', 6),
        ('NH', 'credit_card', 3), ('NH', 'written_contract', 3),
        ('NJ', 'credit_card', 6), ('NJ', 'written_contract', 6),
        ('NM', 'credit_card', 4), ('NM', 'written_contract', 6),
        ('ND', 'credit_card', 6), ('ND', 'written_contract', 6),
        ('OK', 'credit_card', 3), ('OK', 'written_contract', 5),
        ('OR', 'credit_card', 6), ('OR', 'written_contract', 6),
        ('RI', 'credit_card', 10), ('RI', 'written_contract', 10),
        ('SC', 'credit_card', 3), ('SC', 'written_contract', 3),
        ('SD', 'credit_card', 6), ('SD', 'written_contract', 6),
        ('TN', 'credit_card', 6), ('TN', 'written_contract', 6),
        ('UT', 'credit_card', 4), ('UT', 'written_contract', 6),
        ('VT', 'credit_card', 3), ('VT', 'written_contract', 6),
        ('VA', 'credit_card', 3), ('VA', 'written_contract', 5),
        ('WA', 'credit_card', 3), ('WA', 'written_contract', 6),
        ('WV', 'credit_card', 5), ('WV', 'written_contract', 10),
        ('WI', 'credit_card', 6), ('WI', 'written_contract', 6),
        ('WY', 'credit_card', 8), ('WY', 'written_contract', 10),
    ]
    
    for state, debt_type, years in sol_data:
        await db.statute_of_limitations.update_one(
            {'state_code': state, 'debt_type': debt_type},
            {'$set': {
                'state_code': state,
                'debt_type': debt_type,
                'years': years,
                'notes': f"Statute of limitations for {debt_type} in {state}",
                'updated_at': datetime.now(timezone.utc)
            }},
            upsert=True
        )
    
    logger.info(f"Seeded {len(sol_data)} SOL entries (50 states)")
    
    # Seed legal rules
    legal_rules = [
        # FDCPA Rules
        {'rule_code': 'FDCPA_809', 'rule_type': 'debt_collection', 'state_code': None,
         'rule_text': 'Debt collector must provide validation within 30 days if requested.',
         'citations': {'statute': '15 U.S.C. § 1692g', 'title': 'FDCPA § 809'},
         'severity': 'low', 'db_version': 'v1.0'},
        {'rule_code': 'FDCPA_805', 'rule_type': 'debt_collection', 'state_code': None,
         'rule_text': 'Debt collector must cease communication if requested in writing.',
         'citations': {'statute': '15 U.S.C. § 1692c', 'title': 'FDCPA § 805'},
         'severity': 'medium', 'db_version': 'v1.0'},
        {'rule_code': 'FDCPA_806', 'rule_type': 'debt_collection', 'state_code': None,
         'rule_text': 'Debt collectors may not harass, oppress, or abuse any person.',
         'citations': {'statute': '15 U.S.C. § 1692d', 'title': 'FDCPA § 806 - Harassment'},
         'severity': 'high', 'db_version': 'v1.0'},
        # FCRA Rules
        {'rule_code': 'FCRA_611', 'rule_type': 'credit_reporting', 'state_code': None,
         'rule_text': 'Credit bureaus must investigate disputes within 30 days.',
         'citations': {'statute': '15 U.S.C. § 1681i', 'title': 'FCRA § 611'},
         'severity': 'low', 'db_version': 'v1.0'},
        {'rule_code': 'FCRA_609', 'rule_type': 'credit_reporting', 'state_code': None,
         'rule_text': 'Consumers have right to obtain all information in their file.',
         'citations': {'statute': '15 U.S.C. § 1681g', 'title': 'FCRA § 609'},
         'severity': 'low', 'db_version': 'v1.0'},
    ]
    
    for rule in legal_rules:
        await db.legal_rules.update_one(
            {'rule_code': rule['rule_code']},
            {'$set': {**rule, 'updated_at': datetime.now(timezone.utc)}},
            upsert=True
        )
    
    logger.info(f"Seeded {len(legal_rules)} legal rules")
