import uuid
import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

# Set up logging configuration
logger = logging.getLogger("api")
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 1. Check or generate Request ID
        request_id = request.headers.get("X-Request-ID")
        if not request_id:
            request_id = str(uuid.uuid4())

        # Attach request_id to request state
        request.state.request_id = request_id

        # 2. Track processing duration
        start_time = time.time()
        try:
            response = await call_next(request)
        except Exception as e:
            process_time = time.time() - start_time
            logger.error(
                f"method={request.method} path={request.url.path} "
                f"status=500 duration={process_time:.4f}s "
                f"request_id={request_id} error={str(e)}"
            )
            raise e

        process_time = time.time() - start_time

        # 3. Add Request ID header to response
        response.headers["X-Request-ID"] = request_id

        # 4. Log request details
        logger.info(
            f"method={request.method} path={request.url.path} "
            f"status={response.status_code} duration={process_time:.4f}s "
            f"request_id={request_id}"
        )

        return response
