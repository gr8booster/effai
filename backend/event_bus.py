"""
Event-Driven System - Pub/Sub for async workflows
Replaces synchronous linear flows with reactive event processing
"""
import asyncio
from typing import Callable, Dict, List
from datetime import datetime, timezone
import logging
from database import get_mongo_db
from job_queue import job_queue

logger = logging.getLogger(__name__)


class EventBus:
    """Central event bus for pub/sub architecture"""
    
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}
    
    def subscribe(self, event_type: str, handler: Callable):
        """Subscribe to event"""
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(handler)
        logger.info(f"Subscribed to event: {event_type}")
    
    async def publish(self, event_type: str, event_data: dict):
        """Publish event to all subscribers"""
        event = {
            "type": event_type,
            "data": event_data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_id": f"{event_type}_{datetime.now().timestamp()}"
        }
        
        # Log event
        db = get_mongo_db()
        await db.events.insert_one(event)
        
        # Trigger all subscribers
        if event_type in self.subscribers:
            for handler in self.subscribers[event_type]:
                try:
                    # Execute async or enqueue as job
                    if asyncio.iscoroutinefunction(handler):
                        await handler(event_data)
                    else:
                        # Enqueue as background job
                        await job_queue.enqueue('events', {
                            "handler": handler.__name__,
                            "event_data": event_data
                        })
                except Exception as e:
                    logger.error(f"Event handler failed: {e}")
        
        logger.info(f"Event published: {event_type}")
        return event["event_id"]


# Global event bus
event_bus = EventBus()


# Event Handlers
async def on_user_registered(data: dict):
    """Handle user.registered event"""
    user_id = data['user_id']
    logger.info(f"Event: User registered - {user_id}")
    # Create EEFai instance, send welcome email, etc.


async def on_document_uploaded(data: dict):
    """Handle document.uploaded event"""
    doc_id = data['doc_id']
    # Trigger OCR job
    await job_queue.enqueue('ocr', data)
    logger.info(f"Event: Document uploaded - {doc_id}, OCR job queued")


async def on_ocr_completed(data: dict):
    """Handle ocr.completed event"""
    doc_id = data['doc_id']
    # Extract fields, run legal analysis
    logger.info(f"Event: OCR completed - {doc_id}")


async def on_letter_generated(data: dict):
    """Handle letter.generated event"""
    # Log to audit, notify user
    logger.info(f"Event: Letter generated")


async def on_task_completed(data: dict):
    """Handle task.completed event"""
    # Update streak, check milestones
    logger.info(f"Event: Task completed")


async def on_lesson_completed(data: dict):
    """Handle lesson.completed event"""
    # Award points, unlock next lesson
    logger.info(f"Event: Lesson completed")


def register_event_handlers():
    """Register all event handlers"""
    event_bus.subscribe('user.registered', on_user_registered)
    event_bus.subscribe('document.uploaded', on_document_uploaded)
    event_bus.subscribe('ocr.completed', on_ocr_completed)
    event_bus.subscribe('letter.generated', on_letter_generated)
    event_bus.subscribe('task.completed', on_task_completed)
    event_bus.subscribe('lesson.completed', on_lesson_completed)
    logger.info("All event handlers registered")
