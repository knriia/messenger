"""Конфигурация глобального DI-контейнера."""

from dishka import AsyncContainer, make_async_container

from app.di.providers.chat_provider import ChatProvider
from app.di.providers.config_provider import ConfigProvider
from app.di.providers.db_provider import DBProvider
from app.di.providers.kafka_provider import KafkaProvider
from app.di.providers.message_provider import MessageProvider
from app.di.providers.redis_provider import RedisProvider
from app.di.providers.user_provider import UserProvider


def get_container() -> AsyncContainer:
    return make_async_container(
        ChatProvider(),
        ConfigProvider(),
        DBProvider(),
        KafkaProvider(),
        MessageProvider(),
        RedisProvider(),
        UserProvider(),
    )
