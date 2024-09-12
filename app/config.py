from pydantic_settings import BaseSettings, SettingsConfigDict


class Redis(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="REX_REDIS_", extra="ignore")

    host: str = "localhost"
    port: int = 6000
    db: int = 0
    max_connections: int = 10

    @property
    def url(self) -> str:
        return f"redis://{self.host}:{self.port}/{self.db}"


class ExchangeRatesAPI(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="EXCHANGERATESAPI_", extra="ignore"
    )

    base_url: str = "https://api.exchangeratesapi.io/v1/"
    access_key: str
    expire: int = 3600  # in seconds
    has_access_to_base: bool = True


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    redis: Redis = Redis()
    exchangeratesapi: ExchangeRatesAPI = ExchangeRatesAPI()


settings = Settings()
