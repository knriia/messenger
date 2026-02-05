"""Точка входа в воркер Kafka."""

import asyncio
from dishka import make_async_container
from app.di.container import DatabaseProvider, KafkaProvider
from app.services.kafka_consumer import KafkaConsumerService


async def main():
    container = make_async_container(DatabaseProvider(), KafkaProvider())
    try:
        consumer_service = await container.get(KafkaConsumerService)
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
