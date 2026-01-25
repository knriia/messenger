from sqlalchemy.ext.asyncio import AsyncSession

from app.database.repositories.message import MessageRepository
from app.schemas.message import MessageCreate
from app.database.models import Message


class ChatService:
    def __init__(self, session: AsyncSession):
        self.message_repo = MessageRepository(session)

    async def save_message(self, message_data: MessageCreate) -> Message:
        return await self.message_repo.create(message_data=message_data)


    async def get_recent_messages(self, limit: int = 50) -> list[Message]:
        return await self.message_repo.get_recent(limit)
