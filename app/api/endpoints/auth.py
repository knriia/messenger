from typing import Annotated
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from dishka.integrations.fastapi import FromDishka, inject

from app.schemas.user import UserCreate, UserOut, Token
from app.services.auth import AuthService


auth_router = APIRouter(prefix="/auth", tags=["Auth"])

@auth_router.post(
    "/register",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    summary="Регистрация нового пользователя"
)
@inject
async def register_user(user_data: UserCreate, auth_service: FromDishka[AuthService]):
    return await auth_service.register_user(user_data=user_data)


@auth_router.post(
    "/login",
    response_model=Token,
    summary="Вход в систему"
)
@inject
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], auth_service: FromDishka[AuthService]):
    access_token = await auth_service.login(username=form_data.username, password=form_data.password)
    return Token(access_token=access_token, token_type="bearer")
