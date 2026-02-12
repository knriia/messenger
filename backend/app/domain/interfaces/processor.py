from abc import ABC, abstractmethod


class IMessageProcessor(ABC):
    @abstractmethod
    async def start(self) -> None:
        """Запуск цикла прослушивания сообщений."""
        pass
