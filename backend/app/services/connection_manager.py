"""Менеджер WebSocket-соединений."""

import asyncio

from anyio import BrokenResourceError
from starlette.websockets import WebSocket, WebSocketDisconnect

from app.schemas.message import MessageRead


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, list[WebSocket]] = {}

    async def connect(self, user_id: int, websocket: WebSocket):
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)

    async def disconnect(self, user_id: int, websocket: WebSocket):
        if user_id in self.active_connections:
            if websocket in self.active_connections[user_id]:
                self.active_connections[user_id].remove(websocket)

            if not self.active_connections[user_id]:
                self.active_connections.pop(user_id, None)

    async def send_to_user(self, user_id: int, message: MessageRead):
        if user_id not in self.active_connections:
            return

        sockets = list(self.active_connections[user_id])
        message_data = message.model_dump(mode="json")
        tasks = [self._send_safe(user_id, ws, message_data) for ws in sockets]
        await asyncio.gather(*tasks, return_exceptions=True)

    async def broadcast(self, message: dict):
        tasks = []
        for user_id in list(self.active_connections.keys()):
            sockets = list(self.active_connections.get(user_id, []))
            for ws in sockets:
                tasks.append(self._send_safe(user_id, ws, message))

        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    async def _send_safe(self, user_id: int, websocket: WebSocket, message: dict):
        """Защищенная отправка сообщения с авто-удалением «мертвых» сокетов."""
        try:
            await websocket.send_json(message)
        except (WebSocketDisconnect, RuntimeError, BrokenResourceError, Exception):
            await self.disconnect(user_id, websocket)
