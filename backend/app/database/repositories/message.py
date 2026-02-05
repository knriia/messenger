from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.message import Message
from app.schemas.message import MessageCreateDTO


class MessageRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_message(self, message_data: MessageCreateDTO) -> Message:
        new_message = Message(**message_data.model_dump())
        self._session.add(new_message)
        await self._session.commit()
        return new_message
