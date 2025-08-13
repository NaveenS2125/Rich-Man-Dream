from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from database.connection import calls_collection, leads_collection
from auth.middleware import get_current_user_data
from models.call import CallCreate, CallUpdate
from bson import ObjectId
from datetime import datetime
import math

router = APIRouter(prefix="/calls", tags=["Calls"])


@router.get("/")
async def get_calls(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    lead_id: Optional[str] = Query(None),
    agent: Optional[str] = Query(None),
    user_data: dict = Depends(get_current_user_data)
):
    """Get paginated calls with optional filters."""
    
    # Build query
    query = {}
    
    # Add lead filter
    if lead_id:
        if not ObjectId.is_valid(lead_id):
            raise HTTPException(status_code=400, detail="Invalid lead ID")
        query["lead_id"] = ObjectId(lead_id)
    
    # Add agent filter
    if agent:
        query["agent"] = {"$regex": agent, "$options": "i"}
    
    # Role-based access: agents can only see their own calls
    if user_data.get("role") == "agent":
        query["agent_id"] = ObjectId(user_data.get("user_id"))
    
    # Calculate skip value for pagination
    skip = (page - 1) * limit
    
    # Get total count
    total = await calls_collection.count_documents(query)
    
    # Get calls
    cursor = calls_collection.find(query).skip(skip).limit(limit).sort("created_at", -1)
    calls = await cursor.to_list(length=limit)
    
    # Convert ObjectIds to strings
    for call in calls:
        call["id"] = str(call["_id"])
        del call["_id"]
        call["lead_id"] = str(call["lead_id"])
        if "agent_id" in call and call["agent_id"]:
            call["agent_id"] = str(call["agent_id"])
    
    return {
        "calls": calls,
        "total": total,
        "page": page,
        "pages": math.ceil(total / limit),
        "limit": limit
    }


@router.get("/{call_id}")
async def get_call(
    call_id: str,
    user_data: dict = Depends(get_current_user_data)
):
    """Get a specific call by ID."""
    
    if not ObjectId.is_valid(call_id):
        raise HTTPException(status_code=400, detail="Invalid call ID")
    
    call = await calls_collection.find_one({"_id": ObjectId(call_id)})
    if not call:
        raise HTTPException(status_code=404, detail="Call not found")
    
    # Role-based access: agents can only see their own calls
    if user_data.get("role") == "agent":
        if str(call.get("agent_id")) != user_data.get("user_id"):
            raise HTTPException(status_code=403, detail="Access denied")
    
    # Convert ObjectIds to strings
    call["id"] = str(call["_id"])
    del call["_id"]
    call["lead_id"] = str(call["lead_id"])
    if "agent_id" in call and call["agent_id"]:
        call["agent_id"] = str(call["agent_id"])
    
    return {"call": call}


@router.post("/")
async def create_call(
    call_data: CallCreate,
    user_data: dict = Depends(get_current_user_data)
):
    """Create a new call log entry."""
    
    # Verify lead exists
    lead_id = call_data.lead_id
    if isinstance(lead_id, str):
        lead_id = ObjectId(lead_id)
    
    lead = await leads_collection.find_one({"_id": lead_id})
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    # Role-based access: agents can only create calls for their assigned leads
    if user_data.get("role") == "agent":
        if str(lead.get("assigned_agent_id")) != user_data.get("user_id"):
            raise HTTPException(status_code=403, detail="Access denied - not your assigned lead")
    
    # Prepare call document
    call_dict = call_data.dict(by_alias=True)
    call_dict["created_at"] = datetime.utcnow()
    
    # Set agent info from current user if not provided
    if not call_dict.get("agent_id"):
        call_dict["agent_id"] = ObjectId(user_data.get("user_id"))
        call_dict["agent"] = user_data.get("name")
    
    # Convert string IDs to ObjectIds
    if isinstance(call_dict["lead_id"], str):
        call_dict["lead_id"] = ObjectId(call_dict["lead_id"])
    if isinstance(call_dict.get("agent_id"), str):
        call_dict["agent_id"] = ObjectId(call_dict["agent_id"])
    
    # Insert call
    result = await calls_collection.insert_one(call_dict)
    
    # Update lead's last_contact
    await leads_collection.update_one(
        {"_id": call_dict["lead_id"]},
        {"$set": {"last_contact": datetime.utcnow(), "updated_at": datetime.utcnow()}}
    )
    
    # Get the created call
    created_call = await calls_collection.find_one({"_id": result.inserted_id})
    
    # Convert ObjectIds to strings
    created_call["id"] = str(created_call["_id"])
    del created_call["_id"]
    created_call["lead_id"] = str(created_call["lead_id"])
    if "agent_id" in created_call and created_call["agent_id"]:
        created_call["agent_id"] = str(created_call["agent_id"])
    
    return {"call": created_call}


@router.put("/{call_id}")
async def update_call(
    call_id: str,
    call_data: CallUpdate,
    user_data: dict = Depends(get_current_user_data)
):
    """Update a call log entry."""
    
    if not ObjectId.is_valid(call_id):
        raise HTTPException(status_code=400, detail="Invalid call ID")
    
    # Check if call exists
    existing_call = await calls_collection.find_one({"_id": ObjectId(call_id)})
    if not existing_call:
        raise HTTPException(status_code=404, detail="Call not found")
    
    # Role-based access: agents can only update their own calls
    if user_data.get("role") == "agent":
        if str(existing_call.get("agent_id")) != user_data.get("user_id"):
            raise HTTPException(status_code=403, detail="Access denied")
    
    # Prepare update data
    update_dict = call_data.dict(by_alias=True, exclude_unset=True)
    if update_dict:
        # Convert string IDs to ObjectIds
        if "lead_id" in update_dict and isinstance(update_dict["lead_id"], str):
            update_dict["lead_id"] = ObjectId(update_dict["lead_id"])
        if "agent_id" in update_dict and isinstance(update_dict["agent_id"], str):
            update_dict["agent_id"] = ObjectId(update_dict["agent_id"])
        
        # Update call
        await calls_collection.update_one(
            {"_id": ObjectId(call_id)},
            {"$set": update_dict}
        )
    
    # Get updated call
    updated_call = await calls_collection.find_one({"_id": ObjectId(call_id)})
    
    # Convert ObjectIds to strings
    updated_call["id"] = str(updated_call["_id"])
    del updated_call["_id"]
    updated_call["lead_id"] = str(updated_call["lead_id"])
    if "agent_id" in updated_call and updated_call["agent_id"]:
        updated_call["agent_id"] = str(updated_call["agent_id"])
    
    return {"call": updated_call}


@router.delete("/{call_id}")
async def delete_call(
    call_id: str,
    user_data: dict = Depends(get_current_user_data)
):
    """Delete a call (admin only)."""
    
    # Only admins can delete calls
    if user_data.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    if not ObjectId.is_valid(call_id):
        raise HTTPException(status_code=400, detail="Invalid call ID")
    
    # Check if call exists
    call = await calls_collection.find_one({"_id": ObjectId(call_id)})
    if not call:
        raise HTTPException(status_code=404, detail="Call not found")
    
    # Delete call
    await calls_collection.delete_one({"_id": ObjectId(call_id)})
    
    return {"success": True, "message": "Call deleted successfully"}