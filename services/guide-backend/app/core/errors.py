"""Application-specific exceptions and FastAPI exception mapping."""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class GuideError(Exception):
    """Base class for expected GUIDE backend errors."""

    status_code = 500

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class LessonNotFoundError(GuideError):
    """Raised when a requested lesson does not exist."""

    status_code = 404


class LessonLoadError(GuideError):
    """Raised when a lesson exists but cannot be parsed."""

    status_code = 500


class SessionNotFoundError(GuideError):
    """Raised when a requested tutorial session does not exist."""

    status_code = 404


class InvalidSessionStateError(GuideError):
    """Raised when a session command is invalid for the current state."""

    status_code = 409


class ValidatorNotFoundError(GuideError):
    """Raised when a lesson references an unknown validation strategy."""

    status_code = 500


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(GuideError)
    async def handle_guide_error(request: Request, exc: GuideError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.__class__.__name__,
                "detail": exc.message,
            },
        )
