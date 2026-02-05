"""Провайдер доступа к данным: управление сессиями и репозиториями."""

from typing import AsyncGenerator

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, async_sessionmaker
from app.database.session import DatabaseSessionManager
from app.database.repositories.user import UserRepository
from app.database.repositories.message import MessageRepository
from app.core.config import Settings


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
    def get_user_repository(self, session: AsyncSession) -> UserRepository:
        return UserRepository(session=session)

    @provide(scope=Scope.REQUEST)
    def get_message_repository(self, session: AsyncSession) -> MessageRepository:
        return MessageRepository(session=session)
