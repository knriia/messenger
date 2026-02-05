"""Эндпоинты управления сообщениями."""

from typing import Annotated
from fastapi import APIRouter, Depends
from dishka.integrations.fastapi import FromDishka, inject

from app.schemas.message import MessageCreate
from app.services.message.chat import ChatService
from app.database.models.user import User
from app.api.dependencies import get_current_user


messages_router = APIRouter(prefix='/messages', tags=['Messeges'])

@messages_router.post('/send')
@inject
async def send_message(
    chat_id: int,
    content: str,
    current_user: Annotated[User, Depends(get_current_user)],
    chat_service: FromDishka[ChatService]
):
    message_data = MessageCreate(
        sender_id=current_user.id,
        chat_id=chat_id,
        content=content
    )

    result = await chat_service.send_new_message(message_data)
    return result
