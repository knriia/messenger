import os
from typing import Annotated

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
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
    origins = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    container = make_async_container(DatabaseProvider())
    setup_dishka(app=app, container=container)
    return app


app = create_app()
