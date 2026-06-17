"""Application settings."""

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
import os


@dataclass(frozen=True)
class Settings:
    app_name: str = "guide-backend"
    app_version: str = "0.1.0"
    host: str = "127.0.0.1"
    port: int = 8000
    debug: bool = False
    lesson_dir: Path = Path(__file__).resolve().parents[4] / "lessons"


@lru_cache
def get_settings() -> Settings:
    return Settings(
        host=os.getenv("GUIDE_BACKEND_HOST", "127.0.0.1"),
        port=int(os.getenv("GUIDE_BACKEND_PORT", "8000")),
        debug=os.getenv("GUIDE_DEBUG", "false").lower() == "true",
        lesson_dir=Path(
            os.getenv(
                "GUIDE_LESSON_DIR",
                str(Path(__file__).resolve().parents[4] / "lessons"),
            )
        ),
    )

