"""Схема для создания нового сообщения."""

from pydantic import BaseModel


class MessageCreate(BaseModel):
    sender_id: int
    chat_id: int
    content: str
    message_type: str = 'text'
    reply_to_id: int | None = None
