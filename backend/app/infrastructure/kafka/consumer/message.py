import asyncio
import logging
from aiokafka import AIOKafkaConsumer
from aiokafka.errors import GroupCoordinatorNotAvailableError
from dishka import AsyncContainer
from app.domain.interfaces.processor import IMessageProcessor
from app.services.message_handler import MessageHandler

logger = logging.getLogger(__name__)

class KafkaMessageProcessor(IMessageProcessor):
    def __init__(self, consumer: AIOKafkaConsumer, container: AsyncContainer):
        self.consumer = consumer
        self.container = container

    async def start(self) -> None:
        logger.info("✅ Kafka Consumer is ready and listening")
        try:
            async for msg in self.consumer:
                async with self.container() as request_container:
                    try:
                        handler = await request_container.get(MessageHandler)
                        await handler.handle(msg.value)
                    except Exception as e:
                        logger.error(f"❌ Error processing message: {e}")
        finally:
            await self.consumer.stop()
