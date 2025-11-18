from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from enum import Enum


class MessageStatus(str, Enum):
    SENT = "sent"
    READ = "read"


class Message(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    sender_id: UUID
    receiver_id: UUID
    advertisement_id: UUID
    text: str
    status: MessageStatus
    created_at: datetime
    read_at: datetime | None = None


class MessageCreate(BaseModel):
    receiver_id: UUID
    advertisement_id: UUID
    text: str


class MessageList(BaseModel):
    items: list[Message]
    total: int
    limit: int
    offset: int