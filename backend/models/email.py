from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Literal
from datetime import datetime


class EmailBase(BaseModel):
    lead_id: Optional[str] = Field(alias="leadId", default=None)
    lead_name: Optional[str] = Field(alias="leadName", default=None)
    to_email: EmailStr = Field(alias="toEmail")
    from_email: EmailStr = Field(alias="fromEmail")
    subject: str
    content: str
    email_type: Literal["manual", "automated", "template"] = Field(alias="emailType", default="manual")
    template_id: Optional[str] = Field(alias="templateId", default=None)
    status: Literal["draft", "sent", "delivered", "failed", "read"] = "draft"
    direction: Literal["inbound", "outbound"] = "outbound"
    agent_id: Optional[str] = Field(alias="agentId", default=None)
    agent_name: Optional[str] = Field(alias="agentName", default=None)


class EmailCreate(EmailBase):
    pass


class EmailUpdate(BaseModel):
    lead_id: Optional[str] = Field(alias="leadId", default=None)
    lead_name: Optional[str] = Field(alias="leadName", default=None)
    to_email: Optional[EmailStr] = Field(alias="toEmail", default=None)
    from_email: Optional[EmailStr] = Field(alias="fromEmail", default=None)
    subject: Optional[str] = None
    content: Optional[str] = None
    email_type: Optional[Literal["manual", "automated", "template"]] = Field(alias="emailType", default=None)
    template_id: Optional[str] = Field(alias="templateId", default=None)
    status: Optional[Literal["draft", "sent", "delivered", "failed", "read"]] = None
    direction: Optional[Literal["inbound", "outbound"]] = None
    agent_id: Optional[str] = Field(alias="agentId", default=None)
    agent_name: Optional[str] = Field(alias="agentName", default=None)


class Email(EmailBase):
    id: str = Field(alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow, alias="createdAt")
    updated_at: datetime = Field(default_factory=datetime.utcnow, alias="updatedAt")
    sent_at: Optional[datetime] = Field(alias="sentAt", default=None)

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True
    }


# Email Template Models
class EmailTemplateBase(BaseModel):
    name: str
    subject: str
    content: str
    template_type: Literal["welcome", "viewing_reminder", "sale_update", "follow_up", "custom"] = Field(alias="templateType")
    variables: list[str] = []  # List of variable placeholders like {lead_name}, {agent_name}
    is_active: bool = Field(alias="isActive", default=True)


class EmailTemplateCreate(EmailTemplateBase):
    pass


class EmailTemplateUpdate(BaseModel):
    name: Optional[str] = None
    subject: Optional[str] = None
    content: Optional[str] = None
    template_type: Optional[Literal["welcome", "viewing_reminder", "sale_update", "follow_up", "custom"]] = Field(alias="templateType", default=None)
    variables: Optional[list[str]] = None
    is_active: Optional[bool] = Field(alias="isActive", default=None)


class EmailTemplate(EmailTemplateBase):
    id: str = Field(alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow, alias="createdAt")
    updated_at: datetime = Field(default_factory=datetime.utcnow, alias="updatedAt")

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True
    }