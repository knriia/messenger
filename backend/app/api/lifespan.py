import asyncio
import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
from dishka import AsyncContainer
from redis.asyncio import Redis
from app.services.connection_manager import ConnectionManager
from app.core.config import Settings
from app.schemas.notification import RedisChatNotification


logger = logging.getLogger(__name__)


async def redis_listener(container: AsyncContainer):
    redis = await container.get(Redis)
    manager = await container.get(ConnectionManager)
    settings = await container.get(Settings)
    pubsub = redis.pubsub()
    await pubsub.subscribe(settings.REDIS_NOTIFICATIONS_CHANNEL)
    try:
        async for message in pubsub.listen():
            if message['type'] != 'message':
                continue
            try:
                notification = RedisChatNotification.model_validate_json(message['data'])

                tasks = [
                    manager.send_to_user(user_id, notification.payload)
                    for user_id in notification.recipient_ids
                ]
                if tasks:
                    await asyncio.gather(*tasks)

            except Exception as e:
                logger.error(f"Ошибка при обработке сообщения из Redis: {e}")
    except asyncio.CancelledError:
        await pubsub.unsubscribe("chat_notifications")
        await pubsub.close()


def setup_lifespan(container: AsyncContainer):
    @asynccontextmanager
    async def lifespan(_: FastAPI):
        listener_task = asyncio.create_task(redis_listener(container))
        yield
        listener_task.cancel()
        try:
            await listener_task
        except asyncio.CancelledError:
            pass

        await container.close()

    return lifespan
