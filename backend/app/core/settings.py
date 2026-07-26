from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """

    APP_NAME: str = "Vertex Nurture API"
    APP_VERSION: str = "0.1.0"
    APP_ENV: str = "development"

    # Backward compatibility
    VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"

    API_PREFIX: str = "/api/v1"

    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "vertex_nurture"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "Myname1sbonga!"

    DATABASE_ECHO: bool = False

    #JWT
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Returns cached application settings.
    """
    return Settings()


settings = get_settings()