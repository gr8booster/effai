"""
Worker process starter - Run background job workers
Usage: python start_workers.py
"""
import asyncio
import logging
from dotenv import load_dotenv
from pathlib import Path

# Load environment
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

from job_queue import job_queue, register_all_workers

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    """Start all worker processes"""
    logger.info("Starting EEFai background workers...")
    
    # Connect to Redis
    await job_queue.connect()
    
    # Register all workers
    register_all_workers()
    
    # Start workers for each queue
    queues = ['ocr', 'pdf', 'email', 'ai']
    
    tasks = []
    for queue_name in queues:
        task = asyncio.create_task(job_queue.start_worker(queue_name))
        tasks.append(task)
        logger.info(f"Worker spawned for {queue_name} queue")
    
    logger.info(f"All {len(tasks)} workers running. Press Ctrl+C to stop.")
    
    # Run forever
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Workers stopped by user")
    except Exception as e:
        logger.error(f"Worker system crashed: {e}")
