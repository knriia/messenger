"""Провайдер инфраструктуры сообщений: Producer и Consumer."""

from typing import AsyncGenerator

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from dishka import Provider, Scope, provide, AsyncContainer

from app.core.config import Settings
from app.domain.interfaces.broker import IMessageBroker
from app.domain.interfaces.processor import IMessageProcessor
from app.infrastructure.kafka.producer.message import KafkaMessageBroker
from app.infrastructure.kafka.consumer.message import KafkaMessageProcessor


class KafkaProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_aiokafka_producer(self, settings: Settings) -> AsyncGenerator[AIOKafkaProducer, None]:
        producer = AIOKafkaProducer(bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS)
        await producer.start()
        yield producer
        await producer.stop()

    @provide(scope=Scope.APP)
    async def get_aiokafka_consumer(self, setting: Settings) -> AsyncGenerator[AIOKafkaConsumer, None]:
        consumer = AIOKafkaConsumer(
            setting.KAFKA_MESSAGES_TOPIC,
            bootstrap_servers=setting.KAFKA_BOOTSTRAP_SERVERS,
            group_id='messenger_group',
            auto_offset_reset='earliest'
        )
        await consumer.start()
        yield consumer
        await consumer.stop()

    @provide(scope=Scope.APP)
    def get_message_broker(self, producer: AIOKafkaProducer, settings: Settings) -> IMessageBroker:
        return KafkaMessageBroker(producer=producer, topic=settings.KAFKA_MESSAGES_TOPIC)

    @provide(scope=Scope.APP)
    def get_message_processor(
        self,
        consumer: AIOKafkaConsumer,
        container: AsyncContainer
    ) -> IMessageProcessor:
        return KafkaMessageProcessor(consumer=consumer, container=container)
