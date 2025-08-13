from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime


class ViewingBase(BaseModel):
    property: str
    address: str
    date: str
    time: str
    lead_name: str = Field(alias="leadName")
    lead_id: Optional[str] = Field(alias="leadId", default=None)
    agent: str
    agent_id: Optional[str] = Field(alias="agentId", default=None)
    status: Literal["scheduled", "completed", "cancelled"] = "scheduled"
    price: str
    type: str


class ViewingCreate(ViewingBase):
    pass


class ViewingUpdate(BaseModel):
    property: Optional[str] = None
    address: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None
    lead_name: Optional[str] = Field(alias="leadName", default=None)
    lead_id: Optional[str] = Field(alias="leadId", default=None)
    agent: Optional[str] = None
    agent_id: Optional[str] = Field(alias="agentId", default=None)
    status: Optional[Literal["scheduled", "completed", "cancelled"]] = None
    price: Optional[str] = None
    type: Optional[str] = None


class Viewing(ViewingBase):
    id: str = Field(alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow, alias="createdAt")

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True
    }