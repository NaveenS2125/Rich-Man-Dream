from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from database.connection import viewings_collection, leads_collection
from auth.middleware import get_current_user_data
from models.viewing import ViewingCreate, ViewingUpdate
from bson import ObjectId
from datetime import datetime
import math

router = APIRouter(prefix="/viewings", tags=["Viewings"])


@router.get("/")
async def get_viewings(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    date: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    agent: Optional[str] = Query(None),
    user_data: dict = Depends(get_current_user_data)
):
    """Get paginated viewings with optional filters."""
    
    # Build query
    query = {}
    
    # Add date filter
    if date:
        query["date"] = date
    
    # Add status filter
    if status:
        query["status"] = status
    
    # Add agent filter
    if agent:
        query["agent"] = {"$regex": agent, "$options": "i"}
    
    # Role-based access: agents can only see their own viewings
    if user_data.get("role") == "agent":
        query["agent_id"] = ObjectId(user_data.get("user_id"))
    
    # Calculate skip value for pagination
    skip = (page - 1) * limit
    
    # Get total count
    total = await viewings_collection.count_documents(query)
    
    # Get viewings
    cursor = viewings_collection.find(query).skip(skip).limit(limit).sort("date", 1)
    viewings = await cursor.to_list(length=limit)
    
    # Convert ObjectIds to strings
    for viewing in viewings:
        viewing["id"] = str(viewing["_id"])
        del viewing["_id"]
        if "lead_id" in viewing and viewing["lead_id"]:
            viewing["lead_id"] = str(viewing["lead_id"])
        if "agent_id" in viewing and viewing["agent_id"]:
            viewing["agent_id"] = str(viewing["agent_id"])
    
    return {
        "viewings": viewings,
        "total": total,
        "page": page,
        "pages": math.ceil(total / limit),
        "limit": limit
    }


@router.get("/{viewing_id}")
async def get_viewing(
    viewing_id: str,
    user_data: dict = Depends(get_current_user_data)
):
    """Get a specific viewing by ID."""
    
    if not ObjectId.is_valid(viewing_id):
        raise HTTPException(status_code=400, detail="Invalid viewing ID")
    
    viewing = await viewings_collection.find_one({"_id": ObjectId(viewing_id)})
    if not viewing:
        raise HTTPException(status_code=404, detail="Viewing not found")
    
    # Role-based access: agents can only see their own viewings
    if user_data.get("role") == "agent":
        if str(viewing.get("agent_id")) != user_data.get("user_id"):
            raise HTTPException(status_code=403, detail="Access denied")
    
    # Convert ObjectIds to strings
    viewing["id"] = str(viewing["_id"])
    del viewing["_id"]
    if "lead_id" in viewing and viewing["lead_id"]:
        viewing["lead_id"] = str(viewing["lead_id"])
    if "agent_id" in viewing and viewing["agent_id"]:
        viewing["agent_id"] = str(viewing["agent_id"])
    
    return {"viewing": viewing}


