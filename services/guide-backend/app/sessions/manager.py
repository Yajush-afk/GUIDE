"""In-memory tutorial session manager for the MVP."""

from datetime import datetime, timezone
from uuid import uuid4

from app.core.errors import SessionNotFoundError
from app.lessons.loader import LessonLoader
from app.models.session import SessionState, SessionStatus
from app.models.validation import ValidationContext, ValidationResult, ValidationStatus
from app.validators.registry import ValidatorRegistry


class SessionManager:
    def __init__(
        self,
        lesson_loader: LessonLoader,
        validator_registry: ValidatorRegistry,
    ) -> None:
        self.lesson_loader = lesson_loader
        self.validator_registry = validator_registry
        self._sessions: dict[str, SessionState] = {}

    def create_session(self, lesson_id: str) -> SessionState:
        lesson = self.lesson_loader.load_lesson(lesson_id)
        session = SessionState(
            id=str(uuid4()),
            lesson_id=lesson.id,
            status=SessionStatus.CREATED,
            current_step_index=0,
            current_step=lesson.steps[0] if lesson.steps else None,
        )
        self._sessions[session.id] = session
        return session

    def get_session(self, session_id: str) -> SessionState:
        session = self._sessions.get(session_id)
        if session is None:
            raise SessionNotFoundError(f"Session not found: {session_id}")
        return session

    def start_session(self, session_id: str) -> SessionState:
        session = self.get_session(session_id)
        session.status = SessionStatus.RUNNING
        return self._touch(session)

    def pause_session(self, session_id: str) -> SessionState:
        session = self.get_session(session_id)
        session.status = SessionStatus.PAUSED
        return self._touch(session)

    def resume_session(self, session_id: str) -> SessionState:
        session = self.get_session(session_id)
        session.status = SessionStatus.RUNNING
        return self._touch(session)

    def stop_session(self, session_id: str) -> SessionState:
        session = self.get_session(session_id)
        session.status = SessionStatus.STOPPED
        return self._touch(session)

    async def validate_current_step(self, session_id: str) -> ValidationResult:
        session = self.get_session(session_id)
        if session.current_step is None:
            return ValidationResult(
                status=ValidationStatus.COMPLETED,
                completed=True,
                reason="Tutorial is already complete.",
            )

        validator = self.validator_registry.get(session.current_step.validation.strategy)
        result = await validator.validate(
            ValidationContext(
                step=session.current_step,
                spec=session.current_step.validation,
            )
        )

        if result.completed:
            self._advance(session, result.reason)

        return result

    def complete_step_manually(self, session_id: str) -> SessionState:
        session = self.get_session(session_id)
        return self._advance(session, "Step manually marked complete.")

    def get_hint(self, session_id: str) -> dict[str, str | None]:
        session = self.get_session(session_id)
        if session.current_step is None:
            return {"hint": None, "reason": "Tutorial is complete."}

        hint = session.current_step.hints[0] if session.current_step.hints else None
        return {"hint": hint, "reason": session.last_reason}

    def _advance(self, session: SessionState, reason: str) -> SessionState:
        lesson = self.lesson_loader.load_lesson(session.lesson_id)
        if session.current_step is not None:
            session.completed_step_ids.append(session.current_step.id)

        session.current_step_index += 1
        session.last_reason = reason

        if session.current_step_index >= len(lesson.steps):
            session.current_step = None
            session.status = SessionStatus.COMPLETED
        else:
            session.current_step = lesson.steps[session.current_step_index]

        return self._touch(session)

    def _touch(self, session: SessionState) -> SessionState:
        session.updated_at = datetime.now(timezone.utc)
        return session
