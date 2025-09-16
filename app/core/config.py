from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI template"
    VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"

    # Example DB URL postgresql+asyncpg://postgres:password@db:5432/appdb
    DATABASE_URL: str

    # JWT / security
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"


settings = Settings()