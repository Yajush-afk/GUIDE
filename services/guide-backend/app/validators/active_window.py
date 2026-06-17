"""Active-window validation strategy."""

from app.models.validation import ValidationContext, ValidationResult, ValidationStatus
from app.validators.base import StepValidator


class ActiveWindowValidator(StepValidator):
    strategy = "active_window"

    async def validate(self, context: ValidationContext) -> ValidationResult:
        return ValidationResult(
            status=ValidationStatus.WAITING,
            completed=False,
            reason="Active window validation is not implemented yet.",
            signals={"strategy": self.strategy},
        )

