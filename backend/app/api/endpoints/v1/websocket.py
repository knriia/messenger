"""WebSocket эндпоинт приложения."""

from typing import Annotated

from dishka import AsyncContainer
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query, status
from dishka.integrations.fastapi import FromDishka, inject

from app.services.connection_manager import ConnectionManager
from app.services.security import SecurityService
from app.database.repositories.user_repo import UserRepository


websocket_router = APIRouter(prefix="/v1/ws", tags=["WebSocket"])
@websocket_router.websocket('')
@inject
async def websocket_endpoint(
    websocket: WebSocket,
    manager: FromDishka[ConnectionManager],
    security_service: FromDishka[SecurityService],
    token: Annotated[str | None, Query()] = None,
):
    if not token:
        await websocket.accept()
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    payload = security_service.decode_token(token=token)
    if not payload or payload.user_id is None:
        await websocket.accept()
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    current_user_id = payload.user_id
    await manager.connect(current_user_id, websocket)

    try:
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        await manager.disconnect(user_id=current_user_id, websocket=websocket)
    except Exception:
        await manager.disconnect(user_id=current_user_id, websocket=websocket)