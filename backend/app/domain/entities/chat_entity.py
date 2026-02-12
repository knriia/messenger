from dataclasses import dataclass
from datetime import datetime
from app.domain.consts import ChatType


@dataclass(frozen=True)
class BaseChatEntity:
    id: int
    creator_id: int
    chat_type: ChatType
    created_at: datetime


@dataclass(frozen=True)
class PrivateChatEntity(BaseChatEntity):
    private_hash: str


@dataclass(frozen=True)
class GroupChatEntity(BaseChatEntity):
    chat_name: str
