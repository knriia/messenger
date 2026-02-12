from abc import ABC, abstractmethod


class IChatMemberRepository(ABC):
    @abstractmethod
    async def get_chat_member_ids(self, chat_id: int) -> list[int]:
        pass

    @abstractmethod
    async def add_chat_member(self, chat_id: int, user_id: int, role: str) -> None:
        pass
