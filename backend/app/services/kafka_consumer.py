"""Сервис прослушивания сообщений Kafka."""

import asyncio

from aiokafka import AIOKafkaConsumer
import json
import logging

from aiokafka.errors import GroupCoordinatorNotAvailableError
from dishka import AsyncContainer

from app.database.repositories.message import MessageRepository
from app.schemas.message import MessageCreate

logger = logging.getLogger(__name__)


class KafkaConsumerService:
    def __init__(self, consumer: AIOKafkaConsumer):
        self.consumer = consumer

    async def start(self, container: AsyncContainer):
        while True:
            try:
                await self.consumer.start()
                logger.info("✅ Kafka Consumer connected and started")
                break
            except (GroupCoordinatorNotAvailableError, ConnectionError):
                logger.warning("⏳ Kafka Coordinator not available, retrying in 5s...")
                await asyncio.sleep(5)

        try:
            async for msg in self.consumer:
                async with container() as request_container:
                    try:
                        data = json.loads(msg.value.decode('utf-8'))
                        message_dto = MessageCreate(**data)
                        message_repo = await request_container.get(MessageRepository)
                        await message_repo.create_message(message_data=message_dto)
                    except Exception as e:
                        logger.error(f"❌ Error processing message: {e}")
        finally:
            await self.consumer.stop()
