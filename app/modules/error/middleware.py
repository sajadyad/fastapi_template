import traceback
from http import HTTPStatus
from fastapi import Request
from fastapi.responses import JSONResponse
from .codes import ErrorCode


async def catch_all_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as exc:
        # Log full traceback (or send to Sentry, etc.)
        tb = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
        print(f"[ERROR] Unhandled exception: {tb}")

        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "code": ErrorCode.INTERNAL_SERVER_ERROR._name_,
                "error": "An unexpected error occurred.",
                "details": {},  # str(exc),  # Doesn't send details due to sensitive information leakage
            },
        )
