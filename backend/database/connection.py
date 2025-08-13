import os
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure
import logging

logger = logging.getLogger(__name__)

# Database connection
mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
database_name = os.environ.get('DB_NAME', 'richmansdream_db')

client = AsyncIOMotorClient(mongo_url)
database = client[database_name]


async def ping_database():
    """Test database connection."""
    try:
        await client.admin.command('ping')
        logger.info(f"Connected to MongoDB at {mongo_url}")
        return True
    except ConnectionFailure:
        logger.error(f"Failed to connect to MongoDB at {mongo_url}")
        return False


# Collection references
users_collection = database.users
leads_collection = database.leads
calls_collection = database.calls
viewings_collection = database.viewings
sales_collection = database.sales


async def create_indexes():
    """Create database indexes for better performance."""
    # User indexes
    await users_collection.create_index("email", unique=True)
    
    # Lead indexes
    await leads_collection.create_index("email")
    await leads_collection.create_index("status")
    await leads_collection.create_index("assigned_agent_id")
    await leads_collection.create_index("created_at")
    
    # Call indexes
    await calls_collection.create_index("lead_id")
    await calls_collection.create_index("agent_id")
    await calls_collection.create_index("date")
    
    # Viewing indexes
    await viewings_collection.create_index("lead_id")
    await viewings_collection.create_index("agent_id")
    await viewings_collection.create_index("date")
    await viewings_collection.create_index("status")
    
    # Sale indexes
    await sales_collection.create_index("lead_id")
    await sales_collection.create_index("agent_id")
    await sales_collection.create_index("stage")
    await sales_collection.create_index("expected_close")
    
    logger.info("Database indexes created successfully")


async def close_database_connection():
    """Close database connection."""
    client.close()
    logger.info("Database connection closed")