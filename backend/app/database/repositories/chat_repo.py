import hashlib
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app. database.models.chat import Chat


class ChatRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    @staticmethod
    def _generate_private_hash(user_ids: list[int]) -> str:
        sorted_ids = sorted(user_ids)
        hash_str = ''.join(map(str, sorted_ids))
        return hashlib.md5(hash_str.encode()).hexdigest()

    async def get_private_chat_by_hash(self, user_ids: list[int]) -> Chat | None:
        chat_hash = self._generate_private_hash(user_ids=user_ids)
        stmt = select(Chat).where(Chat.private_hash == chat_hash, Chat.chat_type == 'private')
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_chat(
        self,
        creator_id: int,
        chat_type: str,
        name: str | None = None,
        user_ids: list[int] = None
    ) -> Chat:
        p_hash = self._generate_private_hash(user_ids) if chat_type == "private" else None

        new_chat = Chat(
            creator_id=creator_id,
            chat_type=chat_type,
            private_hash=p_hash,
            name="Saved Messages" if len(user_ids) == 1 else name
        )
        self._session.add(new_chat)
        await self._session.flush()
        return new_chat
