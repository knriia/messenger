import logging

from app.domain.interfaces.uow import IUnitOfWork
from app.domain.entities.message_entity import MessageEntity
from app.domain.interfaces.broker import IMessageBroker


logger = logging.getLogger(__name__)


class MessageService:
    def __init__(self, uow: IUnitOfWork, kafka_producer: IMessageBroker):
        self.uow = uow
        self.kafka_producer = kafka_producer

    async def send_message(self, chat_id: int, sender_id: int, content: str) -> MessageEntity:
        async with self.uow:
            message = await self.uow.messages.create_message(
                chat_id=chat_id,
                sender_id=sender_id,
                content=content
            )
            await self.uow.commit()

        try:
            await self.kafka_producer.publish(key=str(chat_id), value=message.to_dict())
        except Exception as e:
            logger.error(f"Failed to publish message to Kafka: {e}")

        return message
