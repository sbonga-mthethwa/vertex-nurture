from fastapi import FastAPI

from app.api.router import router
from app.core.config import settings


def register_routers(app: FastAPI) -> None:
    """
    Register all API routers.
    """

    app.include_router(
        router,
        prefix=settings.API_PREFIX,
    )