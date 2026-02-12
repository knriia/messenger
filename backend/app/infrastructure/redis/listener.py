import asyncio
import logging
from redis.asyncio import Redis
from app.services.connection_manager import ConnectionManager
from app.core.config import Settings
from app.schemas.notification import RedisChatNotification

logger = logging.getLogger(__name__)


class RedisNotificationListener:
    def __init__(
        self,
        redis: Redis,
        manager: ConnectionManager,
        settings: Settings
    ):
        self.redis = redis
        self.manager = manager
        self.settings = settings

    async def listen(self):
        pubsub = self.redis.pubsub()
        await pubsub.subscribe(self.settings.REDIS_NOTIFICATIONS_CHANNEL)

        logger.info("✅ Started listening for Redis notifications")
        try:
            async for message in pubsub.listen():
                if message['type'] != 'message':
                    continue

                try:
                    notification = RedisChatNotification.model_validate_json(message['data'])

                    tasks = [
                        self.manager.send_to_user(user_id, notification.payload)
                        for user_id in notification.recipient_ids
                    ]
                    if tasks:
                        await asyncio.gather(*tasks, return_exceptions=True)

                except Exception as e:
                    logger.error(f"Error processing Redis notification: {e}")
        except asyncio.CancelledError:
            await pubsub.unsubscribe(self.settings.REDIS_NOTIFICATIONS_CHANNEL)
            await pubsub.close()
            logger.info("🛑 Redis listener stopped")