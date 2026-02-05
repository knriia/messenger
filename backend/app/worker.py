"""Точка входа в воркер Kafka."""

import asyncio
from app.di.container import get_container
from app.infrastructure.kafka.consumer.message import MessageKafkaConsumer


async def main():
    container = get_container()
    try:
        consumer_service = await container.get(MessageKafkaConsumer)
        await consumer_service.start(container)
    except Exception as e:
        print(f"Worker crashed: {e}")
    finally:
        await container.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
