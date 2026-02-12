class ApplicationError(Exception):
    """Базовое исключение для всего приложения."""
    @property
    def message(self) -> str:
        return "Произошла внутренняя ошибка приложения"

class EntityNotFoundError(ApplicationError):
    """Когда что-то не нашли в базе."""
    pass
