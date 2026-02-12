import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from dishka import AsyncContainer
from app.infrastructure.redis.listener import RedisNotificationListener


def setup_lifespan(container: AsyncContainer):
    @asynccontextmanager
    async def lifespan(_: FastAPI):
        listener = await container.get(RedisNotificationListener)
        listener_task = asyncio.create_task(listener.listen())
        yield
        listener_task.cancel()
        try:
            await listener_task
        except asyncio.CancelledError:
            pass

        await container.close()

    return lifespan
