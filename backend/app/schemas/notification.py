from pydantic import BaseModel

from app.schemas.message import MessageRead


class RedisChatNotification(BaseModel):
    recipient_ids: list[int]
    payload: MessageRead