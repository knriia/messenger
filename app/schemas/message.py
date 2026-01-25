from pydantic import BaseModel


class MessageCreate(BaseModel):
    text: str
    user_id: int
