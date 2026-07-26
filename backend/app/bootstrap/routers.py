from fastapi import FastAPI

from app.api.router import router


def register_routers(app: FastAPI) -> None:
    """
    Register all API routers.
    """

    app.include_router(router)