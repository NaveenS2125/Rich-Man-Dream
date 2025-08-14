from fastapi import APIRouter, HTTPException, Depends, Query, BackgroundTasks
from typing import List, Optional
from database.connection import emails_collection, email_templates_collection, leads_collection
from auth.middleware import get_current_user_data
from models.email import EmailCreate, EmailUpdate, EmailTemplateCreate, EmailTemplateUpdate
from bson import ObjectId
from datetime import datetime
import math
import re

router = APIRouter(prefix="/emails", tags=["Emails"])


@router.get("/")
async def get_emails(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    lead_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    direction: Optional[str] = Query(None),
    user_data: dict = Depends(get_current_user_data)
):
    """Get paginated emails with optional filters."""
    
    # Build query
    query = {}
    
    # Add lead filter
    if lead_id:
        if not ObjectId.is_valid(lead_id):
            raise HTTPException(status_code=400, detail="Invalid lead ID")
        query["lead_id"] = ObjectId(lead_id)
    
    # Add status filter
    if status:
        query["status"] = status
    
    # Add direction filter
    if direction:
        query["direction"] = direction
    
    # Role-based access: agents can only see their own emails
    if user_data.get("role") == "agent":
        query["agent_id"] = ObjectId(user_data.get("user_id"))
    
    # Calculate skip value for pagination
    skip = (page - 1) * limit
    
    # Get total count
    total = await emails_collection.count_documents(query)
    
    # Get emails
    cursor = emails_collection.find(query).skip(skip).limit(limit).sort("created_at", -1)
    emails = await cursor.to_list(length=limit)
    
    # Convert ObjectIds to strings
    for email in emails:
        email["id"] = str(email["_id"])
        del email["_id"]
        if "lead_id" in email and email["lead_id"]:
            email["lead_id"] = str(email["lead_id"])
        if "agent_id" in email and email["agent_id"]:
            email["agent_id"] = str(email["agent_id"])
    
    return {
        "emails": emails,
        "total": total,
        "page": page,
        "pages": math.ceil(total / limit),
        "limit": limit
    }


@router.get("/{email_id}")
async def get_email(
    email_id: str,
    user_data: dict = Depends(get_current_user_data)
):
    """Get a specific email by ID."""
    
    if not ObjectId.is_valid(email_id):
        raise HTTPException(status_code=400, detail="Invalid email ID")
    
    email = await emails_collection.find_one({"_id": ObjectId(email_id)})
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
    
    # Role-based access: agents can only see their own emails
    if user_data.get("role") == "agent":
        if str(email.get("agent_id")) != user_data.get("user_id"):
            raise HTTPException(status_code=403, detail="Access denied")
    
    # Convert ObjectIds to strings
    email["id"] = str(email["_id"])
    del email["_id"]
    if "lead_id" in email and email["lead_id"]:
        email["lead_id"] = str(email["lead_id"])
    if "agent_id" in email and email["agent_id"]:
        email["agent_id"] = str(email["agent_id"])
    
    return {"email": email}


@router.post("/")
async def create_email(
    email_data: EmailCreate,
    background_tasks: BackgroundTasks,
    user_data: dict = Depends(get_current_user_data)
):
    """Create a new email."""
    
    # Verify lead exists if lead_id is provided
    if email_data.lead_id:
        lead_id = email_data.lead_id
        if isinstance(lead_id, str):
            lead_id = ObjectId(lead_id)
        
        lead = await leads_collection.find_one({"_id": lead_id})
        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found")
    
    # Prepare email document
    email_dict = email_data.dict(by_alias=True)
    email_dict["created_at"] = datetime.utcnow()
    email_dict["updated_at"] = datetime.utcnow()
    
    # Set agent info from current user if not provided
    if not email_dict.get("agent_id"):
        email_dict["agent_id"] = ObjectId(user_data.get("user_id"))
        email_dict["agent_name"] = user_data.get("name")
    
    # Convert string IDs to ObjectIds
    if email_dict.get("lead_id") and isinstance(email_dict["lead_id"], str):
        email_dict["lead_id"] = ObjectId(email_dict["lead_id"])
    if isinstance(email_dict.get("agent_id"), str):
        email_dict["agent_id"] = ObjectId(email_dict["agent_id"])
    
    # Insert email
    result = await emails_collection.insert_one(email_dict)
    
    # If email is marked to be sent, add to background task
    if email_dict.get("status") == "sent":
        background_tasks.add_task(send_email_task, str(result.inserted_id))
    
    # Get the created email
    created_email = await emails_collection.find_one({"_id": result.inserted_id})
    
    # Convert ObjectIds to strings
    created_email["id"] = str(created_email["_id"])
    del created_email["_id"]
    if "lead_id" in created_email and created_email["lead_id"]:
        created_email["lead_id"] = str(created_email["lead_id"])
    if "agent_id" in created_email and created_email["agent_id"]:
        created_email["agent_id"] = str(created_email["agent_id"])
    
    return {"email": created_email}


