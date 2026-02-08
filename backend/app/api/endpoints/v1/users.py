from typing import Annotated
from fastapi import APIRouter, Depends
from dishka.integrations.fastapi import FromDishka, inject

from app.api.dependencies import get_current_user
from app.infrastructure.postgres.models.user import User
from app.infrastructure.postgres.repositories.user_repo import UserRepository
from app.schemas.user import UserOut


user_router = APIRouter(prefix='/v1/users', tags=['Users'])

@user_router.get('/search', response_model=UserOut)
@inject
async def search_users(
    query: str,
    current_user: Annotated[User, Depends(get_current_user)],
    user_repo: FromDishka[UserRepository]
):
    users = await user_repo.search_users(query=query)
    return [user for user in users if user.id != current_user.id]
