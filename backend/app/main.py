from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dishka.integrations.fastapi import setup_dishka
from dishka import make_async_container

from app.di.container import DatabaseProvider, KafkaProvider
from app.api.endpoints.auth import auth_router
from app.api.endpoints.websocket import websocket_router
from app.api.endpoints.messages import messages_router


def create_app() -> FastAPI:
    app = FastAPI()
    container = make_async_container(DatabaseProvider(), KafkaProvider())
    setup_dishka(app=app, container=container)
    app.include_router(auth_router)
    app.include_router(websocket_router)
    app.include_router(messages_router)
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
    return app


app = create_app()
