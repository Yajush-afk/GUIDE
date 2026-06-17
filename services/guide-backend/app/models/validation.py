"""Validation models."""

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field

from app.models.lesson import LessonStep, ValidationSpec
from app.models.screen import ScreenState


class ValidationStatus(StrEnum):
    WAITING = "waiting"
    COMPLETED = "completed"
    FAILED = "failed"


class ValidationResult(BaseModel):
    status: ValidationStatus
    completed: bool
    reason: str
    signals: dict[str, Any] = Field(default_factory=dict)


class ValidationContext(BaseModel):
    step: LessonStep
    spec: ValidationSpec
    screen_state: ScreenState | None = None

