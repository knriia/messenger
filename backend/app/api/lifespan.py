from fastapi import FastAPI
from contextlib import asynccontextmanager
from dishka import AsyncContainer


def setup_lifespan(container: AsyncContainer):
    @asynccontextmanager
    async def lifespan(_: FastAPI):
        yield
        await container.close()

    return lifespan
