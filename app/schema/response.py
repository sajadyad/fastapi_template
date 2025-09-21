from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class StandardResponse(BaseModel, Generic[T]):
    success: bool
    message: str
    payload: T | None = None

    def __str__(self):
        return f"{self.success} : {self.message} -> {self.payload}"


def success(
    message: str = "success", payload: T | None = None
) -> StandardResponse[T] | StandardResponse[None]:
    return StandardResponse(success=True, message=message, payload=payload)


def failure(
    message: str = "failure", payload: T | None = None
) -> StandardResponse[T] | StandardResponse[None]:
    return StandardResponse(success=False, message=message, payload=payload)
