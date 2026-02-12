"""Модель участника чата."""

from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import Index, UniqueConstraint

from app.domain.consts import UserRole
from app.infrastructure.postgres.models.base import Base

if TYPE_CHECKING:
    from .chat import Chat
    from .user import User


class ChatMember(Base):
    """Связь пользователя с чатом (участник чата)"""

    __tablename__ = "chat_members"

    id: Mapped[int] = mapped_column(primary_key=True)

    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id", ondelete="CASCADE"), nullable=False, comment="ID чата")

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        comment="ID пользователя",
    )

    role: Mapped[str] = mapped_column(
        String(20),
        default=UserRole.MEMBER.value,
        nullable=False,
        comment="Роль: owner, admin, member",
    )

    is_muted: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        comment="Заглушен ли чат для этого пользователя",
    )

    notifications_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        comment="Включены ли уведомления для этого чата",
    )

    joined_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
        comment="Когда пользователь присоединился к чату",
    )

    chat: Mapped["Chat"] = relationship(back_populates="members", foreign_keys=[chat_id])

    user: Mapped["User"] = relationship(back_populates="chat_memberships", foreign_keys=[user_id])

    def __repr__(self) -> str:
        return f"<ChatMember(chat={self.chat_id}, user={self.user_id}, role='{self.role}')>"


__table_args__ = (
    UniqueConstraint("chat_id", "user_id", name="uq_chat_user"),
    Index("ix_chat_members_user", "user_id"),
)
