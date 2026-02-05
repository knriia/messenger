"""Менеджер сессий базы данных."""

from typing import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, async_sessionmaker, create_async_engine


class DatabaseSessionManager:
    def __init__(self):
        self._engine: AsyncEngine | None = None
        self._sessionmaker: async_sessionmaker | None = None
        self._initialized = False

    def init(self, database_url: str):
        if self._initialized:
            return

        self._engine = create_async_engine(
            database_url
        )

        self._sessionmaker = async_sessionmaker(
            bind=self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False
        )
        self._initialized = True

    async def close(self):
        if self._engine is not None:
            await self._engine.dispose()
            self._engine = None
            self._sessionmaker = None
            self._initialized = False

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        if not self._initialized:
            raise RuntimeError("DatabaseSessionManager is not initialized")

        if self._sessionmaker is None:
            raise RuntimeError("SessionMaker is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise
        finally:
            await session.close()

    @property
    def engine(self) -> AsyncEngine:
        if self._engine is None:
            raise RuntimeError("Engine is not initialized")
        return self._engine

    @property
    def sessionmaker(self) -> async_sessionmaker:
        if self._sessionmaker is None:
            raise RuntimeError("SessionMaker is not initialized")
        return self._sessionmaker
