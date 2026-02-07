from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ChatOut(BaseModel):
    id: int
    chat_type: str  # private, group, etc.
    name: str | None = None
    created_at: datetime
    last_message_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
