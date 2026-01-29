from typing import Annotated
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query, status
from dishka.integrations.fastapi import FromDishka, inject

from app.services.connection_manager import ConnectionManager
from app.services.chat import ChatService
from app.services.security import SecurityService
from app.database.repositories.user import UserRepository
from app.schemas.message import MessageCreate


websocket_router = APIRouter()
@websocket_router.websocket('/ws')
@inject
async def websocket_endpoint(
    websocket: WebSocket,
    manager: FromDishka[ConnectionManager],
    chat_service: FromDishka[ChatService],
    security_service: FromDishka[SecurityService],
    user_repo: FromDishka[UserRepository],
    token: Annotated[str | None, Query()] = None,
):
    payload = security_service.decode_token(token=token)
    if not payload:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    username = payload.get("sub")
    user = await user_repo.get_by_username(username=username)
    if not user:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await manager.connect(websocket)
    try:
        recent_messages = await chat_service.get_recent_messages(limit=50)
        for message in reversed(recent_messages):
            await websocket.send_json({"user_id": message.user_id, "text": message.text})

        while True:
            data = await websocket.receive_text()
            user_id = user.id
            message_data = MessageCreate(text=data, user_id=user_id)
            new_message = await chat_service.save_message(message_data=message_data)

            format_message = {"user_id": user_id, "text": new_message.text}
            await manager.broadcast(message_text=format_message)

    except WebSocketDisconnect:
        await manager.disconnect(websocket)