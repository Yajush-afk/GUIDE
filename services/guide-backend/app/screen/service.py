"""Facade for collecting structured screen and OS state."""

from app.models.screen import ScreenState
from app.screen.process_state import ProcessStateService
from app.screen.window_state import WindowStateService


class ScreenUnderstandingService:
    def __init__(
        self,
        process_state: ProcessStateService | None = None,
        window_state: WindowStateService | None = None,
    ) -> None:
        self.process_state = process_state or ProcessStateService()
        self.window_state = window_state or WindowStateService()

    def get_state(self) -> ScreenState:
        return ScreenState(
            active_window=self.window_state.get_active_window(),
            running_processes=self.process_state.list_processes(),
        )

