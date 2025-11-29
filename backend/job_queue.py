"""
Redis Job Queue System - Background workers for async processing
Handles: OCR, PDF generation, AI calls, emails, notifications
"""
import asyncio
import json
import logging
from typing import Any, Callable
from datetime import datetime, timezone
import redis.asyncio as aioredis
import os

logger = logging.getLogger(__name__)

REDIS_URL = f"redis://{os.getenv('REDIS_HOST', 'localhost')}:{os.getenv('REDIS_PORT', '6379')}/{os.getenv('REDIS_DB', '0')}"


class JobQueue:
    """Async job queue using Redis"""
    
    def __init__(self):
        self.redis = None
        self.workers = {}
    
    async def connect(self):
        """Connect to Redis"""
        try:
            self.redis = await aioredis.from_url(REDIS_URL, encoding="utf-8", decode_responses=True)
            logger.info("Job queue connected to Redis")
        except Exception as e:
            logger.warning(f"Redis unavailable: {e}. Job queue disabled.")
            self.redis = None
    
    async def enqueue(self, queue_name: str, job_data: dict, priority: int = 0):
        """
        Enqueue job for background processing
        
        Args:
            queue_name: Queue name (e.g., 'ocr', 'pdf', 'email')
            job_data: Job payload
            priority: Priority (higher = more urgent)
        """
        if not self.redis:
            logger.warning(f"Job queue unavailable, executing synchronously: {queue_name}")
            return None
        
        job = {
            "id": f"{queue_name}_{datetime.now().timestamp()}",
            "queue": queue_name,
            "data": job_data,
            "priority": priority,
            "enqueued_at": datetime.now(timezone.utc).isoformat(),
            "status": "pending"
        }
        
        # Add to Redis list with priority
        await self.redis.zadd(f"queue:{queue_name}", {json.dumps(job): priority})
        
        logger.info(f"Job enqueued: {job['id']} on {queue_name}")
        return job["id"]
    
    async def dequeue(self, queue_name: str, timeout: int = 5):
        """Dequeue next job from queue"""
        if not self.redis:
            return None
        
        # Pop highest priority job
        result = await self.redis.zpopmax(f"queue:{queue_name}", 1)
        if not result:
            return None
        
        job_json, priority = result[0]
        job = json.loads(job_json)
        return job
    
    def register_worker(self, queue_name: str, handler: Callable):
        """Register a worker function for a queue"""
        self.workers[queue_name] = handler
        logger.info(f"Worker registered for queue: {queue_name}")
    
    async def start_worker(self, queue_name: str):
        """Start processing jobs from queue"""
        if queue_name not in self.workers:
            raise ValueError(f"No worker registered for {queue_name}")
        
        handler = self.workers[queue_name]
        
        logger.info(f"Worker started for {queue_name}")
        
        while True:
            try:
                job = await self.dequeue(queue_name, timeout=5)
                
                if job:
                    logger.info(f"Processing job: {job['id']}")
                    
                    try:
                        # Execute handler
                        result = await handler(job['data'])
                        logger.info(f"Job completed: {job['id']}")
                    except Exception as e:
                        logger.error(f"Job failed: {job['id']} - {e}")
                        # Re-queue with lower priority for retry
                        job['retry_count'] = job.get('retry_count', 0) + 1
                        if job['retry_count'] < 3:
                            await self.enqueue(queue_name, job['data'], priority=job['priority'] - 10)
                else:
                    # No jobs, wait a bit
                    await asyncio.sleep(1)
                    
            except Exception as e:
                logger.error(f"Worker error: {e}")
                await asyncio.sleep(5)


# Global job queue instance
job_queue = JobQueue()


# Example worker handlers
async def ocr_worker(job_data: dict):
    """Worker for OCR processing"""
    from agents.intake import perform_ocr
    
    file_content = job_data['file_content']
    filename = job_data['filename']
    
    text = perform_ocr(file_content, filename)
    
    # Store result
    from database import get_mongo_db
    db = get_mongo_db()
    await db.ocr_results.insert_one({
        "doc_id": job_data['doc_id'],
        "text": text,
        "processed_at": datetime.now(timezone.utc).isoformat()
    })
    
    return {"status": "completed", "doc_id": job_data['doc_id']}


async def pdf_worker(job_data: dict):
    """Worker for PDF generation"""
    # PDF generation logic here
    return {"status": "completed"}


async def email_worker(job_data: dict):
    """Worker for email sending"""
    # Email sending logic here
    return {"status": "completed"}


async def ai_worker(job_data: dict):
    """Worker for AI processing"""
    from ai_utils import AIProvider
    
    provider = AIProvider()
    result = await provider.generate(
        job_data['system_message'],
        job_data['user_message'],
        job_data.get('session_id', 'worker')
    )
    
    return {"status": "completed", "result": result}


def register_all_workers():
    """Register all worker handlers"""
    job_queue.register_worker('ocr', ocr_worker)
    job_queue.register_worker('pdf', pdf_worker)
    job_queue.register_worker('email', email_worker)
    job_queue.register_worker('ai', ai_worker)
    logger.info("All workers registered")
