"""Провайдер бизнес-логики: сборка сервисов чата и аутентификации."""

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.repositories.message_repo import MessageRepository
from app.infrastructure.kafka.producer.message import MessageKafkaProducer
from app.services.message import MessageService
from app.services.connection_manager import ConnectionManager


class MessageProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_message_repository(self, session: AsyncSession) -> MessageRepository:
        return MessageRepository(session=session)

    @provide(scope=Scope.REQUEST)
    def get_message_service(self, kafka_producer: MessageKafkaProducer) -> MessageService:
        return MessageService(kafka_producer=kafka_producer)

    @provide(scope=Scope.APP)
    def get_connection_manager(self) -> ConnectionManager:
        return ConnectionManager()
