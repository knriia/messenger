from app.domain.exceptions.base import ApplicationError


class AuthError(ApplicationError):
    pass

class UserAlreadyExistsError(AuthError):
    @property
    def message(self) -> str:
        return "Пользователь с таким именем уже существует"

class InvalidCredentialsError(AuthError):
    @property
    def message(self) -> str:
        return "Неверный логин или пароль"
