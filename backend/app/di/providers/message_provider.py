from dishka import Provider, Scope, provide
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings
from app.domain.interfaces.broker import IMessageBroker
from app.domain.interfaces.chat_member_repo import IChatMemberRepository
from app.domain.interfaces.message_repo import IMessageRepository
from app.domain.interfaces.uow import IUnitOfWork
from app.infrastructure.postgres.repositories.message_repo import MessageRepository
from app.services.connection_manager import ConnectionManager
from app.services.message import MessageService
from app.services.message_handler import MessageHandler


class MessageProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_message_repository(self, session: AsyncSession) -> IMessageRepository:
        return MessageRepository(session=session)

    @provide(scope=Scope.REQUEST)
    def get_message_handler(
        self, member_repo: IChatMemberRepository, redis: Redis, settings: Settings
    ) -> MessageHandler:
        return MessageHandler(member_repo=member_repo, redis=redis, settings=settings)

    @provide(scope=Scope.REQUEST)
    def get_message_service(self, uow: IUnitOfWork, kafka_producer: IMessageBroker) -> MessageService:
        return MessageService(uow=uow, kafka_producer=kafka_producer)

    @provide(scope=Scope.APP)
    def get_connection_manager(self) -> ConnectionManager:
        return ConnectionManager()
