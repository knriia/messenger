from fastapi import Request
from dishka import Provider, Scope, provide
from app.database.session import DatabaseSessionManager, AsyncSession, AsyncEngine
from app.services.chat import ChatService
from app.services.connection_manager import ConnectionManager
from typing import AsyncGenerator
from app.core.config import Settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


class DatabaseProvider(Provider):
    # Scope.APP означает, что он будет создан один раз при запуске приложения.
    @provide(scope=Scope.APP)
    def get_settings(self) -> Settings:
        return Settings()

    @provide(scope=Scope.APP)
    def get_engine(self, settings: Settings) -> AsyncEngine:
        return create_async_engine(settings.db_url)

    @provide(scope=Scope.APP)
    def get_session_factory(self, engine: AsyncEngine) -> async_sessionmaker:
        return async_sessionmaker(engine, expire_on_commit=False)

    # Scope.REQUEST означает, что новая сессия создается для каждого HTTP-запроса/WS-соединения.
    @provide(scope=Scope.REQUEST)
    async def get_session(
            self,
            session_factory: async_sessionmaker[AsyncSession]
    ) -> AsyncGenerator[AsyncSession, None]:
        async with session_factory() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    def get_chat_service(self, session: AsyncSession) -> ChatService:
        return ChatService(session=session)

    @provide(scope=Scope.APP)
    def get_connection_manager(self) -> ConnectionManager:
        return ConnectionManager()
