import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext

security = HTTPBasic()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Mock the db
fake_users_db = {
    "admin": {"username": "admin", "hashed_password": pwd_context.hash("1234")}
}


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    user = fake_users_db.get(credentials.username)
    if not user:
        return None

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    if not secrets.compare_digest(credentials.username, user["username"]):
        return None

    if not secrets.compare_digest(credentials.password, user["password"]):
        return None

    return user
