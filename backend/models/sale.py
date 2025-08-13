from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime


class SaleBase(BaseModel):
    lead_id: str = Field(alias="leadId")
    lead_name: str = Field(alias="leadName")
    property: str
    agent: str
    agent_id: Optional[str] = Field(alias="agentId", default=None)
    stage: Literal["contacted", "viewed", "negotiation", "closed"] = "contacted"
    value: str
    probability: int = Field(ge=0, le=100)
    expected_close: str = Field(alias="expectedClose")


class SaleCreate(SaleBase):
    pass


class SaleUpdate(BaseModel):
    lead_id: Optional[str] = Field(alias="leadId", default=None)
    lead_name: Optional[str] = Field(alias="leadName", default=None)
    property: Optional[str] = None
    agent: Optional[str] = None
    agent_id: Optional[str] = Field(alias="agentId", default=None)
    stage: Optional[Literal["contacted", "viewed", "negotiation", "closed"]] = None
    value: Optional[str] = None
    probability: Optional[int] = Field(ge=0, le=100, default=None)
    expected_close: Optional[str] = Field(alias="expectedClose", default=None)
    last_activity: Optional[datetime] = Field(alias="lastActivity", default=None)


class Sale(SaleBase):
    id: str = Field(alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow, alias="createdAt")
    last_activity: datetime = Field(default_factory=datetime.utcnow, alias="lastActivity")

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True
    }