from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class SaleBase(BaseModel):
    lead_id: PyObjectId = Field(alias="leadId")
    lead_name: str = Field(alias="leadName")
    property: str
    agent: str
    agent_id: Optional[PyObjectId] = Field(alias="agentId", default=None)
    stage: Literal["contacted", "viewed", "negotiation", "closed"] = "contacted"
    value: str
    probability: int = Field(ge=0, le=100)
    expected_close: str = Field(alias="expectedClose")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class SaleCreate(SaleBase):
    pass


class SaleUpdate(BaseModel):
    lead_id: Optional[PyObjectId] = Field(alias="leadId", default=None)
    lead_name: Optional[str] = Field(alias="leadName", default=None)
    property: Optional[str] = None
    agent: Optional[str] = None
    agent_id: Optional[PyObjectId] = Field(alias="agentId", default=None)
    stage: Optional[Literal["contacted", "viewed", "negotiation", "closed"]] = None
    value: Optional[str] = None
    probability: Optional[int] = Field(ge=0, le=100, default=None)
    expected_close: Optional[str] = Field(alias="expectedClose", default=None)
    last_activity: Optional[datetime] = Field(alias="lastActivity", default=None)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class Sale(SaleBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow, alias="createdAt")
    last_activity: datetime = Field(default_factory=datetime.utcnow, alias="lastActivity")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}