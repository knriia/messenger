"""Репозиторий для работы сущности сообщения."""

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.message_entity import MessageCreateEntity, MessageEntity
from app.domain.interfaces.message_repo import IMessageRepository
from app.infrastructure.postgres.mappers.message_mapper import MessageMapper
from app.infrastructure.postgres.models.message import Message


class MessageRepository(IMessageRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_message(self, message_data: MessageCreateEntity) -> MessageEntity:
        new_message = Message(**message_data.to_dict())
        self._session.add(new_message)
        await self._session.flush()
        return MessageMapper.to_domain(new_message)

    async def get_history(self, chat_id: int, limit: int = 20, cursor: int | None = None) -> list[MessageEntity]:
        stmt = select(Message).where(Message.chat_id == chat_id).order_by(desc(Message.id)).limit(limit=limit)
        if cursor:
            stmt = stmt.where(Message.id < cursor)

        result = await self._session.execute(stmt)
        return [MessageMapper.to_domain(m) for m in result.scalars().all()]
