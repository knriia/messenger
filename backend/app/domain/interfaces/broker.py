from abc import ABC, abstractmethod
from typing import Any


class IMessageBroker(ABC):
    @abstractmethod
    async def publish(self, key: str, value: Any) -> None:
        pass
