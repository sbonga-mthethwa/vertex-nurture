from app.core.config import settings


class DatabaseConfig:
    """
    Database configuration.
    """

    @property
    def database_url(self) -> str:
        return (
            "postgresql+asyncpg://"
            f"{settings.POSTGRES_USER}:"
            f"{settings.POSTGRES_PASSWORD}@"
            f"{settings.POSTGRES_HOST}:"
            f"{settings.POSTGRES_PORT}/"
            f"{settings.POSTGRES_DB}"
        )


database_config = DatabaseConfig()