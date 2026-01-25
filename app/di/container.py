from fastapi import Request
from dishka import Provider, Scope, provide
from app.database.session import DatabaseSessionManager, AsyncSession
from app.services.chat import ChatService
from app.services.connection_manager import ConnectionManager
from typing import AsyncGenerator


class DatabaseProvider(Provider):
    # Scope.APP означает, что он будет создан один раз при запуске приложения.
    @provide(scope=Scope.APP)
    def get_db_manager(self, request: Request) -> DatabaseSessionManager:
        db_url = request.app.state.db_url
        manager = DatabaseSessionManager()
        manager.init(db_url)
        return manager

    # Scope.REQUEST означает, что новая сессия создается для каждого HTTP-запроса/WS-соединения.
    @provide(scope=Scope.REQUEST)
    async def get_session(self, manager: DatabaseSessionManager) -> AsyncGenerator[AsyncSession, None]:
        async with manager.get_session() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    def get_chat_service(self, session: AsyncSession) -> ChatService:
        return ChatService(session=session)

    @provide(scope=Scope.APP)
    def get_connection_manager(self) -> ConnectionManager:
        return ConnectionManager()
