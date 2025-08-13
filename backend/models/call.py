from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime


class CallBase(BaseModel):
    lead_id: str = Field(alias="leadId")
    lead_name: str = Field(alias="leadName")
    agent: str
    agent_id: Optional[str] = Field(alias="agentId", default=None)
    type: Literal["inbound", "outbound"]
    duration: str
    date: str
    time: str
    status: Literal["completed", "missed"]
    notes: Optional[str] = ""


class CallCreate(CallBase):
    pass


class CallUpdate(BaseModel):
    lead_id: Optional[str] = Field(alias="leadId", default=None)
    lead_name: Optional[str] = Field(alias="leadName", default=None)
    agent: Optional[str] = None
    agent_id: Optional[str] = Field(alias="agentId", default=None)
    type: Optional[Literal["inbound", "outbound"]] = None
    duration: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None
    status: Optional[Literal["completed", "missed"]] = None
    notes: Optional[str] = None


class Call(CallBase):
    id: str = Field(alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow, alias="createdAt")

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True
    }