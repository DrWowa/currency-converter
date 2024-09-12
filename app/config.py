from pydantic_settings import BaseSettings, SettingsConfigDict


class Redis(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="REX_REDIS_")

    host: str = "localhost"
    port: int = 6000
    db: int = 0
    max_connections: int = 10

    @property
    def url(self) -> str:
        return f"redis://{self.host}:{self.port}/{self.db}"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    redis: Redis = Redis()


settings = Settings()
