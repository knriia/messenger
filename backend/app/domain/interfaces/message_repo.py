from abc import ABC, abstractmethod

from app.domain.entities.message_entity import MessageCreateEntity, MessageEntity


class IMessageRepository(ABC):
    @abstractmethod
    async def create_message(self, message_data: MessageCreateEntity) -> MessageEntity:
        pass

    @abstractmethod
    async def get_history(self, chat_id: int, limit: int = 20, cursor: int | None = None) -> list[MessageEntity]:
        pass
