"""Схема для создания нового сообщения."""

from datetime import datetime

from pydantic import BaseModel

from app.domain.entities.message_entity import MessageCreateEntity


class MessageCreate(BaseModel):
    chat_id: int
    content: str
    message_type: str = "text"
    reply_to_id: int | None = None

    def to_entity(self, sender_id: int) -> MessageCreateEntity:
        return MessageCreateEntity(
            sender_id=sender_id,
            chat_id=self.chat_id,
            content=self.content,
            message_type=self.message_type,
            reply_to_id=self.reply_to_id,
        )


class MessageRead(MessageCreate):
    id: int
    sender_id: int
    chat_id: int
    content: str
    message_type: str
    created_at: datetime
    reply_to_id: int | None = None

    class Config:
        from_attributes = True