@router.put("/{email_id}")
async def update_email(
    email_id: str,
    email_data: EmailUpdate,
    user_data: dict = Depends(get_current_user_data)
):
    """Update an email."""
    
    if not ObjectId.is_valid(email_id):
        raise HTTPException(status_code=400, detail="Invalid email ID")
    
    # Check if email exists
    existing_email = await emails_collection.find_one({"_id": ObjectId(email_id)})
    if not existing_email:
        raise HTTPException(status_code=404, detail="Email not found")
    
    # Role-based access: agents can only update their own emails
    if user_data.get("role") == "agent":
        if str(existing_email.get("agent_id")) != user_data.get("user_id"):
            raise HTTPException(status_code=403, detail="Access denied")
    
    # Prepare update data
    update_dict = email_data.dict(by_alias=True, exclude_unset=True)
    if update_dict:
        update_dict["updated_at"] = datetime.utcnow()
        
        # Convert string IDs to ObjectIds
        if "lead_id" in update_dict and update_dict["lead_id"] and isinstance(update_dict["lead_id"], str):
            update_dict["lead_id"] = ObjectId(update_dict["lead_id"])
        if "agent_id" in update_dict and update_dict["agent_id"] and isinstance(update_dict["agent_id"], str):
            update_dict["agent_id"] = ObjectId(update_dict["agent_id"])
        
        # Update email
        await emails_collection.update_one(
            {"_id": ObjectId(email_id)},
            {"$set": update_dict}
        )
    
    # Get updated email
    updated_email = await emails_collection.find_one({"_id": ObjectId(email_id)})
    
    # Convert ObjectIds to strings
    updated_email["id"] = str(updated_email["_id"])
    del updated_email["_id"]
    if "lead_id" in updated_email and updated_email["lead_id"]:
        updated_email["lead_id"] = str(updated_email["lead_id"])
    if "agent_id" in updated_email and updated_email["agent_id"]:
        updated_email["agent_id"] = str(updated_email["agent_id"])
    
    return {"email": updated_email}


@router.delete("/{email_id}")
async def delete_email(
    email_id: str,
    user_data: dict = Depends(get_current_user_data)
):
    """Delete an email (admin only)."""
    
    # Only admins can delete emails
    if user_data.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    if not ObjectId.is_valid(email_id):
        raise HTTPException(status_code=400, detail="Invalid email ID")
    
    # Check if email exists
    email = await emails_collection.find_one({"_id": ObjectId(email_id)})
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
    
    # Delete email
    await emails_collection.delete_one({"_id": ObjectId(email_id)})
    
    return {"success": True, "message": "Email deleted successfully"}


# Email Templates Endpoints
@router.get("/templates/")
async def get_email_templates(
    user_data: dict = Depends(get_current_user_data)
):
    """Get all email templates."""
    
    # Get active templates
    cursor = email_templates_collection.find({"is_active": True}).sort("created_at", -1)
    templates = await cursor.to_list(length=100)
    
    # Convert ObjectIds to strings
    for template in templates:
        template["id"] = str(template["_id"])
        del template["_id"]
    
    return {"templates": templates}


@router.post("/templates/")
async def create_email_template(
    template_data: EmailTemplateCreate,
    user_data: dict = Depends(get_current_user_data)
):
    """Create a new email template (admin only)."""
    
    # Only admins can create templates
    if user_data.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    # Prepare template document
    template_dict = template_data.dict(by_alias=True)
    template_dict["created_at"] = datetime.utcnow()
    template_dict["updated_at"] = datetime.utcnow()
    
    # Insert template
    result = await email_templates_collection.insert_one(template_dict)
    
    # Get the created template
    created_template = await email_templates_collection.find_one({"_id": result.inserted_id})
    
    # Convert ObjectIds to strings
    created_template["id"] = str(created_template["_id"])
    del created_template["_id"]
    
    return {"template": created_template}


