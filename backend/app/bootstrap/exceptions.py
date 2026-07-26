from fastapi import FastAPI

from app.core.exceptions.handlers import register_exception_handlers


def configure_exception_handlers(app: FastAPI) -> None:
    """
    Register global exception handlers.
    """

    register_exception_handlers(app)