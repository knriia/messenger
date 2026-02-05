from typing import AsyncGenerator

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from dishka import Provider, Scope, provide
from app.services.kafka_producer import KafkaProducerService
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncEngine

from app.services.kafka_consumer import KafkaConsumerService
from app.services.security import SecurityService
from app.database.repositories.user import UserRepository
from app.services.auth import AuthService
from app.services.chat import ChatService
from app.services.connection_manager import ConnectionManager
from app.core.config import Settings

from app.database.repositories.message import MessageRepository


class KafkaProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_kafka_producer(self, settings: Settings) -> AsyncGenerator[AIOKafkaProducer, None]:
        producer = AIOKafkaProducer(bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS)
        await producer.start()
        yield producer
        await producer.stop()

    @provide(scope=Scope.APP)
    def get_kafka_producer_service(self, producer: AIOKafkaProducer, settings: Settings) -> KafkaProducerService:
        return KafkaProducerService(producer=producer, topic=settings.KAFKA_MESSAGES_TOPIC)

    @provide(scope=Scope.APP)
    async def get_kafka_consumer(self, setting: Settings) -> AsyncGenerator[AIOKafkaConsumer, None]:
        consumer = AIOKafkaConsumer(
            setting.KAFKA_MESSAGES_TOPIC,
            bootstrap_servers=setting.KAFKA_BOOTSTRAP_SERVERS,
            group_id="messenger_group",
            auto_offset_reset="earliest"
        )
        yield consumer
        try:
            await consumer.stop()
        except:
            pass

    @provide(scope=Scope.APP)
    def get_kafka_consumer_service(
        self,
        consumer: AIOKafkaConsumer,
    ) -> KafkaConsumerService:
        return KafkaConsumerService(consumer=consumer)


class DatabaseProvider(Provider):
    # Scope.APP означает, что он будет создан один раз при запуске приложения.
    @provide(scope=Scope.APP)
    def get_settings(self) -> Settings:
        return Settings()

    @provide(scope=Scope.APP)
    def get_engine(self, settings: Settings) -> AsyncEngine:
        return create_async_engine(settings.db_url)

    @provide(scope=Scope.APP)
    def get_session_factory(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(engine, expire_on_commit=False)

    # Scope.REQUEST означает, что новая сессия создается для каждого HTTP-запроса/WS-соединения.
    @provide(scope=Scope.SESSION)
    async def get_session(
        self,
        session_factory: async_sessionmaker[AsyncSession]
    ) -> AsyncGenerator[AsyncSession, None]:
        async with session_factory() as session:
            yield session

    @provide(scope=Scope.SESSION)
    def get_chat_service(
        self,
        kafka_producer_service: KafkaProducerService,
        connection_manager: ConnectionManager
    ) -> ChatService:
        return ChatService(kafka_producer_service=kafka_producer_service, connection_manager=connection_manager)

    @provide(scope=Scope.APP)
    def get_connection_manager(self) -> ConnectionManager:
        return ConnectionManager()

    @provide(scope=Scope.APP)
    def get_security_service(self, settings: Settings) -> SecurityService:
        return SecurityService(settings=settings)

    @provide(scope=Scope.SESSION)
    def get_user_repository(self, session: AsyncSession) -> UserRepository:
        return UserRepository(session=session)

    @provide(scope=Scope.SESSION)
    def get_auth_service(self, repository: UserRepository, security_service: SecurityService) -> AuthService:
        return AuthService(repository=repository, security_service=security_service)

    @provide(scope=Scope.SESSION)
    def get_message_repository(self, session: AsyncSession) -> MessageRepository:
        return MessageRepository(session=session)
