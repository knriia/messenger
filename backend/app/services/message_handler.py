import json
from redis.asyncio import Redis
from app.domain.interfaces.chat_member_repo import IChatMemberRepository
from app.schemas.notification import RedisChatNotification
from app.core.config import Settings

class MessageHandler:
    def __init__(
        self,
        member_repo: IChatMemberRepository,
        redis: Redis,
        settings: Settings
    ):
        self.member_repo = member_repo
        self.redis = redis
        self.settings = settings

    async def handle(self, raw_payload: bytes):
        data = json.loads(raw_payload.decode('utf-8'))
        chat_id = data.get("chat_id")

        recipient_ids = await self.member_repo.get_chat_member_ids(chat_id)

        notification = RedisChatNotification(
            recipient_ids=recipient_ids,
            payload=data
        )

        await self.redis.publish(
            self.settings.REDIS_CHAT_CHANNEL,
            notification.model_dump_json()
        )
