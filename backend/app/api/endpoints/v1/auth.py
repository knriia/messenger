"""Эндпоинты регистрации и авторизации"""

from typing import Annotated

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.token import Token
from app.schemas.user import UserCreate, UserOut
from app.services.auth import AuthService

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    summary="Регистрация нового пользователя",
)
@inject
async def register_user(user_data: UserCreate, auth_service: FromDishka[AuthService]) -> UserOut:
    result = await auth_service.register_user(user_data=user_data.to_entity())
    return UserOut.model_validate(result, from_attributes=True)


@auth_router.post("/login", summary="Вход в систему")
@inject
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: FromDishka[AuthService],
) -> Token:
    token_entity = await auth_service.login(username=form_data.username, password=form_data.password)
    return Token.model_validate(token_entity, from_attributes=True)
