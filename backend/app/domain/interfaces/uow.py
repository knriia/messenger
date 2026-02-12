from abc import ABC, abstractmethod
from app.domain.interfaces.user_repo import IUserRepository
from app.domain.interfaces.chat_repo import IChatRepository
from app.domain.interfaces.chat_member_repo import IChatMemberRepository
from app.domain.interfaces.message_repo import IMessageRepository

class IUnitOfWork(ABC):
    users: IUserRepository
    chats: IChatRepository
    members: IChatMemberRepository
    messages: IMessageRepository

    @abstractmethod
    async def __aenter__(self) -> "IUnitOfWork":
        pass

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    @abstractmethod
    async def commit(self):
        pass

    @abstractmethod
    async def rollback(self):
        pass
