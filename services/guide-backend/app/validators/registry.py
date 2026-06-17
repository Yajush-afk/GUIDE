"""Validation strategy registry."""

from app.core.errors import ValidatorNotFoundError
from app.validators.active_window import ActiveWindowValidator
from app.validators.base import StepValidator
from app.validators.chrome import BrowserSearchDetectedValidator, ChromeRunningValidator
from app.validators.manual import ManualValidator


class ValidatorRegistry:
    def __init__(self) -> None:
        self._validators: dict[str, StepValidator] = {}

    @classmethod
    def create_default(cls) -> "ValidatorRegistry":
        registry = cls()
        registry.register(ManualValidator())
        registry.register(ActiveWindowValidator())
        registry.register(ChromeRunningValidator())
        registry.register(BrowserSearchDetectedValidator())
        return registry

    def register(self, validator: StepValidator) -> None:
        self._validators[validator.strategy] = validator

    def get(self, strategy: str) -> StepValidator:
        validator = self._validators.get(strategy)
        if validator is None:
            raise ValidatorNotFoundError(f"Unknown validator strategy: {strategy}")
        return validator
