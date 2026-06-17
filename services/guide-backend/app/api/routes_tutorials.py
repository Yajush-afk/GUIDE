"""Tutorial listing and lesson detail routes."""

from fastapi import APIRouter, Depends

from app.api.dependencies import get_lesson_loader
from app.lessons.loader import LessonLoader
from app.models.lesson import Lesson, TutorialSummary

router = APIRouter(prefix="/tutorials", tags=["tutorials"])


@router.get("", response_model=list[TutorialSummary])
async def list_tutorials(
    lesson_loader: LessonLoader = Depends(get_lesson_loader),
) -> list[TutorialSummary]:
    return lesson_loader.list_tutorials()


@router.get("/{lesson_id}", response_model=Lesson)
async def get_tutorial(
    lesson_id: str,
    lesson_loader: LessonLoader = Depends(get_lesson_loader),
) -> Lesson:
    return lesson_loader.load_lesson(lesson_id)

