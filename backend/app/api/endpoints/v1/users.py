from typing import Annotated

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Depends

from app.api.dependencies import get_current_user
from app.domain.entities.user_entity import UserEntity
from app.schemas.user import UserOut
from app.services.user import UserService

user_router = APIRouter(prefix="/v1/users", tags=["Users"])


@user_router.get("/search", summary="Поиск пользователя")
@inject
async def search_users(
    query: str,
    current_user: Annotated[UserEntity, Depends(get_current_user)],
    user_service: FromDishka[UserService],
) -> list[UserOut]:
    users = await user_service.search_users(query=query, current_user_id=current_user.id)
    return [UserOut.model_validate(u, from_attributes=True) for u in users]
