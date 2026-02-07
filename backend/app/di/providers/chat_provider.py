"""Провайдер сервисов чата."""

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.repositories.chat_repo import ChatRepository
from app.database.repositories.chat_member_repo import ChatMemberRepository
from app.services.chat_management import ChatManagementService


class ChatProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_chat_management_service(
        self,
        chat_repo: ChatRepository,
        member_repo: ChatMemberRepository
    ) -> ChatManagementService:
        return ChatManagementService(chat_repo=chat_repo, member_repo=member_repo)

    @provide(scope=Scope.REQUEST)
    def get_chat_repository(self, session: AsyncSession) -> ChatRepository:
        return ChatRepository(session=session)

    @provide(scope=Scope.REQUEST)
    def get_member_repository(self, session: AsyncSession) -> ChatMemberRepository:
        return ChatMemberRepository(session=session)
