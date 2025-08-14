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
    
    # Create email templates
    email_templates_data = [
        {
            "name": "Welcome New Lead",
            "subject": "Welcome to Rich Man Dream - Let's Find Your Perfect Property!",
            "content": """Dear {lead_name},

Welcome to Rich Man Dream! We're thrilled to help you find your perfect property.

I'm {agent_name}, your dedicated real estate agent. I understand you're looking for a {property_type} with a budget of {lead_budget}. Our team specializes in luxury properties and we're confident we can find exactly what you're looking for.

What's next:
- I'll be calling you within 24 hours to discuss your requirements in detail
- We'll schedule property viewings that match your criteria
- I'll provide you with exclusive market insights and opportunities

Feel free to reach out to me directly at {agent_email} if you have any questions.

Looking forward to helping you achieve your real estate dreams!

Best regards,
{agent_name}
Rich Man Dream Real Estate

Phone: (555) 123-RICH
Website: www.richmansdream.com""",
            "template_type": "welcome",
            "variables": ["{lead_name}", "{agent_name}", "{property_type}", "{lead_budget}", "{agent_email}"],
            "is_active": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "name": "Viewing Reminder",
            "subject": "Reminder: Property Viewing Tomorrow at {time}",
            "content": """Dear {lead_name},

This is a friendly reminder about your property viewing scheduled for tomorrow.

Viewing Details:
- Property: {property_name}
- Date: {date}
- Time: {time}
- Address: {property_address}
- Your Agent: {agent_name}

Please arrive 5 minutes early. If you need to reschedule or have any questions, please call me at {agent_phone}.

Looking forward to showing you this amazing property!

Best regards,
{agent_name}
Rich Man Dream Real Estate""",
            "template_type": "viewing_reminder",
            "variables": ["{lead_name}", "{property_name}", "{date}", "{time}", "{property_address}", "{agent_name}", "{agent_phone}"],
            "is_active": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "name": "Sale Progress Update",
            "subject": "Update on Your Property Purchase - {property_name}",
            "content": """Dear {lead_name},

I wanted to give you an update on the progress of your property purchase.

Property: {property_name}
Current Stage: {sale_stage}
Expected Closing: {expected_close}

Recent developments:
- All documentation is progressing smoothly
- We're on track for the expected closing date
- I'll keep you updated on any new developments

If you have any questions or concerns, please don't hesitate to reach out to me directly.

Best regards,
{agent_name}
Rich Man Dream Real Estate

Phone: {agent_phone}
Email: {agent_email}""",
            "template_type": "sale_update",
            "variables": ["{lead_name}", "{property_name}", "{sale_stage}", "{expected_close}", "{agent_name}", "{agent_phone}", "{agent_email}"],
            "is_active": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "name": "Follow Up",
            "subject": "Following Up - Still Looking for Your Perfect Property?",
            "content": """Dear {lead_name},

I hope this email finds you well! It's been a while since we last spoke, and I wanted to follow up on your property search.

I remember you were looking for a {property_type} with a budget of {lead_budget}. The market has some exciting new opportunities that might interest you.

Recent developments in your area:
- New luxury properties have come on the market
- Interest rates remain favorable for buyers
- We've had several successful closings in your price range

Would you like to schedule a call this week to discuss the current market and see some new options?

You can reach me directly at {agent_email} or {agent_phone}.

Best regards,
{agent_name}
Rich Man Dream Real Estate""",
            "template_type": "follow_up",
            "variables": ["{lead_name}", "{property_type}", "{lead_budget}", "{agent_name}", "{agent_email}", "{agent_phone}"],
            "is_active": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
    ]
    
    await email_templates_collection.insert_many(email_templates_data)
    
    # Create sample emails
    emails_data = [
        {
            "lead_id": ObjectId("65a1b2c3d4e5f6789abcdef3"),
            "lead_name": "John Williams",
            "to_email": "john.williams@email.com",
            "from_email": "sarah.johnson@richmansdream.com",
            "subject": "Re: Skyline Tower Viewing",
            "content": "Thank you for showing me the property. I'm very interested in moving forward with the purchase. Could we schedule a call to discuss the next steps?",
            "email_type": "manual",
            "status": "read",
            "direction": "inbound",
            "agent_id": ObjectId("65a1b2c3d4e5f6789abcdef0"),
            "agent_name": "Sarah Johnson",
            "created_at": datetime(2024, 1, 20, 15, 45),
            "updated_at": datetime(2024, 1, 20, 15, 45),
            "sent_at": datetime(2024, 1, 20, 15, 45)
        },
        {
            "lead_id": ObjectId("65a1b2c3d4e5f6789abcdef4"),
            "lead_name": "Emma Rodriguez",
            "to_email": "emma.rodriguez@email.com",
            "from_email": "michael.chen@richmansdream.com",
            "subject": "Welcome to Rich Man Dream!",
            "content": "Welcome! I'm excited to help you find your perfect family home. I'll be calling you tomorrow to discuss your requirements in detail.",
            "email_type": "template",
            "status": "delivered",
            "direction": "outbound",
            "agent_id": ObjectId("65a1b2c3d4e5f6789abcdef1"),
            "agent_name": "Michael Chen",
            "created_at": datetime(2024, 1, 19, 11, 30),
            "updated_at": datetime(2024, 1, 19, 11, 30),
            "sent_at": datetime(2024, 1, 19, 11, 30)
        }
    ]
    
    await emails_collection.insert_many(emails_data)
    
    print("Database seeded successfully!")
    print("Demo login credentials:")
    print("- Email: sarah.johnson@richmansdream.com")
    print("- Password: password123")
    print("- Role: admin")