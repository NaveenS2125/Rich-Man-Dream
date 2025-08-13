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


class CallBase(BaseModel):
    lead_id: PyObjectId = Field(alias="leadId")
    lead_name: str = Field(alias="leadName")
    agent: str
    agent_id: Optional[PyObjectId] = Field(alias="agentId", default=None)
    type: Literal["inbound", "outbound"]
    duration: str
    date: str
    time: str
    status: Literal["completed", "missed"]
    notes: Optional[str] = ""

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class CallCreate(CallBase):
    pass


class CallUpdate(BaseModel):
    lead_id: Optional[PyObjectId] = Field(alias="leadId", default=None)
    lead_name: Optional[str] = Field(alias="leadName", default=None)
    agent: Optional[str] = None
    agent_id: Optional[PyObjectId] = Field(alias="agentId", default=None)
    type: Optional[Literal["inbound", "outbound"]] = None
    duration: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None
    status: Optional[Literal["completed", "missed"]] = None
    notes: Optional[str] = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class Call(CallBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow, alias="createdAt")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}