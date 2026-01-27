import os
from typing import Annotated

from fastapi import FastAPI, Depends
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from dishka.integrations.fastapi import setup_dishka, FromDishka, inject
from dishka import make_async_container

from app.di.container import DatabaseProvider
from app.core.config import Settings
from app.api.endpoints.auth import auth_router
from app.api.endpoints.websocket import websocket_router


def create_app() -> FastAPI:
    settings = Settings()
    app = FastAPI()
    app.include_router(auth_router)
    app.include_router(websocket_router)
    app.mount("/static", StaticFiles(directory=settings.PATH_TO_STATIC), name="static")
    container = make_async_container(DatabaseProvider())
    setup_dishka(app=app, container=container)
    return app


app = create_app()

@app.get('/')
@inject
async def get_front_page(
    settings: Annotated[Settings, FromDishka()],
):
    index_path = os.path.join(settings.PATH_TO_STATIC, "index.html")
    return FileResponse(index_path)
