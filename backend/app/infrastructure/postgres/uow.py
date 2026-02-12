from types import TracebackType

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.interfaces.uow import IUnitOfWork
from app.infrastructure.postgres.repositories.chat_member_repo import ChatMemberRepository
from app.infrastructure.postgres.repositories.chat_repo import ChatRepository
from app.infrastructure.postgres.repositories.message_repo import MessageRepository
from app.infrastructure.postgres.repositories.user_repo import UserRepository


class UnitOfWork(IUnitOfWork):
    def __init__(self, session: AsyncSession):
        self._session = session
        self.chats = ChatRepository(session=self._session)
        self.members = ChatMemberRepository(session=self._session)
        self.messages = MessageRepository(session=self._session)
        self.users = UserRepository(session=self._session)

    async def __aenter__(self) -> "UnitOfWork":
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if exc_type:
            await self.rollback()
        else:
            await self.commit()

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()
