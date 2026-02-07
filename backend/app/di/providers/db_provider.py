"""Провайдер доступа к данным: управление сессиями и репозиториями."""

from typing import AsyncGenerator

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.repositories.chat_member_repo import ChatMemberRepository
from app.database.repositories.chat_repo import ChatRepository
from app.database.repositories.message_repo import MessageRepository
from app.database.repositories.user_repo import UserRepository
from app.database.session import DatabaseSessionManager
from app.core.config import Settings
from app.database.uow import UnitOfWork


class DBProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_session_manager(self, settings: Settings) -> AsyncGenerator[DatabaseSessionManager, None]:
        db_manager = DatabaseSessionManager(settings.db_url)
        yield db_manager
        await db_manager.close()

    @provide(scope=Scope.REQUEST)
    async def get_session(self, db_manager: DatabaseSessionManager) -> AsyncGenerator[AsyncSession, None]:
        async with db_manager.get_session() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    def get_uow(
        self,
        session: AsyncSession,
        chats: ChatRepository,
        members: ChatMemberRepository,
        messages: MessageRepository,
        users: UserRepository,
    ) -> UnitOfWork:
        return UnitOfWork(
            session=session,
            chats=chats,
            members=members,
            messages=messages,
            users=users,
        )
