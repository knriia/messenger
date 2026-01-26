from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Message
from app.schemas.message import MessageCreate


class MessageRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, message_data: MessageCreate) -> Message:
        stmt = insert(Message).values(**message_data.model_dump()).returning(Message)
        result = await self._session.execute(stmt)
        await self._session.commit()
        return result.scalar_one()

    async def get_recent(self, limit: int = 50) -> list[Message]:
        query = select(Message).order_by(Message.created_at.desc()).limit(limit)
        result = await self._session.execute(query)
        return result.scalars().all()

    async def get_by_id(self, message_id: int) -> Message | None:
        result = await self._session.execute(select(Message).where(Message.id == message_id))
        return result.scalar_one_or_none()
