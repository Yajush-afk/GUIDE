"""Process detection helpers."""

from app.models.screen import ProcessInfo


class ProcessStateService:
    def list_processes(self) -> list[ProcessInfo]:
        """Return running processes.

        Implement with psutil. Keep output compact and avoid sensitive details.
        """
        return []

    def is_process_running(self, process_name: str) -> bool:
        target = process_name.lower()
        return any(process.name.lower() == target for process in self.list_processes())

