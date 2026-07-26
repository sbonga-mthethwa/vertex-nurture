from fastapi import FastAPI

from app.api.middleware.logging import RequestLoggingMiddleware
from app.api.middleware.request_id import RequestIDMiddleware
from app.api.middleware.timing import RequestTimingMiddleware


def configure_middleware(app: FastAPI) -> None:
    """
    Register application middleware.
    """

    app.add_middleware(RequestIDMiddleware)
    app.add_middleware(RequestTimingMiddleware)
    app.add_middleware(RequestLoggingMiddleware)