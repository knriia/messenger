import logging

from app.domain.entities.message_entity import MessageCreateEntity, MessageEntity
from app.domain.interfaces.broker import IMessageBroker
from app.domain.interfaces.uow import IUnitOfWork

logger = logging.getLogger(__name__)


class MessageService:
    def __init__(self, uow: IUnitOfWork, kafka_producer: IMessageBroker):
        self.uow = uow
        self.kafka_producer = kafka_producer

    async def send_message(self, message_data: MessageCreateEntity) -> MessageEntity:
        async with self.uow:
            message = await self.uow.messages.create_message(message_data=message_data)
            await self.uow.commit()

        try:
            await self.kafka_producer.publish(key=str(message.chat_id), value=message.to_dict())
        except Exception as e:
            logger.error(f"Failed to publish message to Kafka: {e}")

        return message
