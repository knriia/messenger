"""Провайдер доступа к данным: управление сессиями и репозиториями."""

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings
from app.domain.interfaces.security import ISecurityService
from app.domain.interfaces.uow import IUnitOfWork
from app.domain.interfaces.user_repo import IUserRepository
from app.infrastructure.postgres.repositories.user_repo import UserRepository
from app.services.auth import AuthService
from app.services.security import SecurityService
from app.services.user import UserService


class UserProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_user_repository(self, session: AsyncSession) -> IUserRepository:
        return UserRepository(session=session)

    @provide(scope=Scope.REQUEST)
    def get_auth_service(
        self, user_repo: IUserRepository, security: ISecurityService, settings: Settings
    ) -> AuthService:
        return AuthService(user_repository=user_repo, security_service=security, token_type=settings.TOKEN_TYPE_BEARER)

    @provide(scope=Scope.APP)
    def get_security_service(self, settings: Settings) -> ISecurityService:
        return SecurityService(
            secret_key=settings.SECRET_KEY,
            algorithm=settings.ALGORITHM,
            expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        )

    @provide(scope=Scope.REQUEST)
    def get_user_service(self, uow: IUnitOfWork) -> UserService:
        return UserService(uow=uow)
