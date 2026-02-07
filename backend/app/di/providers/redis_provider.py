"""Провайдер для завсисимостей Redis"""

from redis.asyncio import Redis
from dishka import Scope, Provider, provide
from app.core.config import Settings


class RedisProvider(Provider):
    @provide(scope=Scope.APP)
    def get_redis_client(self, settings: Settings) -> Redis:
        return Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=0,
            decode_responses=True
        )
