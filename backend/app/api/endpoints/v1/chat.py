from typing import Annotated
from fastapi import Depends, APIRouter
from dishka.integrations.fastapi import FromDishka, inject

from app.api.dependencies import get_current_user
from app.database.models.user import User
from app.schemas.chat import ChatOut
from app.services.chat_management import ChatManagementService


chat_router = APIRouter(prefix='/v1/chats', tags=['Chats'])

@chat_router.post("/get-or-create", response_model=ChatOut)
@inject
async def get_or_create_chat(
    target_user_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    chat_management_service: FromDishka[ChatManagementService]
):
    chat = await chat_management_service.get_or_create_private_chat(
        creator_id=current_user.id,
        target_id=target_user_id
    )
    return chat

