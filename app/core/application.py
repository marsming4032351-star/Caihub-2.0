from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import get_settings
from app.core.lifespan import lifespan


def create_application() -> FastAPI:
    settings = get_settings()
    application = FastAPI(
        title=settings.app_name,
        description="Backend API for the CaiHub platform.",
        debug=settings.debug,
        version=settings.app_version,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )
    application.include_router(api_router)
    return application
