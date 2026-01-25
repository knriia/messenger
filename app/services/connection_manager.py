import asyncio

from anyio import BrokenResourceError
from starlette.websockets import WebSocket, WebSocketDisconnect


class ConnectionManager:
    def __init__(self):
        self.active_connections: set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)

    async def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message_text: str):
        task = [self._send_safe(conn, message_text) for conn in self.active_connections]
        await asyncio.gather(*task, return_exceptions=True)

    async def _send_safe(self, websocket: WebSocket, message_text: str):
        try:
            await websocket.send_text(message_text)
        except (WebSocketDisconnect, RuntimeError, BrokenResourceError):
            await self.disconnect(websocket)
        except Exception as e:
            import logging
            logging.error(f"Unexpected WebSocket error: {e}")
            await self.disconnect(websocket)
