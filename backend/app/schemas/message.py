from pydantic import BaseModel


class MessageCreateDTO(BaseModel):
    sender_id: int
    chat_id: int
    content: str
    message_type: str = 'text'
    reply_to_id: int | None = None
