"""Active-window detection helpers."""

from app.models.screen import WindowState


class WindowStateService:
    def get_active_window(self) -> WindowState | None:
        """Return active window metadata.

        Implement with pywin32 on Windows.
        """
        return None

