from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app.bootstrap.cors import configure_cors
from app.bootstrap.exceptions import configure_exception_handlers
from app.bootstrap.lifespan import lifespan
from app.bootstrap.logging import configure_logging
from app.bootstrap.middleware import configure_middleware
from app.bootstrap.routers import register_routers
from app.core.config import settings


def create_app() -> FastAPI:
    """
    Application Factory.

    Creates and configures the FastAPI application.
    """

    app = FastAPI(
        title=settings.APP_NAME,
        description="Backend API for the Vertex Nurture platform.",
        version=settings.APP_VERSION,
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    configure_logging(app)
    configure_cors(app)
    configure_middleware(app)
    configure_exception_handlers(app)

    register_routers(app)

    app.openapi = lambda: custom_openapi(app)

    return app


def custom_openapi(app: FastAPI):
    """
    Adds JWT Bearer authentication to Swagger.
    """

    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    app.openapi_schema = openapi_schema

    return app.openapi_schema