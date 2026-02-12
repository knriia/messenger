"""Менеджер сессий базы данных."""

from typing import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, async_sessionmaker, create_async_engine


class DatabaseSessionManager:
    def __init__(self, db_url: str):
        self._engine: AsyncEngine = create_async_engine(db_url)
        self._session_maker: async_sessionmaker = async_sessionmaker(
            bind=self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False
        )

    async def close(self):
        if self._engine is not None:
            await self._engine.dispose()

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self._session_maker() as session:
            yield session
