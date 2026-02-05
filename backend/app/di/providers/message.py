"""Провайдер бизнес-логики: сборка сервисов чата и аутентификации."""

from dishka import Provider, Scope, provide

from app.core.config import Settings
from app.database.repositories.user import UserRepository
from app.infrastructure.kafka.producer.message import MessageKafkaProducer
from app.services.auth import AuthService
from app.services.message.chat import ChatService
from app.services.connection_manager import ConnectionManager
from app.services.security import SecurityService


class MessageProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_auth_service(self, user_repository: UserRepository,  security_service: SecurityService) -> AuthService:
        return AuthService(user_repository=user_repository, security_service=security_service)

    @provide(scope=Scope.REQUEST)
    def get_chat_service(
        self,
        message_kafka_producer: MessageKafkaProducer,
        connection_manager: ConnectionManager
    ) -> ChatService:
        return ChatService(
            message_kafka_producer=message_kafka_producer,
            connection_manager=connection_manager
        )

    @provide(scope=Scope.APP)
    def get_connection_manager(self) -> ConnectionManager:
        return ConnectionManager()

    @provide(scope=Scope.APP)
    def get_security_service(self, settings: Settings) -> SecurityService:
        return SecurityService(settings=settings)
