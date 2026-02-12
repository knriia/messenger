"""Провайдер настроек приложения"""

from dishka import Provider, Scope, provide

from app.core.config import Settings


class ConfigProvider(Provider):
    @provide(scope=Scope.APP)
    def get_settings(self) -> Settings:
        return Settings()
