"""Backend event models for future WebSocket updates."""

from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, Field


class BackendEvent(BaseModel):
    type: str
    session_id: str | None = None
    step_id: str | None = None
    payload: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class StepChangedEvent(BackendEvent):
    type: Literal["step_changed"] = "step_changed"


class ValidationUpdateEvent(BackendEvent):
    type: Literal["validation_update"] = "validation_update"

