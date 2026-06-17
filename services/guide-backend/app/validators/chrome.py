"""Chrome-specific validation strategies."""

from app.models.validation import ValidationContext, ValidationResult, ValidationStatus
from app.validators.base import StepValidator


class ChromeRunningValidator(StepValidator):
    strategy = "chrome_running"

    async def validate(self, context: ValidationContext) -> ValidationResult:
        return ValidationResult(
            status=ValidationStatus.WAITING,
            completed=False,
            reason="Chrome process validation is not implemented yet.",
            signals={"strategy": self.strategy},
        )


class BrowserSearchDetectedValidator(StepValidator):
    strategy = "browser_search_detected"

    async def validate(self, context: ValidationContext) -> ValidationResult:
        return ValidationResult(
            status=ValidationStatus.WAITING,
            completed=False,
            reason="Browser search detection is not implemented yet.",
            signals={"strategy": self.strategy},
        )

