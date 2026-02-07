"""Схема для создания нового сообщения."""

from datetime import datetime
from pydantic import BaseModel


class MessageCreate(BaseModel):
    sender_id: int
    chat_id: int
    content: str
    message_type: str = 'text'
    reply_to_id: int | None = None

class MessageRead(MessageCreate):
    """То, что летит в сокет и возвращается из API."""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class MessageSendResponse(BaseModel):
    status: str = "accepted"
    details: str = "message_queued"
