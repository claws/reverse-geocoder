import logging
from fastapi import FastAPI
from .config import settings
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware
from . import api
from . import db

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:

    db.configure(settings)

    app = FastAPI(
        title=settings.service_name,
        openapi_url=f"{settings.api_v1_path}{settings.open_api_path}",
        docs_url=f"{settings.api_v1_path}{settings.docs_path}",
        debug=settings.debug,
    )

    # Add middleware
    app.add_middleware(GZipMiddleware)
    app.add_middleware(
        CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
    )

    # attach endpoints
    app.include_router(api.root.router)
    app.include_router(
        api.reverse_geocoder.router,
        prefix=settings.api_v1_path,
        tags=["reverse geocoder"],
    )

    @app.on_event("startup")
    async def startup():
        logger.info(f"Starting {settings.service_name}")
        await db.get_db().connect()

    @app.on_event("shutdown")
    async def shutdown():
        logger.info(f"Stopping {settings.service_name}")
        await db.get_db().disconnect()

    return app


app = create_app()
