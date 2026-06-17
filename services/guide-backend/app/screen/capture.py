"""Screen capture helpers.

Screenshots must stay in memory and must not be saved by default.
"""


class ScreenCaptureService:
    def capture_primary_monitor(self) -> object | None:
        """Return an in-memory screenshot object.

        Implement with MSS when screen understanding work starts.
        """
        return None

