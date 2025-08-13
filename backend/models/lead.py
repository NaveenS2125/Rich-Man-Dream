from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Literal
from datetime import datetime


class LeadBase(BaseModel):
    name: str
    email: EmailStr
    phone: str
    status: Literal["hot", "warm", "cold"] = "cold"
    source: str
    budget: str
    property_type: str = Field(alias="propertyType")
    assigned_agent: str = Field(alias="assignedAgent")
    assigned_agent_id: Optional[str] = Field(alias="assignedAgentId", default=None)
    notes: Optional[str] = ""


class LeadCreate(LeadBase):
    pass


class LeadUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    status: Optional[Literal["hot", "warm", "cold"]] = None
    source: Optional[str] = None
    budget: Optional[str] = None
    property_type: Optional[str] = Field(alias="propertyType", default=None)
    assigned_agent: Optional[str] = Field(alias="assignedAgent", default=None)
    assigned_agent_id: Optional[str] = Field(alias="assignedAgentId", default=None)
    notes: Optional[str] = None
    last_contact: Optional[datetime] = Field(alias="lastContact", default=None)


class Lead(LeadBase):
    id: str = Field(alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow, alias="createdAt")
    updated_at: datetime = Field(default_factory=datetime.utcnow, alias="updatedAt")
    last_contact: Optional[datetime] = Field(alias="lastContact", default=None)

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True
    }