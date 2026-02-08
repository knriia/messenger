"""Модель сущности чата."""

from datetime import datetime, timezone
from typing import Optional, TYPE_CHECKING

from sqlalchemy import String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import Index

from app.infrastructure.postgres.models.base import Base
from app.domain.consts import ChatType


if TYPE_CHECKING:
    from .user import User
    from .message import Message
    from .chat_member import ChatMember


class Chat(Base):
    """Модель чата (личного или группового)"""

    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        comment="Название чата (для групповых чатов)"
    )

    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="Описание чата (для групповых)"
    )

    chat_type: Mapped[str] = mapped_column(
        String(20),
        default=ChatType.PRIVATE.value,
        nullable=False,
        comment="Тип чата: private (личный), group (групповой), channel (канал)"
    )

    is_private: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        comment="Приватный ли чат (True) или публичный (False)"
    )

    private_hash: Mapped[Optional[str]] = mapped_column(
        String(64),
        unique=True,
        index=True,
        nullable=True,
        comment="Хэш для быстрого поиска приватных чатов между двумя пользователями"
    )

    creator_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),  # Если создатель удалится, чат остаётся
        nullable=False,
        comment="ID пользователя, который создал чат"
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        comment="Активен ли чат"
    )

    avatar_url: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        comment="URL аватара чата"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        comment="Дата создания чата"
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
        comment="Дата последнего обновления (сообщения/настроек)"
    )

    last_message_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="Дата последнего сообщения в чате"
    )

    creator: Mapped["User"] = relationship(
        back_populates="created_chats",
        foreign_keys=[creator_id]
    )

    messages: Mapped[list["Message"]] = relationship(
        back_populates="chat",
        order_by="Message.created_at.desc()",  # Новые сообщения первыми
        cascade="all, delete-orphan",
        lazy="dynamic"  # Для пагинации
    )

    members: Mapped[list["ChatMember"]] = relationship(
        back_populates="chat",
        cascade="all, delete-orphan",
        lazy="selectin"  # Загружаем при загрузке чата
    )

    @property
    def display_name(self) -> str:
        """Имя чата для отображения"""
        if self.name:
            return self.name

        if self.chat_type == ChatType.PRIVATE.value:
            if self.members:
                other_members = [m.user for m in self.members if m.user_id != self.creator_id]
                if other_members:
                    return ", ".join([user.display_name for user in other_members[:2]])

        return f"Чат #{self.id}"

    @property
    def member_count(self) -> int:
        """Количество участников"""
        return len(self.members) if self.members else 0

    @property
    def last_message(self) -> Optional["Message"]:
        """Последнее сообщение в чате"""
        if self.messages:
            return self.messages[0] if self.messages else None
        return None

    def update_last_message_time(self):
        """Обновить время последнего сообщения"""
        last_msg = self.last_message
        if last_msg:
            self.last_message_at = last_msg.created_at

    def is_user_member(self, user_id: int) -> bool:
        """Проверить, является ли пользователь участником чата"""
        return any(member.user_id == user_id for member in self.members)

    def get_user_role(self, user_id: int) -> Optional[str]:
        """Получить роль пользователя в чате"""
        for member in self.members:
            if member.user_id == user_id:
                return member.role
        return None

    def __repr__(self) -> str:
        return f"<Chat(id={self.id}, type='{self.chat_type}', name='{self.name or self.display_name}')>"


__table_args__ = (
    Index('ix_chats_creator', 'creator_id'),
    Index('ix_chats_last_message', 'last_message_at', postgresql_using='btree'),
    Index('ix_chats_type', 'chat_type'),
)
