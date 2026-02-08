"""Репозиторий для работы с сущностью сообщения."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.postgres.models.message import Message
from app.schemas.message import MessageCreate


class MessageRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_message(self, message_data: MessageCreate) -> Message:
        new_message = Message(**message_data.model_dump())
        self._session.add(new_message)
        await self._session.commit()
        return new_message
