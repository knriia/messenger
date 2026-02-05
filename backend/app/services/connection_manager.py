"""Менеджер WebSocket-соединений."""

import asyncio

from anyio import BrokenResourceError
from starlette.websockets import WebSocket, WebSocketDisconnect


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, list[WebSocket]] = {}

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)

    async def disconnect(self, user_id: int, websocket: WebSocket):
        if user_id in self.active_connections:
            if websocket in self.active_connections[user_id]:
                self.active_connections[user_id].remove(websocket)

            if not self.active_connections[user_id]:
                del self.active_connections[user_id]

    async def send_to_user(self, user_id: int, message: dict):
        if user_id not in self.active_connections:
            return

        sockets = self.active_connections[user_id]
        tasks = [self._send_safe(user_id, ws, message) for ws in sockets]
        await asyncio.gather(*tasks, return_exceptions=True)

    async def broadcast(self, message: dict):
        tasks = []
        for user_id, sockets in self.active_connections.items():
            for ws in sockets:
                tasks.append(self._send_safe(user_id, ws, message))
        await asyncio.gather(*tasks, return_exceptions=True)

    async def _send_safe(self, user_id: int, websocket: WebSocket, message: dict):
        try:
            await websocket.send_json(message)
        except (WebSocketDisconnect, RuntimeError, BrokenResourceError):
            await self.disconnect(user_id, websocket)
        except Exception as e:
            await self.disconnect(user_id, websocket)
