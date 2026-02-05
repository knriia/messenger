"""Конфигурация и инициализация FastAPI приложения."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dishka.integrations.fastapi import setup_dishka

from app.di.container import get_container
from app.api.endpoints.v1.auth import auth_router
from app.api.endpoints.v1.websocket import websocket_router
from app.api.endpoints.v1.messages import messages_router
from app.api.lifespan import setup_lifespan


def create_app() -> FastAPI:
    container = get_container()
    fastapi_app = FastAPI(lifespan=setup_lifespan(container=container))
    setup_dishka(app=fastapi_app, container=container)

    # Роутеры
    fastapi_app.include_router(auth_router)
    fastapi_app.include_router(websocket_router)
    fastapi_app.include_router(messages_router)

    # CORS
    fastapi_app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return fastapi_app


app = create_app()
