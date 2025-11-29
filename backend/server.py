from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
import os
import logging
from pathlib import Path
from contextlib import asynccontextmanager

# Load environment variables FIRST
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Import database connections
from database import init_databases, close_databases

# Import security middleware
from security_middleware import SecurityHeadersMiddleware, RateLimitMiddleware

# Import all agent routers
from agents import orchestrator, legal, cfp, writer, intake, eefai, mentor, support, audit, static_routes, credit, auth, admin_stats

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown"""
    # Startup
    logger.info("Initializing EEFai platform...")
    await init_databases()
    logger.info("All databases connected")
    
    # Initialize event bus
    from event_bus import event_bus, register_event_handlers
    register_event_handlers()
    logger.info("Event bus initialized")
    
    # Initialize job queue
    from job_queue import job_queue, register_all_workers
    await job_queue.connect()
    register_all_workers()
    logger.info("Job queue initialized")
    
    yield
    
    # Shutdown
    logger.info("Shutting down EEFai platform...")
    await close_databases()
    logger.info("All databases closed")


# Create the main app with lifespan
app = FastAPI(
    title="EEFai Platform API",
    description="Emergency Expense Friend AI - Complete financial assistance platform",
    version="1.0.0",
    lifespan=lifespan
)

# Create main API router
api_router = APIRouter(prefix="/api")

# Health check endpoint
@api_router.get("/")
async def root():
    return {
        "message": "EEFai Platform API",
        "version": "1.0.0",
        "status": "running",
        "agents": [
            "OrchestratorAI",
            "EEFai",
            "IntakeAgent",
            "LegalAI",
            "CFP-AI",
            "WriterAgent",
            "MentorAgent",
            "SupportAgent",
            "AuditAgent"
        ]
    }

# Include all agent routers (without /api prefix since api_router already has it)
app.include_router(orchestrator.router, prefix="", tags=["orchestrator"])
app.include_router(legal.router, prefix="", tags=["legal"])
app.include_router(cfp.router, prefix="", tags=["cfp"])
app.include_router(writer.router, prefix="", tags=["writer"])
app.include_router(intake.router, prefix="", tags=["intake"])
app.include_router(eefai.router, prefix="", tags=["eefai"])
app.include_router(mentor.router, prefix="", tags=["mentor"])
app.include_router(support.router, prefix="", tags=["support"])
app.include_router(audit.router, prefix="", tags=["audit"])
app.include_router(static_routes.router, prefix="", tags=["static"])
app.include_router(credit.router, prefix="", tags=["credit"])
app.include_router(auth.router, prefix="", tags=["auth"])

# Include main API router
app.include_router(api_router)

# Add security middleware
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RateLimitMiddleware, max_requests=60, window_seconds=60)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info("EEFai server configured successfully")
