"""Structured screen and OS-state models."""

from datetime import datetime, timezone

from pydantic import BaseModel, Field


class WindowState(BaseModel):
    title: str | None = None
    process_name: str | None = None
    class_name: str | None = None


class ProcessInfo(BaseModel):
    pid: int
    name: str


class ScreenState(BaseModel):
    captured_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    active_window: WindowState | None = None
    running_processes: list[ProcessInfo] = Field(default_factory=list)
    ocr_text: list[str] = Field(default_factory=list)
    signals: dict[str, bool | str | int | float | None] = Field(default_factory=dict)

