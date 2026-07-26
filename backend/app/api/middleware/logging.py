from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logging import logger


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Logs every request.
    """

    async def dispatch(self, request, call_next):
        response = await call_next(request)

        logger.info(
            "request_completed",
            request_id=getattr(request.state, "request_id", None),
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration_ms=getattr(request.state, "duration_ms", None),
            client_ip=request.client.host if request.client else None,
        )

        return response