"""Сервис прослушивания сообщений Kafka."""

import asyncio

from aiokafka import AIOKafkaConsumer
import json
import logging

from aiokafka.errors import GroupCoordinatorNotAvailableError
from dishka import AsyncContainer
from redis.asyncio import Redis

from app.core.config import Settings
from app.database.repositories.chat_member_repo import ChatMemberRepository
from app.database.repositories.message_repo import MessageRepository
from app.schemas.message import MessageCreate, MessageRead
from app.schemas.notification import RedisChatNotification

logger = logging.getLogger(__name__)


class MessageKafkaConsumer:
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
                        member_repo = await request_container.get(ChatMemberRepository)
                        saved_message = await message_repo.create_message(message_data=message_dto)
                        redis = await request_container.get(Redis)
                        settings = await request_container.get(Settings)
                        recipients = await member_repo.get_chat_member_ids(saved_message.chat_id)
                        notification = RedisChatNotification(
                            recipient_ids=recipients,
                            payload=MessageRead.model_validate(saved_message)
                        )
                        await redis.publish(
                            settings.REDIS_CHAT_CHANNEL,
                            notification.model_dump_json()
                        )
                    except Exception as e:
                        logger.error(f"❌ Error processing message: {e}")
        finally:
            await self.consumer.stop()
