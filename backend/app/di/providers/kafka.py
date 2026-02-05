"""Провайдер инфраструктуры сообщений: Producer и Consumer."""

from typing import AsyncGenerator

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from dishka import Provider, Scope, provide

from app.core.config import Settings
from app.infrastructure.kafka.producer.message import MessageKafkaProducer
from app.infrastructure.kafka.consumer.message import MessageKafkaConsumer


class KafkaProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_aiokafka_producer(self, settings: Settings) -> AsyncGenerator[AIOKafkaProducer, None]:
        producer = AIOKafkaProducer(bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS)
        await producer.start()
        yield producer
        await producer.stop()

    @provide(scope=Scope.APP)
    def get_message_producer(self, producer: AIOKafkaProducer, settings: Settings) -> MessageKafkaProducer:
        return MessageKafkaProducer(producer=producer, topic=settings.KAFKA_MESSAGES_TOPIC)

    @provide(scope=Scope.APP)
    def get_aiokafka_consumer(self, setting: Settings) -> AIOKafkaConsumer:
        return AIOKafkaConsumer(
            setting.KAFKA_MESSAGES_TOPIC,
            bootstrap_servers=setting.KAFKA_BOOTSTRAP_SERVERS,
            group_id='messenger_group',
            auto_offset_reset='earliest'
        )

    @provide(scope=Scope.APP)
    def get_message_consumer(self, consumer: AIOKafkaConsumer) -> MessageKafkaConsumer:
        return MessageKafkaConsumer(consumer=consumer)
