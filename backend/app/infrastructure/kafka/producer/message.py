"""Сервис отправки сообщений в Kafka."""
from typing import Any

from aiokafka import AIOKafkaProducer
import json

from app.domain.interfaces.broker import IMessageBroker


class KafkaMessageBroker(IMessageBroker):
    def __init__(self, producer: AIOKafkaProducer, topic: str):
        self.producer = producer
        self.topic = topic

    async def publish(self, key: str, value: Any) -> None:
        payload = json.dumps(value, default=str).encode("utf-8")
        await self.producer.send_and_wait(topic=self.topic, key=key.encode("utf-8"), value=payload)
