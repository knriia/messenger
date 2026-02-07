from sqlalchemy.ext.asyncio import AsyncSession

from app.database.repositories.chat_repo import ChatRepository
from app.database.repositories.chat_member_repo import ChatMemberRepository
from app.database.repositories.message_repo import MessageRepository
from app.database.repositories.user_repo import UserRepository


class UnitOfWork:
    def __init__(
        self,
        session: AsyncSession,
        chats: ChatRepository,
        members: ChatMemberRepository,
        messages: MessageRepository,
        users: UserRepository,
    ):
        self._session = session
        self.chats = chats
        self.members = members
        self.messages = messages
        self.users = users

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()

    async def refresh(self, obj):
        await self._session.refresh(obj)