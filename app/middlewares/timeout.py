import asyncio
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse


class TimeoutMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, timeout: int = 60):
        super().__init__(app)
        self.timeout = timeout

    async def dispatch(self, request: Request, call_next):
        try:
            return await asyncio.wait_for(call_next(request), timeout=self.timeout)
        except asyncio.TimeoutError:
            return JSONResponse(
                status_code=504,
                content={"error": "Request timed out. Try again later."},
            )