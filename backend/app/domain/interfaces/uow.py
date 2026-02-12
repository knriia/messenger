from abc import ABC, abstractmethod
from types import TracebackType

from app.domain.interfaces.chat_member_repo import IChatMemberRepository
from app.domain.interfaces.chat_repo import IChatRepository
from app.domain.interfaces.message_repo import IMessageRepository
from app.domain.interfaces.user_repo import IUserRepository


class IUnitOfWork(ABC):
    users: IUserRepository
    chats: IChatRepository
    members: IChatMemberRepository
    messages: IMessageRepository

    @abstractmethod
    async def __aenter__(self) -> "IUnitOfWork":
        pass

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        pass

    @abstractmethod
    async def commit(self):
        pass

    @abstractmethod
    async def rollback(self):
        pass
