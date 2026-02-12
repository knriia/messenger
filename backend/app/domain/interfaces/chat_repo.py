from abc import ABC, abstractmethod

from app.domain.entities.chat_entity import PrivateChatEntity


class IChatRepository(ABC):
    @abstractmethod
    async def get_private_chat_by_hash(self, user_ids: list[int]) -> PrivateChatEntity | None:
        pass

    async def create_private_chat(
        self,
        creator_id: int,
        user_ids: list[int]
    ) -> PrivateChatEntity:
        pass
