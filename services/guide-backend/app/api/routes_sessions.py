"""Tutorial session routes."""

from fastapi import APIRouter, Depends

from app.api.dependencies import get_session_manager
from app.models.session import CreateSessionRequest, SessionState
from app.models.validation import ValidationResult
from app.sessions.manager import SessionManager

router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.post("", response_model=SessionState)
async def create_session(
    request: CreateSessionRequest,
    session_manager: SessionManager = Depends(get_session_manager),
) -> SessionState:
    return session_manager.create_session(request.lesson_id)


@router.get("/{session_id}", response_model=SessionState)
async def get_session(
    session_id: str,
    session_manager: SessionManager = Depends(get_session_manager),
) -> SessionState:
    return session_manager.get_session(session_id)


@router.post("/{session_id}/start", response_model=SessionState)
async def start_session(
    session_id: str,
    session_manager: SessionManager = Depends(get_session_manager),
) -> SessionState:
    return session_manager.start_session(session_id)


@router.post("/{session_id}/pause", response_model=SessionState)
async def pause_session(
    session_id: str,
    session_manager: SessionManager = Depends(get_session_manager),
) -> SessionState:
    return session_manager.pause_session(session_id)


@router.post("/{session_id}/resume", response_model=SessionState)
async def resume_session(
    session_id: str,
    session_manager: SessionManager = Depends(get_session_manager),
) -> SessionState:
    return session_manager.resume_session(session_id)


@router.post("/{session_id}/validate", response_model=ValidationResult)
async def validate_current_step(
    session_id: str,
    session_manager: SessionManager = Depends(get_session_manager),
) -> ValidationResult:
    return await session_manager.validate_current_step(session_id)


@router.post("/{session_id}/complete-step-manually", response_model=SessionState)
async def complete_step_manually(
    session_id: str,
    session_manager: SessionManager = Depends(get_session_manager),
) -> SessionState:
    return session_manager.complete_step_manually(session_id)


@router.post("/{session_id}/hint")
async def get_hint(
    session_id: str,
    session_manager: SessionManager = Depends(get_session_manager),
) -> dict[str, str | None]:
    return session_manager.get_hint(session_id)


@router.post("/{session_id}/stop", response_model=SessionState)
async def stop_session(
    session_id: str,
    session_manager: SessionManager = Depends(get_session_manager),
) -> SessionState:
    return session_manager.stop_session(session_id)

