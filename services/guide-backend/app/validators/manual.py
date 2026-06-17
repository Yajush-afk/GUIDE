"""Manual validation strategy used for fallback and early testing."""

from app.models.validation import ValidationContext, ValidationResult, ValidationStatus
from app.validators.base import StepValidator


class ManualValidator(StepValidator):
    strategy = "manual"

    async def validate(self, context: ValidationContext) -> ValidationResult:
        return ValidationResult(
            status=ValidationStatus.WAITING,
            completed=False,
            reason="Waiting for the user to manually complete this step.",
            signals={"strategy": self.strategy},
        )

