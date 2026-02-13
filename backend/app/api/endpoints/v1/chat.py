from typing import Annotated

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Depends

from app.api.dependencies import get_current_user
from app.domain.entities.user_entity import UserEntity
from app.schemas.chat import PrivateChatOut
from app.services.chat_management import ChatManagementService

chat_router = APIRouter(prefix="/v1/chats", tags=["Chats"])


@chat_router.post("/get-or-create", summary="Получение/создание чата")
@inject
async def get_or_create_chat(
    target_user_id: int,
    current_user: Annotated[UserEntity, Depends(get_current_user)],
    chat_management_service: FromDishka[ChatManagementService],
) -> PrivateChatOut:
    chat_entity = await chat_management_service.get_or_create_private_chat(
        creator_id=current_user.id, target_id=target_user_id
    )
    return PrivateChatOut.model_validate(chat_entity, from_attributes=True)
