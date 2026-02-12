from dataclasses import asdict, dataclass
from datetime import datetime


@dataclass(frozen=True, kw_only=True)
class MessageBaseEntity:
    chat_id: int
    sender_id: int
    content: str
    message_type: str = "text"
    reply_to_id: int | None = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True, kw_only=True)
class MessageCreateEntity(MessageBaseEntity):
    pass


@dataclass(frozen=True, kw_only=True)
class MessageEntity(MessageBaseEntity):
    id: int
    created_at: datetime
