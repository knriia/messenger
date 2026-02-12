import asyncio
from collections.abc import AsyncIterator, Callable
from contextlib import AbstractAsyncContextManager, asynccontextmanager, suppress

from dishka import AsyncContainer
from fastapi import FastAPI

from app.infrastructure.redis.listener import RedisNotificationListener

LifespanType = Callable[[FastAPI], AbstractAsyncContextManager[None]]


def setup_lifespan(container: AsyncContainer) -> LifespanType:
    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        listener = await container.get(RedisNotificationListener)
        listener_task = asyncio.create_task(listener.listen())
        yield
        listener_task.cancel()
        with suppress(asyncio.CancelledError):
            await listener_task

        await container.close()

    return lifespan
