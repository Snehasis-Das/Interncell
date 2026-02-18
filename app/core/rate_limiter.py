from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from fastapi import Request
from redis import Redis
from redis.exceptions import RedisError
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# -----------------------------
# Try Connecting To Redis
# -----------------------------

redis_client = None
limiter = None

try:
    redis_client = Redis.from_url(settings.REDIS_URL, socket_connect_timeout=2)
    redis_client.ping()  # Test connection

    limiter = Limiter(
        key_func=get_remote_address,
        storage_uri=settings.REDIS_URL,
    )

    logger.info("Redis connected. Rate limiting enabled.")

except RedisError:
    logger.warning("Redis unavailable. Rate limiting disabled.")

    # Dummy limiter (no-op)
    class DummyLimiter:
        def limit(self, *args, **kwargs):
            def decorator(func):
                return func
            return decorator

    limiter = DummyLimiter()
