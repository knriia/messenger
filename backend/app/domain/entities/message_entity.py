from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass(frozen=True)
class MessageEntity:
    id: int
    chat_id: int
    sender_id: int
    content: str
    created_at: datetime

    def to_dict(self) -> dict:
        return asdict(self)
