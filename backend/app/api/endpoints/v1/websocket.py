"""WebSocket эндпоинт приложения."""

import logging
from typing import Annotated

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Query, WebSocket, WebSocketDisconnect, status

from app.domain.interfaces.security import ISecurityService
from app.services.connection_manager import ConnectionManager

logger = logging.getLogger(__name__)
websocket_router = APIRouter(prefix="/v1/ws", tags=["WebSocket"])


@websocket_router.websocket("")
@inject
async def websocket_endpoint(
    websocket: WebSocket,
    manager: FromDishka[ConnectionManager],
    security_service: FromDishka[ISecurityService],
    token: Annotated[str | None, Query()] = None,
) -> None:
    if not token:
        return await websocket.close(code=status.WS_1008_POLICY_VIOLATION)

    payload = security_service.decode_token(token=token)
    if not payload:
        return await websocket.close(code=status.WS_1008_POLICY_VIOLATION)

    current_user_id = payload.user_id
    await websocket.accept()
    await manager.connect(current_user_id, websocket)

    try:
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        await manager.disconnect(user_id=current_user_id, websocket=websocket)
    except Exception as e:
        logger.error(f"WebSocket error for user {current_user_id}: {e}")
        await manager.disconnect(user_id=current_user_id, websocket=websocket)
