from fastapi import APIRouter, HTTPException, Depends, Query, status
from typing import List, Optional
from database.connection import leads_collection, users_collection
from auth.middleware import get_current_user_data
from models.lead import LeadCreate, LeadUpdate
from bson import ObjectId
from datetime import datetime
import math

router = APIRouter(prefix="/leads", tags=["Leads"])


@router.get("/")
async def get_leads(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    user_data: dict = Depends(get_current_user_data)
):
    """Get paginated leads with optional search and filter."""
    
    # Build query
    query = {}
    
    # Add search filter
    if search:
        query["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"email": {"$regex": search, "$options": "i"}},
            {"phone": {"$regex": search, "$options": "i"}}
        ]
    
    # Add status filter
    if status:
        query["status"] = status
    
    # Role-based access: agents can only see their own leads
    if user_data.get("role") == "agent":
        query["assigned_agent_id"] = user_data.get("user_id")
    
    # Calculate skip value for pagination
    skip = (page - 1) * limit
    
    # Get total count
    total = await leads_collection.count_documents(query)
    
    # Get leads
    cursor = leads_collection.find(query).skip(skip).limit(limit).sort("created_at", -1)
    leads = await cursor.to_list(length=limit)
    
    # Convert ObjectId to string
    for lead in leads:
        lead["id"] = str(lead["_id"])
        del lead["_id"]
        if "assigned_agent_id" in lead and lead["assigned_agent_id"]:
            lead["assigned_agent_id"] = str(lead["assigned_agent_id"])
    
    return {
        "leads": leads,
        "total": total,
        "page": page,
        "pages": math.ceil(total / limit),
        "limit": limit
    }


@router.get("/{lead_id}")
async def get_lead(
    lead_id: str,
    user_data: dict = Depends(get_current_user_data)
):
    """Get a specific lead by ID."""
    
    if not ObjectId.is_valid(lead_id):
        raise HTTPException(status_code=400, detail="Invalid lead ID")
    
    lead = await leads_collection.find_one({"_id": ObjectId(lead_id)})
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    # Role-based access: agents can only see their own leads
    if user_data.get("role") == "agent":
        if str(lead.get("assigned_agent_id")) != user_data.get("user_id"):
            raise HTTPException(status_code=403, detail="Access denied")
    
    # Convert ObjectId to string
    lead["id"] = str(lead["_id"])
    del lead["_id"]
    if "assigned_agent_id" in lead and lead["assigned_agent_id"]:
        lead["assigned_agent_id"] = str(lead["assigned_agent_id"])
    
    return {"lead": lead}


@router.post("/")
async def create_lead(
    lead_data: LeadCreate,
    user_data: dict = Depends(get_current_user_data)
):
    """Create a new lead."""
    
    # Check if email already exists
    existing_lead = await leads_collection.find_one({"email": lead_data.email})
    if existing_lead:
        raise HTTPException(status_code=400, detail="Lead with this email already exists")
    
    # Prepare lead document
    lead_dict = lead_data.dict(by_alias=True)
    lead_dict["created_at"] = datetime.utcnow()
    lead_dict["updated_at"] = datetime.utcnow()
    
    # If no assigned agent specified, assign to current user if they're an agent
    if not lead_dict.get("assigned_agent_id"):
        if user_data.get("role") == "agent":
            lead_dict["assigned_agent_id"] = ObjectId(user_data.get("user_id"))
            lead_dict["assigned_agent"] = user_data.get("name")
        else:
            # For admin, find the first available agent
            agent = await users_collection.find_one({"role": "agent"})
            if agent:
                lead_dict["assigned_agent_id"] = agent["_id"]
                lead_dict["assigned_agent"] = agent["name"]
    
    # Convert assigned_agent_id to ObjectId if it's a string
    if lead_dict.get("assigned_agent_id") and isinstance(lead_dict["assigned_agent_id"], str):
        lead_dict["assigned_agent_id"] = ObjectId(lead_dict["assigned_agent_id"])
    
    # Insert lead
    result = await leads_collection.insert_one(lead_dict)
    
    # Get the created lead
    created_lead = await leads_collection.find_one({"_id": result.inserted_id})
    
    # Convert ObjectId to string
    created_lead["id"] = str(created_lead["_id"])
    del created_lead["_id"]
    if "assigned_agent_id" in created_lead and created_lead["assigned_agent_id"]:
        created_lead["assigned_agent_id"] = str(created_lead["assigned_agent_id"])
    
    return {"lead": created_lead}


@router.put("/{lead_id}")
async def update_lead(
    lead_id: str,
    lead_data: LeadUpdate,
    user_data: dict = Depends(get_current_user_data)
):
    """Update a lead."""
    
    if not ObjectId.is_valid(lead_id):
        raise HTTPException(status_code=400, detail="Invalid lead ID")
    
    # Check if lead exists
    existing_lead = await leads_collection.find_one({"_id": ObjectId(lead_id)})
    if not existing_lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    # Role-based access: agents can only update their own leads
    if user_data.get("role") == "agent":
        if str(existing_lead.get("assigned_agent_id")) != user_data.get("user_id"):
            raise HTTPException(status_code=403, detail="Access denied")
    
    # Prepare update data
    update_dict = lead_data.dict(by_alias=True, exclude_unset=True)
    if update_dict:
        update_dict["updated_at"] = datetime.utcnow()
        
        # Convert assigned_agent_id to ObjectId if it's a string
        if "assigned_agent_id" in update_dict and update_dict["assigned_agent_id"]:
            if isinstance(update_dict["assigned_agent_id"], str):
                update_dict["assigned_agent_id"] = ObjectId(update_dict["assigned_agent_id"])
        
        # Update lead
        await leads_collection.update_one(
            {"_id": ObjectId(lead_id)},
            {"$set": update_dict}
        )
    
    # Get updated lead
    updated_lead = await leads_collection.find_one({"_id": ObjectId(lead_id)})
    
    # Convert ObjectId to string
    updated_lead["id"] = str(updated_lead["_id"])
    del updated_lead["_id"]
    if "assigned_agent_id" in updated_lead and updated_lead["assigned_agent_id"]:
        updated_lead["assigned_agent_id"] = str(updated_lead["assigned_agent_id"])
    
    return {"lead": updated_lead}


@router.delete("/{lead_id}")
async def delete_lead(
    lead_id: str,
    user_data: dict = Depends(get_current_user_data)
):
    """Delete a lead (admin only)."""
    
    # Only admins can delete leads
    if user_data.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    if not ObjectId.is_valid(lead_id):
        raise HTTPException(status_code=400, detail="Invalid lead ID")
    
    # Check if lead exists
    lead = await leads_collection.find_one({"_id": ObjectId(lead_id)})
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    # Delete lead
    await leads_collection.delete_one({"_id": ObjectId(lead_id)})
    
    return {"success": True, "message": "Lead deleted successfully"}