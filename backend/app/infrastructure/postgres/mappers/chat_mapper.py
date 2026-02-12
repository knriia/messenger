from app.domain.consts import ChatType
from app.domain.entities.chat_entity import (
    BaseChatEntity,
    GroupChatEntity,
    PrivateChatEntity,
)
from app.infrastructure.postgres.models.chat import Chat


class ChatMapper:
    @staticmethod
    def to_domain(db_chat: Chat) -> BaseChatEntity:
        if db_chat.chat_type == ChatType.PRIVATE:
            return PrivateChatEntity(
                id=db_chat.id,
                creator_id=db_chat.creator_id,
                created_at=db_chat.created_at,
                chat_type=ChatType(db_chat.chat_type),
                private_hash=db_chat.private_hash,
            )

        return GroupChatEntity(
            id=db_chat.id,
            creator_id=db_chat.creator_id,
            created_at=db_chat.created_at,
            chat_type=ChatType(db_chat.chat_type),
            chat_name=db_chat.name,
        )
