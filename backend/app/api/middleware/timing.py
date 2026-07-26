import time

from starlette.middleware.base import BaseHTTPMiddleware


class RequestTimingMiddleware(BaseHTTPMiddleware):
    """
    Measures request processing time.
    """

    async def dispatch(self, request, call_next):
        start = time.perf_counter()

        response = await call_next(request)

        duration = (time.perf_counter() - start) * 1000

        request.state.duration_ms = round(duration, 2)

        response.headers["X-Process-Time"] = f"{duration:.2f} ms"

        return response