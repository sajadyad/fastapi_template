from http import HTTPStatus
from fastapi import Request
from fastapi.responses import JSONResponse
from .exceptions import DomainException, UniqueConstraintException


async def unique_exception_handler(request: Request, exc: DomainException):
    """Handle DomainException and its subclasses."""

    match exc:
        case UniqueConstraintException():
            return JSONResponse(
                status_code=HTTPStatus.BAD_REQUEST,
                content=exc.to_dict(),
            )

        case _:
            return JSONResponse(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR, content=exc.to_dict()
            )


def register_error_handlers(app):
    """Register custom error handlers with the FastAPI app."""
    app.add_exception_handler(DomainException, unique_exception_handler)
