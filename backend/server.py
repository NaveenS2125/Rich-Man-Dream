from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
import os
import logging
from pathlib import Path
from contextlib import asynccontextmanager
import sys

# Add the backend directory to Python path
sys.path.append(str(Path(__file__).parent))

# Import routes
from routes.auth import router as auth_router
from routes.leads import router as leads_router
from routes.calls import router as calls_router
from routes.viewings import router as viewings_router
from routes.sales import router as sales_router
from routes.dashboard import router as dashboard_router

# Import database and utilities
from database.connection import ping_database, create_indexes, close_database_connection
from utils.seed_data import seed_database

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application startup and shutdown."""
    # Startup
    logger.info("Starting Rich Man Dream CRM Backend...")
    
    # Test database connection
    if await ping_database():
        logger.info("Database connection successful")
        
        # Create indexes
        await create_indexes()
        
        # Seed database with initial data
        await seed_database()
    else:
        logger.error("Failed to connect to database")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Rich Man Dream CRM Backend...")
    await close_database_connection()


# Create the main app with lifespan events
app = FastAPI(
    title="Rich Man Dream CRM API",
    description="Premium Real Estate CRM Backend",
    version="1.0.0",
    lifespan=lifespan
)

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# Health check endpoint
@api_router.get("/")
async def root():
    return {
        "message": "Rich Man Dream CRM API is running!",
        "status": "healthy",
        "version": "1.0.0"
    }


@api_router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "Rich Man Dream CRM API",
        "database": "connected"
    }


# Include all routes
api_router.include_router(auth_router)
api_router.include_router(leads_router)
api_router.include_router(calls_router)
api_router.include_router(viewings_router)
api_router.include_router(sales_router)
api_router.include_router(dashboard_router)

# Include the API router in the main app
app.include_router(api_router)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],  # In production, specify actual origins
    allow_methods=["*"],
    allow_headers=["*"],
)
