"""Модель сущности сообщения."""

from typing import Optional, TYPE_CHECKING
from datetime import datetime, timezone
from sqlalchemy import ForeignKey, String, DateTime, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.models.base import Base
from app.domain.consts import MessageType

if TYPE_CHECKING:
    from .chat import Chat
    from .user import User


class Message(Base):
    __tablename__ = 'messages'

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    message_type: Mapped[str] = mapped_column(
        String(30),
        default=MessageType.TEXT,
        nullable=False,
        comment='Тип сообщения: text, image, file'
    )
    sender_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        comment="ID отправителя"
    )
    chat_id: Mapped[int] = mapped_column(
        ForeignKey("chats.id", ondelete="CASCADE"),
        nullable=False,
        comment="ID чата"
    )
    reply_to_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("messages.id", ondelete="SET NULL"),
        nullable=True,
        comment="ID сообщения на которое отвечаем"
    )
    is_edited: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        comment="Было ли сообщение отредактировано"
    )
    is_deleted: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        comment="Удалено ли сообщение (soft delete)"
    )
    deleted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="Когда сообщение было удалено"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        comment="Дата отправки сообщения"
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
        comment="Дата последнего редактирования"
    )

    sender: Mapped["User"] = relationship(
        back_populates="sent_messages",
        foreign_keys=[sender_id]
    )

    chat: Mapped["Chat"] = relationship(
        back_populates="messages"
    )

    reply_to: Mapped[Optional["Message"]] = relationship(
        remote_side=[id],
        backref="replies"
    )

    def __repr__(self) -> str:
        preview = self.content[:30] + "..." if len(self.content) > 30 else self.content
        return f"<Message(id={self.id}, chat={self.chat_id}, sender={self.sender_id}, text='{preview}')>"