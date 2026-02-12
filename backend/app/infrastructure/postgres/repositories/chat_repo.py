from typing import cast

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.chat_entity import PrivateChatEntity
from app.domain.interfaces.chat_repo import IChatRepository
from app.infrastructure.postgres.mappers.chat_mapper import ChatMapper
from app.infrastructure.postgres.models.chat import Chat
from app.domain.consts import ChatType
from app.domain.logic import generate_private_chat_hash


class ChatRepository(IChatRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_private_chat_by_hash(self, user_ids: list[int]) -> PrivateChatEntity | None:
        chat_hash = generate_private_chat_hash(user_ids=user_ids)
        stmt = select(Chat).where(Chat.private_hash == chat_hash, Chat.chat_type == ChatType.PRIVATE)
        result = await self._session.execute(stmt)
        db_chat = result.scalar_one_or_none()
        if not db_chat:
            return None

        return cast(PrivateChatEntity, ChatMapper.to_domain(db_chat))

    async def create_private_chat(self, creator_id: int, user_ids: list[int]) -> PrivateChatEntity:
        new_chat = Chat(
            creator_id=creator_id,
            chat_type=ChatType.PRIVATE,
            private_hash=generate_private_chat_hash(user_ids),
        )
        self._session.add(new_chat)
        await self._session.flush()
        return cast(PrivateChatEntity, ChatMapper.to_domain(new_chat))