@router.post("/send-template/")
async def send_template_email(
    template_id: str,
    lead_id: str,
    background_tasks: BackgroundTasks,
    user_data: dict = Depends(get_current_user_data)
):
    """Send an email using a template."""
    
    # Verify template exists
    if not ObjectId.is_valid(template_id):
        raise HTTPException(status_code=400, detail="Invalid template ID")
    
    template = await email_templates_collection.find_one({"_id": ObjectId(template_id)})
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    # Verify lead exists
    if not ObjectId.is_valid(lead_id):
        raise HTTPException(status_code=400, detail="Invalid lead ID")
    
    lead = await leads_collection.find_one({"_id": ObjectId(lead_id)})
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    # Replace template variables
    subject = replace_template_variables(template["subject"], lead, user_data)
    content = replace_template_variables(template["content"], lead, user_data)
    
    # Create email from template
    email_dict = {
        "lead_id": ObjectId(lead_id),
        "lead_name": lead["name"],
        "to_email": lead["email"],
        "from_email": user_data.get("email", "noreply@richmansdream.com"),
        "subject": subject,
        "content": content,
        "email_type": "template",
        "template_id": str(template_id),
        "status": "sent",
        "direction": "outbound",
        "agent_id": ObjectId(user_data.get("user_id")),
        "agent_name": user_data.get("name"),
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "sent_at": datetime.utcnow()
    }
    
    # Insert email
    result = await emails_collection.insert_one(email_dict)
    
    # Add to background task for actual sending
    background_tasks.add_task(send_email_task, str(result.inserted_id))
    
    return {"success": True, "message": "Template email queued for sending", "email_id": str(result.inserted_id)}


def replace_template_variables(content: str, lead: dict, user_data: dict) -> str:
    """Replace template variables with actual values."""
    
    variables = {
        "{lead_name}": lead.get("name", ""),
        "{lead_email}": lead.get("email", ""),
        "{lead_phone}": lead.get("phone", ""),
        "{lead_budget}": lead.get("budget", ""),
        "{property_type}": lead.get("property_type", ""),
        "{agent_name}": user_data.get("name", ""),
        "{agent_email}": user_data.get("email", ""),
        "{company_name}": "Rich Man Dream",
        "{date}": datetime.now().strftime("%B %d, %Y"),
        "{time}": datetime.now().strftime("%I:%M %p")
    }
    
    for variable, value in variables.items():
        content = content.replace(variable, str(value))
    
    return content


async def send_email_task(email_id: str):
    """Background task to simulate email sending."""
    
    # In a real implementation, this would integrate with an email service like SendGrid
    # For now, we'll just update the email status to "delivered"
    
    try:
        await emails_collection.update_one(
            {"_id": ObjectId(email_id)},
            {
                "$set": {
                    "status": "delivered",
                    "updated_at": datetime.utcnow()
                }
            }
        )
        print(f"Email {email_id} marked as delivered")
    except Exception as e:
        # Mark as failed if there's an error
        await emails_collection.update_one(
            {"_id": ObjectId(email_id)},
            {
                "$set": {
                    "status": "failed",
                    "updated_at": datetime.utcnow()
                }
            }
        )
        print(f"Email {email_id} marked as failed: {str(e)}")


# Notification Triggers
@router.post("/triggers/new-lead")
async def trigger_new_lead_email(
    lead_id: str,
    background_tasks: BackgroundTasks,
    user_data: dict = Depends(get_current_user_data)
):
    """Trigger welcome email for new lead."""
    
    # Find welcome email template
    template = await email_templates_collection.find_one({"template_type": "welcome", "is_active": True})
    if template:
        await send_template_email(str(template["_id"]), lead_id, background_tasks, user_data)
        return {"success": True, "message": "Welcome email triggered"}
    
    return {"success": False, "message": "No welcome template found"}


@router.post("/triggers/viewing-reminder")
async def trigger_viewing_reminder_email(
    viewing_id: str,
    background_tasks: BackgroundTasks,
    user_data: dict = Depends(get_current_user_data)
):
    """Trigger viewing reminder email."""
    
    # This would integrate with the viewings system
    # For now, return success
    return {"success": True, "message": "Viewing reminder email triggered"}