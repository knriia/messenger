"""WebSocket эндпоинт приложения."""

from typing import Annotated
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query, status
from dishka.integrations.fastapi import FromDishka, inject

from app.services.connection_manager import ConnectionManager
from app.services.security import SecurityService
from app.database.repositories.user import UserRepository


websocket_router = APIRouter()
@websocket_router.websocket('/ws')
@inject
async def websocket_endpoint(
    websocket: WebSocket,
    manager: FromDishka[ConnectionManager],
    security_service: FromDishka[SecurityService],
    user_repo: FromDishka[UserRepository],
    token: Annotated[str | None, Query()] = None,
):
    if not token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    payload = security_service.decode_token(token=token)
    if not payload:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    user = await user_repo.get_by_username(username=payload.sub)
    if not user:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await manager.connect(user.id, websocket)
    try:
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        await manager.disconnect(user_id=user.id, websocket=websocket)