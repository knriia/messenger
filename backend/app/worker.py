"""Точка входа в воркер Kafka."""

import asyncio
from app.di.container import get_container
from app.domain.interfaces.processor import IMessageProcessor


async def main():
    container = get_container()
    try:
        processor = await container.get(IMessageProcessor)
        await processor.start()
    finally:
        await container.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
