from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env", extra="ignore")

    # Для локальной разработки
    postgres_url: str = "postgresql://user:password@localhost:5432/message_db"

    # Для продакшена (будут использоваться переменные окружения из workflow)
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "message_db"
    postgres_user: str = "user"
    postgres_password: str = "password"

    @property
    def database_url(self):
        # Если есть полный URL - используем его
        if self.postgres_url and self.postgres_url.startswith("postgresql://"):
            return self.postgres_url
        # Иначе собираем из компонентов
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"


settings = Settings()