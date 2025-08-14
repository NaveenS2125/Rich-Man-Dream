from datetime import datetime, timedelta
from bson import ObjectId
from auth.jwt_handler import hash_password
from database.connection import (
    users_collection, 
    leads_collection, 
    calls_collection, 
    viewings_collection, 
    sales_collection,
    emails_collection,
    email_templates_collection
)


async def seed_database():
    """Seed the database with initial data."""
    
    # Check if data already exists
    user_count = await users_collection.count_documents({})
    if user_count > 0:
        print("Database already seeded. Skipping...")
        return
    
    print("Seeding database with initial data...")
    
    # Create users
    users_data = [
        {
            "_id": ObjectId("65a1b2c3d4e5f6789abcdef0"),
            "name": "Sarah Johnson",
            "email": "sarah.johnson@richmansdream.com",
            "password": hash_password("password123"),
            "role": "admin",
            "avatar": "https://images.unsplash.com/photo-1494790108755-2616b9997701?w=100&h=100&fit=crop&crop=face",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "_id": ObjectId("65a1b2c3d4e5f6789abcdef1"),
            "name": "Michael Chen",
            "email": "michael.chen@richmansdream.com",
            "password": hash_password("password123"),
            "role": "agent",
            "avatar": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=100&h=100&fit=crop&crop=face",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "_id": ObjectId("65a1b2c3d4e5f6789abcdef2"),
            "name": "Lisa Park",
            "email": "lisa.park@richmansdream.com",
            "password": hash_password("password123"),
            "role": "agent",
            "avatar": "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=100&h=100&fit=crop&crop=face",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
    ]
    
    await users_collection.insert_many(users_data)
    
    # Create leads
    leads_data = [
        {
            "_id": ObjectId("65a1b2c3d4e5f6789abcdef3"),
            "name": "John Williams",
            "email": "john.williams@email.com",
            "phone": "+1 (555) 123-4567",
            "status": "hot",
            "source": "Website",
            "budget": "$850,000",
            "property_type": "Luxury Condo",
            "assigned_agent": "Sarah Johnson",
            "assigned_agent_id": ObjectId("65a1b2c3d4e5f6789abcdef0"),
            "notes": "Interested in downtown luxury condos. Prefers high-rise with city view.",
            "created_at": datetime(2024, 1, 15),
            "updated_at": datetime.utcnow(),
            "last_contact": datetime(2024, 1, 20)
        },
        {
            "_id": ObjectId("65a1b2c3d4e5f6789abcdef4"),
            "name": "Emma Rodriguez",
            "email": "emma.rodriguez@email.com",
            "phone": "+1 (555) 234-5678",
            "status": "warm",
            "source": "Referral",
            "budget": "$1,200,000",
            "property_type": "Single Family Home",
            "assigned_agent": "Michael Chen",
            "assigned_agent_id": ObjectId("65a1b2c3d4e5f6789abcdef1"),
            "notes": "Looking for family home in suburbs. Needs 4+ bedrooms.",
            "created_at": datetime(2024, 1, 12),
            "updated_at": datetime.utcnow(),
            "last_contact": datetime(2024, 1, 19)
        },
        {
            "_id": ObjectId("65a1b2c3d4e5f6789abcdef5"),
            "name": "David Thompson",
            "email": "david.thompson@email.com",
            "phone": "+1 (555) 345-6789",
            "status": "cold",
            "source": "Social Media",
            "budget": "$650,000",
            "property_type": "Townhouse",
            "assigned_agent": "Lisa Park",
            "assigned_agent_id": ObjectId("65a1b2c3d4e5f6789abcdef2"),
            "notes": "First-time buyer. Needs guidance on financing options.",
            "created_at": datetime(2024, 1, 10),
            "updated_at": datetime.utcnow(),
            "last_contact": datetime(2024, 1, 17)
        }
    ]
    
    await leads_collection.insert_many(leads_data)
    
    # Create calls
    calls_data = [
        {
            "lead_id": ObjectId("65a1b2c3d4e5f6789abcdef3"),
            "lead_name": "John Williams",
            "agent": "Sarah Johnson",
            "agent_id": ObjectId("65a1b2c3d4e5f6789abcdef0"),
            "type": "outbound",
            "duration": "12:34",
            "date": "2024-01-20",
            "time": "2:30 PM",
            "status": "completed",
            "notes": "Discussed viewing schedule for luxury condos. Very interested in Skyline Tower.",
            "created_at": datetime(2024, 1, 20)
        },
        {
            "lead_id": ObjectId("65a1b2c3d4e5f6789abcdef4"),
            "lead_name": "Emma Rodriguez",
            "agent": "Michael Chen",
            "agent_id": ObjectId("65a1b2c3d4e5f6789abcdef1"),
            "type": "inbound",
            "duration": "8:15",
            "date": "2024-01-19",
            "time": "10:15 AM",
            "status": "completed",
            "notes": "Called to reschedule viewing. Prefers weekend appointments.",
            "created_at": datetime(2024, 1, 19)
        }
    ]
    
    await calls_collection.insert_many(calls_data)
    
    # Create viewings
    viewings_data = [
        {
            "property": "Skyline Tower #2501",
            "address": "123 Downtown Ave, Suite 2501",
            "date": "2024-01-25",
            "time": "2:00 PM",
            "lead_name": "John Williams",
            "lead_id": ObjectId("65a1b2c3d4e5f6789abcdef3"),
            "agent": "Sarah Johnson",
            "agent_id": ObjectId("65a1b2c3d4e5f6789abcdef0"),
            "status": "scheduled",
            "price": "$850,000",
            "type": "Luxury Condo",
            "created_at": datetime.utcnow()
        }
    ]
    
    await viewings_collection.insert_many(viewings_data)
    
    # Create sales
    sales_data = [
        {
            "lead_id": ObjectId("65a1b2c3d4e5f6789abcdef3"),
            "lead_name": "John Williams",
            "property": "Skyline Tower #2501",
            "agent": "Sarah Johnson",
            "agent_id": ObjectId("65a1b2c3d4e5f6789abcdef0"),
            "stage": "negotiation",
            "value": "$850,000",
            "probability": 75,
            "expected_close": "2024-02-15",
            "created_at": datetime.utcnow(),
            "last_activity": datetime(2024, 1, 20)
        }
    ]
    
    await sales_collection.insert_many(sales_data)
    
    print("Database seeded successfully!")
    print("Demo login credentials:")
    print("- Email: sarah.johnson@richmansdream.com")
    print("- Password: password123")
    print("- Role: admin")