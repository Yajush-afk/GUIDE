"""FastAPI dependency providers."""

from functools import lru_cache

from app.core.config import Settings, get_settings
from app.lessons.loader import LessonLoader
from app.sessions.manager import SessionManager
from app.validators.registry import ValidatorRegistry


@lru_cache
def get_lesson_loader() -> LessonLoader:
    settings = get_settings()
    return LessonLoader(settings.lesson_dir)


@lru_cache
def get_validator_registry() -> ValidatorRegistry:
    return ValidatorRegistry.create_default()


@lru_cache
def get_session_manager() -> SessionManager:
    return SessionManager(
        lesson_loader=get_lesson_loader(),
        validator_registry=get_validator_registry(),
    )


def get_app_settings() -> Settings:
    return get_settings()

