"""Эндпоинты управления сообщениями."""

from typing import Annotated
from fastapi import APIRouter, Depends
from dishka.integrations.fastapi import FromDishka, inject

from app.schemas.message import MessageCreate, MessageSendResponse
from app.services.message import MessageService
from app.infrastructure.postgres.models.user import User
from app.api.dependencies import get_current_user


messages_router = APIRouter(prefix='/v1/messages', tags=['Messages'])

@messages_router.post('/send', response_model=MessageSendResponse)
@inject
async def send_message(
    chat_id: int,
    content: str,
    current_user: Annotated[User, Depends(get_current_user)],
    message_service: FromDishka[MessageService]
):
    message_data = MessageCreate(
        sender_id=current_user.id,
        chat_id=chat_id,
        content=content
    )

    result = await message_service.send_message(message_data)
    return result
