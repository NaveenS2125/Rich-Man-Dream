from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from database.connection import sales_collection, leads_collection
from auth.middleware import get_current_user_data
from models.sale import SaleCreate, SaleUpdate
from bson import ObjectId
from datetime import datetime
import math

router = APIRouter(prefix="/sales", tags=["Sales"])


@router.get("/")
async def get_sales(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    stage: Optional[str] = Query(None),
    agent: Optional[str] = Query(None),
    user_data: dict = Depends(get_current_user_data)
):
    """Get paginated sales with optional filters."""
    
    # Build query
    query = {}
    
    # Add stage filter
    if stage:
        query["stage"] = stage
    
    # Add agent filter
    if agent:
        query["agent"] = {"$regex": agent, "$options": "i"}
    
    # Role-based access: agents can only see their own sales
    if user_data.get("role") == "agent":
        query["agent_id"] = ObjectId(user_data.get("user_id"))
    
    # Calculate skip value for pagination
    skip = (page - 1) * limit
    
    # Get total count
    total = await sales_collection.count_documents(query)
    
    # Get sales
    cursor = sales_collection.find(query).skip(skip).limit(limit).sort("created_at", -1)
    sales = await cursor.to_list(length=limit)
    
    # Convert ObjectIds to strings
    for sale in sales:
        sale["id"] = str(sale["_id"])
        del sale["_id"]
        sale["lead_id"] = str(sale["lead_id"])
        if "agent_id" in sale and sale["agent_id"]:
            sale["agent_id"] = str(sale["agent_id"])
    
    return {
        "sales": sales,
        "total": total,
        "page": page,
        "pages": math.ceil(total / limit),
        "limit": limit
    }


@router.get("/{sale_id}")
async def get_sale(
    sale_id: str,
    user_data: dict = Depends(get_current_user_data)
):
    """Get a specific sale by ID."""
    
    if not ObjectId.is_valid(sale_id):
        raise HTTPException(status_code=400, detail="Invalid sale ID")
    
    sale = await sales_collection.find_one({"_id": ObjectId(sale_id)})
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    
    # Role-based access: agents can only see their own sales
    if user_data.get("role") == "agent":
        if str(sale.get("agent_id")) != user_data.get("user_id"):
            raise HTTPException(status_code=403, detail="Access denied")
    
    # Convert ObjectIds to strings
    sale["id"] = str(sale["_id"])
    del sale["_id"]
    sale["lead_id"] = str(sale["lead_id"])
    if "agent_id" in sale and sale["agent_id"]:
        sale["agent_id"] = str(sale["agent_id"])
    
    return {"sale": sale}


@router.post("/")
async def create_sale(
    sale_data: SaleCreate,
    user_data: dict = Depends(get_current_user_data)
):
    """Create a new sales opportunity."""
    
    # Verify lead exists
    lead_id = sale_data.lead_id
    if isinstance(lead_id, str):
        lead_id = ObjectId(lead_id)
    
    lead = await leads_collection.find_one({"_id": lead_id})
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    # Role-based access: agents can only create sales for their assigned leads
    if user_data.get("role") == "agent":
        if str(lead.get("assigned_agent_id")) != user_data.get("user_id"):
            raise HTTPException(status_code=403, detail="Access denied - not your assigned lead")
    
    # Check if sale already exists for this lead
    existing_sale = await sales_collection.find_one({"lead_id": lead_id})
    if existing_sale:
        raise HTTPException(status_code=400, detail="Sale opportunity already exists for this lead")
    
    # Prepare sale document
    sale_dict = sale_data.dict(by_alias=True)
    sale_dict["created_at"] = datetime.utcnow()
    sale_dict["last_activity"] = datetime.utcnow()
    
    # Set agent info from current user if not provided
    if not sale_dict.get("agent_id"):
        sale_dict["agent_id"] = ObjectId(user_data.get("user_id"))
        sale_dict["agent"] = user_data.get("name")
    
    # Convert string IDs to ObjectIds
    if isinstance(sale_dict["lead_id"], str):
        sale_dict["lead_id"] = ObjectId(sale_dict["lead_id"])
    if isinstance(sale_dict.get("agent_id"), str):
        sale_dict["agent_id"] = ObjectId(sale_dict["agent_id"])
    
    # Insert sale
    result = await sales_collection.insert_one(sale_dict)
    
    # Get the created sale
    created_sale = await sales_collection.find_one({"_id": result.inserted_id})
    
    # Convert ObjectIds to strings
    created_sale["id"] = str(created_sale["_id"])
    del created_sale["_id"]
    created_sale["lead_id"] = str(created_sale["lead_id"])
    if "agent_id" in created_sale and created_sale["agent_id"]:
        created_sale["agent_id"] = str(created_sale["agent_id"])
    
    return {"sale": created_sale}


@router.put("/{sale_id}")
async def update_sale(
    sale_id: str,
    sale_data: SaleUpdate,
    user_data: dict = Depends(get_current_user_data)
):
    """Update a sales opportunity."""
    
    if not ObjectId.is_valid(sale_id):
        raise HTTPException(status_code=400, detail="Invalid sale ID")
    
    # Check if sale exists
    existing_sale = await sales_collection.find_one({"_id": ObjectId(sale_id)})
    if not existing_sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    
    # Role-based access: agents can only update their own sales
    if user_data.get("role") == "agent":
        if str(existing_sale.get("agent_id")) != user_data.get("user_id"):
            raise HTTPException(status_code=403, detail="Access denied")
    
    # Prepare update data
    update_dict = sale_data.dict(by_alias=True, exclude_unset=True)
    if update_dict:
        update_dict["last_activity"] = datetime.utcnow()
        
        # Convert string IDs to ObjectIds
        if "lead_id" in update_dict and isinstance(update_dict["lead_id"], str):
            update_dict["lead_id"] = ObjectId(update_dict["lead_id"])
        if "agent_id" in update_dict and isinstance(update_dict["agent_id"], str):
            update_dict["agent_id"] = ObjectId(update_dict["agent_id"])
        
        # Update sale
        await sales_collection.update_one(
            {"_id": ObjectId(sale_id)},
            {"$set": update_dict}
        )
    
    # Get updated sale
    updated_sale = await sales_collection.find_one({"_id": ObjectId(sale_id)})
    
    # Convert ObjectIds to strings
    updated_sale["id"] = str(updated_sale["_id"])
    del updated_sale["_id"]
    updated_sale["lead_id"] = str(updated_sale["lead_id"])
    if "agent_id" in updated_sale and updated_sale["agent_id"]:
        updated_sale["agent_id"] = str(updated_sale["agent_id"])
    
    return {"sale": updated_sale}


@router.delete("/{sale_id}")
async def delete_sale(
    sale_id: str,
    user_data: dict = Depends(get_current_user_data)
):
    """Delete a sales opportunity (admin only)."""
    
    # Only admins can delete sales
    if user_data.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    if not ObjectId.is_valid(sale_id):
        raise HTTPException(status_code=400, detail="Invalid sale ID")
    
    # Check if sale exists
    sale = await sales_collection.find_one({"_id": ObjectId(sale_id)})
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    
    # Delete sale
    await sales_collection.delete_one({"_id": ObjectId(sale_id)})
    
    return {"success": True, "message": "Sale deleted successfully"}