"""Провайдер для завсисимостей Redis"""

from redis.asyncio import Redis
from dishka import Scope, Provider, provide
from app.core.config import Settings
from app.infrastructure.redis.listener import RedisNotificationListener
from app.services.connection_manager import ConnectionManager


class RedisProvider(Provider):
    @provide(scope=Scope.APP)
    def get_redis_client(self, settings: Settings) -> Redis:
        return Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=0,
            decode_responses=True
        )

    @provide(scope=Scope.APP)
    def get_redis_listener(
        self,
        redis: Redis,
        manager: ConnectionManager,
        settings: Settings
    ) -> RedisNotificationListener:
        return RedisNotificationListener(redis, manager, settings)
