from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env")

    postgres_url: str = "postgresql://user:password@message_db:5432/message_db"


settings = Settings()