from pydantic import BaseModel, Field, EmailStr
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


class LeadBase(BaseModel):
    name: str
    email: EmailStr
    phone: str
    status: Literal["hot", "warm", "cold"] = "cold"
    source: str
    budget: str
    property_type: str = Field(alias="propertyType")
    assigned_agent: str = Field(alias="assignedAgent")
    assigned_agent_id: Optional[PyObjectId] = Field(alias="assignedAgentId", default=None)
    notes: Optional[str] = ""

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


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
    assigned_agent_id: Optional[PyObjectId] = Field(alias="assignedAgentId", default=None)
    notes: Optional[str] = None
    last_contact: Optional[datetime] = Field(alias="lastContact", default=None)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class Lead(LeadBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow, alias="createdAt")
    updated_at: datetime = Field(default_factory=datetime.utcnow, alias="updatedAt")
    last_contact: Optional[datetime] = Field(alias="lastContact", default=None)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}