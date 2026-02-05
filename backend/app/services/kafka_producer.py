from aiokafka import AIOKafkaProducer
import json

from app.schemas.message import MessageCreateDTO


class KafkaProducerService:
    def __init__(self, producer: AIOKafkaProducer, topic: str):
        self.producer = producer
        self.topic = topic

    async def send_message(self, message_data: MessageCreateDTO):
        message_dict = message_data.model_dump()
        payload = json.dumps(message_dict).encode("utf-8")
        await self.producer.send_and_wait(self.topic, payload)
