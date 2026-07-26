from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.exceptions.base import ApplicationError
from app.core.exceptions.responses import error_response
from app.core.logging import logger


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(ApplicationError)
    async def application_exception_handler(
        request: Request,
        exc: ApplicationError,
    ):
        logger.warning(
            "application_error",
            path=str(request.url.path),
            code=exc.error_code,
            message=exc.message,
        )

        return error_response(
            status_code=exc.status_code,
            error_code=exc.error_code,
            message=exc.message,
        )


    @app.exception_handler(Exception)
    async def unexpected_exception_handler(
        request: Request,
        exc: Exception,
    ):
        logger.exception(
            "unexpected_exception",
            path=str(request.url.path),
        )

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "An unexpected error occurred.",
                },
            },
        )