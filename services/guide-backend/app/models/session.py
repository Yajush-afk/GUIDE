"""Tutorial session models."""

from datetime import datetime, timezone
from enum import StrEnum

from pydantic import BaseModel, Field

from app.models.lesson import LessonStep


class SessionStatus(StrEnum):
    CREATED = "created"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    STOPPED = "stopped"
    ERROR = "error"


class StepStatus(StrEnum):
    WAITING = "waiting"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED_MANUAL = "skipped_manual"


class CreateSessionRequest(BaseModel):
    lesson_id: str


class SessionState(BaseModel):
    id: str
    lesson_id: str
    status: SessionStatus
    current_step_index: int = 0
    current_step: LessonStep | None = None
    completed_step_ids: list[str] = Field(default_factory=list)
    last_reason: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

