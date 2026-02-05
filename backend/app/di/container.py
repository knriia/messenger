"""Конфигурация глобального DI-контейнера."""

from dishka import make_async_container

from app.di.providers.config import ConfigProvider
from app.di.providers.db import DBProvider
from app.di.providers.kafka import KafkaProvider
from app.di.providers.message import MessageProvider


def get_container():
    return make_async_container(
        ConfigProvider(),
        DBProvider(),
        KafkaProvider(),
        MessageProvider(),
    )
