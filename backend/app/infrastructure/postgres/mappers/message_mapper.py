from app.infrastructure.postgres.models.message import Message
from app.domain.entities.message_entity import MessageEntity

class MessageMapper:
    @staticmethod
    def to_domain(db_msg: Message) -> MessageEntity:
        return MessageEntity(
            id=db_msg.id,
            chat_id=db_msg.chat_id,
            sender_id=db_msg.sender_id,
            content=db_msg.content,
            created_at=db_msg.created_at
        )
