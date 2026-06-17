"""Validator interfaces."""

from abc import ABC, abstractmethod

from app.models.validation import ValidationContext, ValidationResult


class StepValidator(ABC):
    strategy: str

    @abstractmethod
    async def validate(self, context: ValidationContext) -> ValidationResult:
        """Validate whether the current tutorial step is complete."""

