"""Сервис аутентификации и авторизации."""

from app.domain.entities.token import TokenEntity, TokenPayloadEntity
from app.domain.entities.user_entity import UserCreateEntity, UserEntity, UserStoreEntity
from app.domain.exceptions.auth import InvalidCredentialsError, UserAlreadyExistsError
from app.domain.interfaces.security import ISecurityService
from app.domain.interfaces.user_repo import IUserRepository


class AuthService:
    def __init__(self, user_repository: IUserRepository, security_service: ISecurityService, token_type: str):
        self.repository = user_repository
        self.security_service = security_service
        self.token_type = token_type

    async def register_user(self, user_data: UserCreateEntity) -> UserEntity:
        existing_user = await self.repository.get_by_username(user_data.username)
        if existing_user:
            raise UserAlreadyExistsError()

        user_dict = user_data.to_dict()
        user_dict.pop("password")
        hashed_pw = self.security_service.hash_password(user_data.password)
        store_entity = UserStoreEntity(**user_dict, hashed_password=hashed_pw)
        return await self.repository.create_user(store_entity)

    async def login(self, username: str, password: str) -> TokenEntity:
        user = await self.repository.get_with_password_by_username(username=username)

        if not user:
            raise InvalidCredentialsError()

        if not self.security_service.verify_password(password, user.hashed_password):
            raise InvalidCredentialsError()

        payload = TokenPayloadEntity(sub=user.username, user_id=user.id)
        token_str = self.security_service.create_access_token(payload)
        return TokenEntity(access_token=token_str, token_type=self.token_type)
