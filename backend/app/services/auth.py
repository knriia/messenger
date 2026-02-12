"""Сервис аутентификации и авторизации."""


from app.domain.entities.user_entity import UserEntity
from app.domain.exceptions.auth import UserAlreadyExistsError, InvalidCredentialsError
from app.domain.interfaces.security import ISecurityService
from app.domain.interfaces.user_repo import IUserRepository
from app.schemas.token import TokenPayload


class AuthService:
    def __init__(self, user_repository: IUserRepository, security_service: ISecurityService):
        self.repository = user_repository
        self.security_service = security_service

    async def register_user(self, username: str, password: str) -> UserEntity:
        existing_user = await self.repository.get_by_username(username)
        if existing_user:
            raise UserAlreadyExistsError()

        hashed = self.security_service.hash_password(password)

        return await self.repository.create_user(
            username=username,
            hashed_password=hashed,
        )

    async def login(self, username: str, password: str) -> str:
        user = await self.repository.get_by_username(username=username)

        if not user or not self.security_service.verify_password(password, user.hashed_password):
            raise InvalidCredentialsError()

        payload = TokenPayload(sub=user.username, user_id=user.id)
        return self.security_service.create_access_token(payload=payload)
