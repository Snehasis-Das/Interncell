from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.logging_config import setup_logging
import time
import logging

from app.core.config import settings
from app.db.session import engine
from app.db.base import Base

from app.routes import auth, users, internships, applications,uploads

from fastapi.responses import JSONResponse
from fastapi import Request, status
from app.core.exceptions import (
    AppException,
    NotFoundError,
    ConflictError,
    PermissionDenied,
    AuthenticationError,
)
from sqlalchemy.exc import IntegrityError
from app import models

from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from app.core.rate_limiter import limiter
from app.core.rate_limiter import redis_client  # adjust if needed
from redis.exceptions import RedisError
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from sqlalchemy import text


setup_logging()
logger = logging.getLogger(__name__)


def create_application() -> FastAPI:
    app = FastAPI(
        title="Interncell API",
        version="1.0.0",
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url=None,
    )

    # --- Middleware ---
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    app.state.limiter = limiter
    app.add_middleware(SlowAPIMiddleware)

    
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start_time = time.time()

        response = await call_next(request)

        process_time = time.time() - start_time

        logger.info(
            f"{request.method} {request.url.path} "
            f"Status={response.status_code} "
            f"Time={process_time:.3f}s"
        )

        return response

    # --- Include Routers ---
    app.include_router(auth.router, prefix="/auth", tags=["Auth"])
    app.include_router(users.router, prefix="/users", tags=["Users"])
    app.include_router(internships.router, prefix="/internships", tags=["Internships"])
    app.include_router(applications.router, prefix="/applications", tags=["Applications"])
    app.include_router(uploads.router, prefix="/uploads", tags=["Uploads"])
    
    # --- Exception Handlers ---

    @app.exception_handler(RateLimitExceeded)
    async def rate_limit_handler(request, exc):
        return JSONResponse(
            status_code=429,
            content={"detail": "Too many requests. Slow down."},
        )

    @app.exception_handler(NotFoundError)
    async def not_found_handler(request: Request, exc: NotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": exc.message},
        )

    @app.exception_handler(ConflictError)
    async def conflict_handler(request: Request, exc: ConflictError):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": exc.message},
        )

    @app.exception_handler(PermissionDenied)
    async def permission_handler(request: Request, exc: PermissionDenied):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": exc.message},
        )

    @app.exception_handler(AuthenticationError)
    async def auth_handler(request: Request, exc: AuthenticationError):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": exc.message},
        )
    
    @app.exception_handler(IntegrityError)
    async def integrity_error_handler(request: Request, exc: IntegrityError):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": "Database constraint violation"},
        )
    
    # --- Health Check ---
    @app.get("/health", tags=["System"])
    def health_check(db: Session = Depends(get_db)):
        checks = {
            "database": "unknown",
            "redis": "unknown",
        }

        overall_status = "ok"

        # --- Database Check ---
        try:
            db.execute(text("SELECT 1"))
            checks["database"] = "ok"
        except Exception:
            checks["database"] = "failed"
            overall_status = "degraded"

        # --- Redis Check ---
        try:
            redis_client.ping()
            checks["redis"] = "ok"
        except RedisError:
            checks["redis"] = "failed"
            overall_status = "degraded"

        response = {
            "status": overall_status,
            "checks": checks,
        }

        if overall_status != "ok":
            return JSONResponse(status_code=503, content=response)

        return response

    return app

app = create_application()
