"""Сервис управления чатом."""

from app.schemas.message import MessageCreate
from app.services.connection_manager import ConnectionManager
from app.infrastructure.kafka.producer.message import MessageKafkaProducer


class ChatService:
    def __init__(
        self,
        message_kafka_producer: MessageKafkaProducer,
        connection_manager: ConnectionManager
    ):
        self.message_kafka_producer = message_kafka_producer
        self.connection_manager = connection_manager

    async def send_new_message(self, message_data: MessageCreate) -> dict[str, str]:
        await self.message_kafka_producer.send_message(message_data=message_data)

        payload = {
            "type": 'new_message',
            "content": message_data.content,
            "sender_id": message_data.sender_id,
            "chat_id": message_data.chat_id
        }
        await self.connection_manager.send_to_user(message_data.sender_id, payload)

        return {"status": "sent", "message_id": "queued"}