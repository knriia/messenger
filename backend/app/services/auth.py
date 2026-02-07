"""Сервис аутентификации и авторизации."""

from fastapi import HTTPException, status
from app.database.repositories.user_repo import UserRepository
from app.schemas.token import TokenPayload
from app.schemas.user import UserCreate
from app.services.security import SecurityService
from app.database.models.user import User


class AuthService:
    def __init__(self, user_repository: UserRepository, security_service: SecurityService):
        self.repository = user_repository
        self.security_service = security_service

    async def register_user(self, user_data: UserCreate) -> User:
        existing_user = await self.repository.get_by_username(user_data.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this username already exists"
            )

        hashed = self.security_service.hash_password(user_data.password)
        return await self.repository.create_user(
            user_data=user_data,
            hashed_password=hashed,
        )

    async def login(self, username: str, password: str) -> str:
        user = await self.repository.get_by_username(username=username)
        if not user or not self.security_service.verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        payload = TokenPayload(sub=user.username, user_id=user.id)

        return self.security_service.create_access_token(payload=payload)
