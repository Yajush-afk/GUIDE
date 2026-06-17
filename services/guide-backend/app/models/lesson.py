"""Lesson and tutorial content models."""

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class StepTarget(BaseModel):
    model_config = ConfigDict(extra="allow")

    type: str
    region: str | None = None
    role: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class ValidationSpec(BaseModel):
    model_config = ConfigDict(extra="allow")

    strategy: str
    app: str | None = None
    expected_app: str | None = None
    expected_text_any: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class LessonStep(BaseModel):
    id: str
    instruction: str
    validation: ValidationSpec
    voice_text: str | None = None
    target: StepTarget | None = None
    hints: list[str] = Field(default_factory=list)
    timeout_seconds: int | None = None


class Lesson(BaseModel):
    id: str
    title: str
    platform: Literal["windows"]
    version: int
    steps: list[LessonStep]


class TutorialSummary(BaseModel):
    id: str
    title: str
    platform: Literal["windows"]
    version: int
    step_count: int
