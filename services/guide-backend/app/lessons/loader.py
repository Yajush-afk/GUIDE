"""Lesson file loader."""

from pathlib import Path

import yaml
from pydantic import ValidationError

from app.core.errors import LessonLoadError, LessonNotFoundError
from app.models.lesson import Lesson, TutorialSummary


class LessonLoader:
    def __init__(self, lesson_dir: Path) -> None:
        self.lesson_dir = lesson_dir

    def list_tutorials(self) -> list[TutorialSummary]:
        return [
            TutorialSummary(
                id=lesson.id,
                title=lesson.title,
                platform=lesson.platform,
                version=lesson.version,
                step_count=len(lesson.steps),
            )
            for lesson in self._load_all_lessons()
        ]

    def load_lesson(self, lesson_id: str) -> Lesson:
        for path in self._lesson_files():
            raw = self._read_yaml(path)
            if raw.get("id") != lesson_id:
                continue
            return self._parse_lesson(raw, path)

        raise LessonNotFoundError(f"Lesson not found: {lesson_id}")

    def _load_all_lessons(self) -> list[Lesson]:
        return [self._parse_lesson(self._read_yaml(path), path) for path in self._lesson_files()]

    def _lesson_files(self) -> list[Path]:
        if not self.lesson_dir.exists():
            return []
        return sorted(
            [
                *self.lesson_dir.glob("*.yaml"),
                *self.lesson_dir.glob("*.yml"),
            ]
        )

    def _read_yaml(self, path: Path) -> dict:
        with path.open("r", encoding="utf-8") as file:
            data = yaml.safe_load(file) or {}
        if not isinstance(data, dict):
            raise LessonLoadError(f"Invalid lesson file: {path.name}")
        return data

    def _parse_lesson(self, raw: dict, path: Path) -> Lesson:
        try:
            return Lesson.model_validate(raw)
        except ValidationError as exc:
            raise LessonLoadError(f"Invalid lesson schema in {path.name}: {exc}") from exc