@router.post("/")
async def create_viewing(
    viewing_data: ViewingCreate,
    user_data: dict = Depends(get_current_user_data)
):
    """Create a new viewing."""
    
    # Verify lead exists if lead_id is provided
    if viewing_data.lead_id:
        lead_id = viewing_data.lead_id
        if isinstance(lead_id, str):
            lead_id = ObjectId(lead_id)
        
        lead = await leads_collection.find_one({"_id": lead_id})
        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found")
        
        # Role-based access: agents can only create viewings for their assigned leads
        if user_data.get("role") == "agent":
            if str(lead.get("assigned_agent_id")) != user_data.get("user_id"):
                raise HTTPException(status_code=403, detail="Access denied - not your assigned lead")
    
    # Prepare viewing document
    viewing_dict = viewing_data.dict(by_alias=True)
    viewing_dict["created_at"] = datetime.utcnow()
    
    # Set agent info from current user if not provided
    if not viewing_dict.get("agent_id"):
        viewing_dict["agent_id"] = ObjectId(user_data.get("user_id"))
        viewing_dict["agent"] = user_data.get("name")
    
    # Convert string IDs to ObjectIds
    if viewing_dict.get("lead_id") and isinstance(viewing_dict["lead_id"], str):
        viewing_dict["lead_id"] = ObjectId(viewing_dict["lead_id"])
    if isinstance(viewing_dict.get("agent_id"), str):
        viewing_dict["agent_id"] = ObjectId(viewing_dict["agent_id"])
    
    # Insert viewing
    result = await viewings_collection.insert_one(viewing_dict)
    
    # Get the created viewing
    created_viewing = await viewings_collection.find_one({"_id": result.inserted_id})
    
    # Convert ObjectIds to strings
    created_viewing["id"] = str(created_viewing["_id"])
    del created_viewing["_id"]
    if "lead_id" in created_viewing and created_viewing["lead_id"]:
        created_viewing["lead_id"] = str(created_viewing["lead_id"])
    if "agent_id" in created_viewing and created_viewing["agent_id"]:
        created_viewing["agent_id"] = str(created_viewing["agent_id"])
    
    return {"viewing": created_viewing}


@router.put("/{viewing_id}")
async def update_viewing(
    viewing_id: str,
    viewing_data: ViewingUpdate,
    user_data: dict = Depends(get_current_user_data)
):
    """Update a viewing."""
    
    if not ObjectId.is_valid(viewing_id):
        raise HTTPException(status_code=400, detail="Invalid viewing ID")
    
    # Check if viewing exists
    existing_viewing = await viewings_collection.find_one({"_id": ObjectId(viewing_id)})
    if not existing_viewing:
        raise HTTPException(status_code=404, detail="Viewing not found")
    
    # Role-based access: agents can only update their own viewings
    if user_data.get("role") == "agent":
        if str(existing_viewing.get("agent_id")) != user_data.get("user_id"):
            raise HTTPException(status_code=403, detail="Access denied")
    
    # Prepare update data
    update_dict = viewing_data.dict(by_alias=True, exclude_unset=True)
    if update_dict:
        # Convert string IDs to ObjectIds
        if "lead_id" in update_dict and update_dict["lead_id"] and isinstance(update_dict["lead_id"], str):
            update_dict["lead_id"] = ObjectId(update_dict["lead_id"])
        if "agent_id" in update_dict and update_dict["agent_id"] and isinstance(update_dict["agent_id"], str):
            update_dict["agent_id"] = ObjectId(update_dict["agent_id"])
        
        # Update viewing
        await viewings_collection.update_one(
            {"_id": ObjectId(viewing_id)},
            {"$set": update_dict}
        )
    
    # Get updated viewing
    updated_viewing = await viewings_collection.find_one({"_id": ObjectId(viewing_id)})
    
    # Convert ObjectIds to strings
    updated_viewing["id"] = str(updated_viewing["_id"])
    del updated_viewing["_id"]
    if "lead_id" in updated_viewing and updated_viewing["lead_id"]:
        updated_viewing["lead_id"] = str(updated_viewing["lead_id"])
    if "agent_id" in updated_viewing and updated_viewing["agent_id"]:
        updated_viewing["agent_id"] = str(updated_viewing["agent_id"])
    
    return {"viewing": updated_viewing}


@router.delete("/{viewing_id}")
async def delete_viewing(
    viewing_id: str,
    user_data: dict = Depends(get_current_user_data)
):
    """Delete a viewing (admin only)."""
    
    # Only admins can delete viewings
    if user_data.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    if not ObjectId.is_valid(viewing_id):
        raise HTTPException(status_code=400, detail="Invalid viewing ID")
    
    # Check if viewing exists
    viewing = await viewings_collection.find_one({"_id": ObjectId(viewing_id)})
    if not viewing:
        raise HTTPException(status_code=404, detail="Viewing not found")
    
    # Delete viewing
    await viewings_collection.delete_one({"_id": ObjectId(viewing_id)})
    
    return {"success": True, "message": "Viewing deleted successfully"}