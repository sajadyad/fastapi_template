from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import configure_logging
from app.api.v1.api import router as api_v1_router
from .modules.error.handlers import register_error_handlers
from .modules.error.middleware import catch_all_exceptions_middleware
from .modules.error.exceptions import DomainException, UniqueConstraintException


configure_logging()


def create_app() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

    register_error_handlers(app)

    app.middleware("http")(catch_all_exceptions_middleware)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_v1_router, prefix="/api/v1")

    @app.get("/")
    async def root():
        return {"message": "Hello World"}

    @app.get("/health/liveness")
    async def liveness():
        return {"status": "ok"}

    @app.get("/error")
    async def error():
        raise Exception()

    @app.get("/error/domain")
    async def error_domain():
        raise DomainException()

    @app.get("/error/domain/unique-constraint")
    async def domain_error():
        raise UniqueConstraintException()

    return app


app = create_app()
