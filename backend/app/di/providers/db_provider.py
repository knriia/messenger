"""Провайдер доступа к данным: управление сессиями и репозиториями."""

from typing import AsyncGenerator

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.postgres.session import DatabaseSessionManager
from app.core.config import Settings
from app.infrastructure.postgres.uow import UnitOfWork
from app.domain.interfaces.uow import IUnitOfWork


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
    def get_uow(self, session: AsyncSession) -> IUnitOfWork:
        return UnitOfWork(session=session)
