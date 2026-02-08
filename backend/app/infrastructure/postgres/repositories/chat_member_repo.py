from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.postgres.models.chat_member import ChatMember


class ChatMemberRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_chat_member_ids(self, chat_id: int) -> list[int]:
        stmt = select(ChatMember.user_id).where(ChatMember.chat_id == chat_id)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def add_chat_member(self, chat_id: int, user_id: int, role: str = "member"):
        new_member = ChatMember(
            chat_id=chat_id,
            user_id=user_id,
            role=role
        )
        self._session.add(new_member)
        await self._session.flush()
