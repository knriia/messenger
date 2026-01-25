import os

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from dishka.integrations.fastapi import setup_dishka
from dishka import make_container

from app.di.container import DatabaseProvider
from app.schemas.message import MessageCreate
from app.services.chat import ChatService
from app.services.connection_manager import ConnectionManager
from app.core.config import Settings


settings = Settings()

app = FastAPI()
PATH_TO_STATIC = settings.PATH_TO_STATIC
app.mount("/static", StaticFiles(directory=PATH_TO_STATIC), name="static")
container = make_container(DatabaseProvider())
setup_dishka(app=app, container=container)


@app.get('/')
async def get_front_page(settings: Settings = Depends(DatabaseProvider.get_settings)):
    index_path = os.path.join(settings.PATH_TO_STATIC, "index.html")
    return FileResponse(index_path)


@app.websocket('/ws/{client_id}')
async def websocket_endpoint(
        websocket: WebSocket,
        user_id: int,
        manager: ConnectionManager = Depends(DatabaseProvider.get_connection_manager),
        chat_service: ChatService = Depends(DatabaseProvider.get_chat_service)
):
    recent_message = await chat_service.get_recent_messages(limit=50)
    for message in reversed(recent_message):
        await websocket.send_text(f"{message.user_id}: {message.text}")

    try:
        while True:
            data = await websocket.receive_text()
            message_data = MessageCreate(text=data, user_id=user_id)
            new_message = await chat_service.save_message(message_data=message_data)
            format_message = f"{user_id}: {new_message.text}"
            await manager.broadcast(message_text=format_message)

    except WebSocketDisconnect:
        await manager.disconnect(websocket)
