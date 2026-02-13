from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.domain.consts import ChatType


class ChatBase(BaseModel):
    id: int
    chat_type: ChatType
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class PrivateChatOut(ChatBase):
    private_hash: str


class GroupChatOut(ChatBase):
    chat_name: str
