"""Провайдер доступа к данным: управление сессиями и репозиториями."""

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.postgres.repositories.user_repo import UserRepository
from app.core.config import Settings
from app.services.auth import AuthService
from app.services.security import SecurityService


class UserProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_user_repository(self, session: AsyncSession) -> UserRepository:
        return UserRepository(session=session)

    @provide(scope=Scope.REQUEST)
    def get_auth_service(self, user_repo: UserRepository, security: SecurityService) -> AuthService:
        return AuthService(user_repository=user_repo, security_service=security)

    @provide(scope=Scope.APP)
    def get_security_service(self, settings: Settings) -> SecurityService:
        return SecurityService(settings=settings)
