"""Модель сущности сообщения."""

from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.consts import MessageType
from app.infrastructure.postgres.models.base import Base

if TYPE_CHECKING:
    from .chat import Chat
    from .user import User


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    message_type: Mapped[str] = mapped_column(
        String(30),
        default=MessageType.TEXT.value,
        nullable=False,
        comment="Тип сообщения: text, image, file",
    )
    sender_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        comment="ID отправителя",
    )
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id", ondelete="CASCADE"), nullable=False, comment="ID чата")
    reply_to_id: Mapped[int | None] = mapped_column(
        ForeignKey("messages.id", ondelete="SET NULL"),
        nullable=True,
        comment="ID сообщения на которое отвечаем",
    )
    is_edited: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        comment="Было ли сообщение отредактировано",
    )
    is_deleted: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        comment="Удалено ли сообщение (soft delete)",
    )
    deleted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True, comment="Когда сообщение было удалено"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
        comment="Дата отправки сообщения",
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
        comment="Дата последнего редактирования",
    )

    sender: Mapped["User"] = relationship(back_populates="sent_messages", foreign_keys=[sender_id])

    chat: Mapped["Chat"] = relationship(back_populates="messages")

    reply_to: Mapped["Message"] | None = relationship(remote_side=[id], backref="replies")

    def __repr__(self) -> str:
        preview = self.content[:30] + "..." if len(self.content) > 30 else self.content
        return f"<Message(id={self.id}, chat={self.chat_id}, sender={self.sender_id}, text='{preview}')>"
