"""FastAPI application entry point."""

from fastapi import FastAPI

from app.api.routes_health import router as health_router
from app.api.routes_sessions import router as sessions_router
from app.api.routes_tutorials import router as tutorials_router
from app.core.config import get_settings
from app.core.errors import register_exception_handlers
from app.core.logging import configure_logging


def create_app() -> FastAPI:
    """Create and configure the local GUIDE backend app."""
    settings = get_settings()
    configure_logging(settings)

    app = FastAPI(
        title="GUIDE Backend",
        description="Local backend for GUIDE desktop tutorials.",
        version=settings.app_version,
    )

    register_exception_handlers(app)

    app.include_router(health_router)
    app.include_router(tutorials_router)
    app.include_router(sessions_router)

    return app


app = create_app()
