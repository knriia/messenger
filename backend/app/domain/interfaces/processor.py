from abc import ABC, abstractmethod

from dishka import AsyncContainer


class IMessageProcessor(ABC):
    @abstractmethod
    async def start(self) -> None:
        """Запуск цикла прослушивания сообщений."""
        pass
