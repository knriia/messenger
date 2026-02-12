"""Провайдер сервисов чата."""

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.interfaces.chat_member_repo import IChatMemberRepository
from app.domain.interfaces.chat_repo import IChatRepository
from app.infrastructure.postgres.repositories.chat_repo import ChatRepository
from app.infrastructure.postgres.repositories.chat_member_repo import ChatMemberRepository
from app.domain.interfaces.uow import IUnitOfWork
from app.services.chat_management import ChatManagementService


class ChatProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_chat_management_service(
        self,
        uow: IUnitOfWork,
    ) -> ChatManagementService:
        return ChatManagementService(uow=uow)

    @provide(scope=Scope.REQUEST)
    def get_chat_repository(self, session: AsyncSession) -> IChatRepository:
        return ChatRepository(session=session)

    @provide(scope=Scope.REQUEST)
    def get_member_repository(self, session: AsyncSession) -> IChatMemberRepository:
        return ChatMemberRepository(session=session)
