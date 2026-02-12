"""Эндпоинты управления сообщениями."""

from typing import Annotated

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Depends

from app.api.dependencies import get_current_user
from app.domain.entities.user_entity import UserEntity
from app.schemas.message import MessageCreate, MessageRead
from app.services.message import MessageService

messages_router = APIRouter(prefix="/v1/messages", tags=["Messages"])


@messages_router.post("/send", summary="Отправка сообщения")
@inject
async def send_message(
    message_data: MessageCreate,
    current_user: Annotated[UserEntity, Depends(get_current_user)],
    message_service: FromDishka[MessageService],
) -> MessageRead:
    message_entity = message_data.to_entity(sender_id=current_user.id)
    result = await message_service.send_message(message_data=message_entity)
    return MessageRead.model_validate(result, from_attributes=True)
