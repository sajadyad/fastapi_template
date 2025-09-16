from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings

# from app.core.logging import configure_logging
from app.api.v1.api import router as api_v1_router

# configure_loggin()


def create_app() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

    # CORS (adjust origins in production):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
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

    return app


app = create_app()
