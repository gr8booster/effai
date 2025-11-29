"""Database connections and utilities for tri-database architecture"""
import os
from motor.motor_asyncio import AsyncIOMotorClient
import asyncpg
import redis.asyncio as aioredis
from typing import Optional
import logging

logger = logging.getLogger(__name__)

# MongoDB Connection
mongo_client: Optional[AsyncIOMotorClient] = None
mongo_db = None

# PostgreSQL Connection Pool
pg_pool: Optional[asyncpg.Pool] = None

# Redis Connection
redis_client: Optional[aioredis.Redis] = None


async def init_databases():
    """Initialize all three databases"""
    global mongo_client, mongo_db, pg_pool, redis_client
    
    # MongoDB
    mongo_url = os.environ['MONGO_URL']
    mongo_client = AsyncIOMotorClient(mongo_url)
    mongo_db = mongo_client[os.environ['DB_NAME']]
    logger.info("MongoDB connected")
    
    # PostgreSQL
    pg_dsn = f"postgresql://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@{os.environ['POSTGRES_HOST']}:{os.environ['POSTGRES_PORT']}/{os.environ['POSTGRES_DB']}"
    pg_pool = await asyncpg.create_pool(pg_dsn, min_size=5, max_size=20)
    logger.info("PostgreSQL pool created")
    
    # Redis
    redis_client = await aioredis.from_url(
        f"redis://{os.environ['REDIS_HOST']}:{os.environ['REDIS_PORT']}/{os.environ['REDIS_DB']}",
        encoding="utf-8",
        decode_responses=True
    )
    logger.info("Redis connected")
    
    # Create PostgreSQL tables
    await init_pg_schema()


async def init_pg_schema():
    """Initialize PostgreSQL schema for legal templates, audit logs, etc."""
    async with pg_pool.acquire() as conn:
        # Legal templates table
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS legal_templates (
                id SERIAL PRIMARY KEY,
                template_id VARCHAR(255) UNIQUE NOT NULL,
                template_version VARCHAR(50) NOT NULL,
                template_type VARCHAR(100) NOT NULL,
                template_html TEXT NOT NULL,
                template_json JSONB NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Legal rules table
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS legal_rules (
                id SERIAL PRIMARY KEY,
                rule_code VARCHAR(100) UNIQUE NOT NULL,
                rule_type VARCHAR(50) NOT NULL,
                state_code VARCHAR(2),
                rule_text TEXT NOT NULL,
                citations JSONB NOT NULL,
                severity VARCHAR(20) NOT NULL,
                db_version VARCHAR(20) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # CFP golden vectors (test cases)
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS cfp_golden_vectors (
                id SERIAL PRIMARY KEY,
                vector_id VARCHAR(255) UNIQUE NOT NULL,
                scenario_type VARCHAR(100) NOT NULL,
                input_data JSONB NOT NULL,
                expected_output JSONB NOT NULL,
                checksum VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Audit log (immutable provenance)
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS audit_log (
                id SERIAL PRIMARY KEY,
                provenance_id VARCHAR(255) UNIQUE NOT NULL,
                agent_id VARCHAR(100) NOT NULL,
                agent_version VARCHAR(50) NOT NULL,
                input_hash VARCHAR(255) NOT NULL,
                output_hash VARCHAR(255) NOT NULL,
                s3_input_path VARCHAR(500),
                s3_output_path VARCHAR(500),
                db_refs JSONB,
                legal_db_version VARCHAR(50),
                cfp_version VARCHAR(50),
                timestamp TIMESTAMP NOT NULL,
                human_reviewed BOOLEAN DEFAULT FALSE,
                hmac_signature VARCHAR(500) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # State statute of limitations table
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS statute_of_limitations (
                id SERIAL PRIMARY KEY,
                state_code VARCHAR(2) NOT NULL,
                debt_type VARCHAR(100) NOT NULL,
                years INT NOT NULL,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(state_code, debt_type)
            )
        """)
        
        logger.info("PostgreSQL schema initialized")


async def close_databases():
    """Close all database connections"""
    global mongo_client, pg_pool, redis_client
    
    if mongo_client:
        mongo_client.close()
    
    if pg_pool:
        await pg_pool.close()
    
    if redis_client:
        await redis_client.close()
    
    logger.info("All databases closed")


def get_mongo_db():
    """Get MongoDB database instance"""
    return mongo_db


def get_pg_pool():
    """Get PostgreSQL connection pool"""
    return pg_pool


def get_redis():
    """Get Redis client"""
    return redis_client
