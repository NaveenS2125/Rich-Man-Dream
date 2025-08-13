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


class ViewingBase(BaseModel):
    property: str
    address: str
    date: str
    time: str
    lead_name: str = Field(alias="leadName")
    lead_id: Optional[PyObjectId] = Field(alias="leadId", default=None)
    agent: str
    agent_id: Optional[PyObjectId] = Field(alias="agentId", default=None)
    status: Literal["scheduled", "completed", "cancelled"] = "scheduled"
    price: str
    type: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class ViewingCreate(ViewingBase):
    pass


class ViewingUpdate(BaseModel):
    property: Optional[str] = None
    address: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None
    lead_name: Optional[str] = Field(alias="leadName", default=None)
    lead_id: Optional[PyObjectId] = Field(alias="leadId", default=None)
    agent: Optional[str] = None
    agent_id: Optional[PyObjectId] = Field(alias="agentId", default=None)
    status: Optional[Literal["scheduled", "completed", "cancelled"]] = None
    price: Optional[str] = None
    type: Optional[str] = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class Viewing(ViewingBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow, alias="createdAt")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}