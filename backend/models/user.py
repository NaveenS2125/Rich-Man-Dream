from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Literal
from datetime import datetime


class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: Literal["admin", "agent", "viewer"] = "agent"
    avatar: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[Literal["admin", "agent", "viewer"]] = None
    avatar: Optional[str] = None


class User(UserBase):
    id: str = Field(alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True
    }


class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    role: str
    avatar: Optional[str] = None

    model_config = {
        "from_attributes": True
    }