from app.domain.exceptions.base import ApplicationError


class SecurityError(ApplicationError):
    pass

class PasswordVerificationError(SecurityError):
    @property
    def message(self) -> str:
        return "Ошибка проверки целостности пароля"
