"""Сервис управления чатом."""

from app.schemas.message import MessageCreate
from app.infrastructure.kafka.producer.message import MessageKafkaProducer


class MessageService:
    def __init__(
        self,
        kafka_producer: MessageKafkaProducer,
    ):
        self.kafka_producer = kafka_producer

    async def send_message(self, message_data: MessageCreate) -> dict:
        await self.kafka_producer.send_message(message_data=message_data)

        return {"status": "accepted", "details": "message_queued"}