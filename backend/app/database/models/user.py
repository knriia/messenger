"""Модель сущности пользователя."""

from typing import TYPE_CHECKING
from datetime import datetime, timezone
from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.models.base import Base


if TYPE_CHECKING:
    from .chat import ChatMember, Chat
    from .message import Message


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
        comment='Уникальное имя пользователя'
    )
    email: Mapped[str | None] = mapped_column(String(255), unique=True, index=True, comment='Email пользователя')
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False, comment='Хэшированный пароль')
    first_name: Mapped[str] = mapped_column(String(100), nullable=True, comment='Имя пользователя')
    last_name: Mapped[str] = mapped_column(String(100), nullable=True, comment='Фамилия пользователя')
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, comment='Активен ли аккаунт')
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, comment='Подтвержден ли аккаунт')
    is_online: Mapped[bool] = mapped_column(Boolean, default=False, comment='Оналайн ли пользователь сейчас')
    last_seen: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        comment='Последний посещение'
    )
    notifications_enabled: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        comment="Включены ли уведомления"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        comment="Дата создания аккаунта"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
        comment="Дата последнего обновления профиля"
    )
    sent_messages: Mapped[list["Message"]] = relationship(
        back_populates="sender",
        foreign_keys="Message.sender_id",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    chat_memberships: Mapped[list["ChatMember"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    created_chats: Mapped[list["Chat"]] = relationship(
        back_populates="creator",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    @property
    def full_name(self) -> str:
        """Полное имя пользователя (имя + фамилия)"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        return self.username

    @property
    def display_name(self) -> str:
        """Имя для отображения в интерфейсе"""
        full = self.full_name
        return full if full is not None else self.username

    def update_last_seen(self):
        """Обновить время последней активности"""
        self.last_seen = datetime.now(timezone.utc)

    @property
    def chats(self) -> list["Chat"]:
        """Все чаты пользователя"""
        return [membership.chat for membership in self.chat_memberships]

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"

