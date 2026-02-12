"""Зависимости для аутентификации пользователей."""

from typing import Annotated

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.domain.entities.user_entity import UserEntity
from app.domain.interfaces.security import ISecurityService
from app.infrastructure.postgres.repositories.user_repo import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@inject
async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    security_service: FromDishka[ISecurityService],
    user_repo: FromDishka[UserRepository],
) -> UserEntity:
    payload = security_service.decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    username = payload.sub
    user = await user_repo.get_by_username(username=username)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    return user
