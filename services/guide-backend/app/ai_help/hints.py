"""Static hint helpers."""

from app.models.lesson import LessonStep


class HintService:
    def first_hint(self, step: LessonStep) -> str | None:
        return step.hints[0] if step.hints else None

