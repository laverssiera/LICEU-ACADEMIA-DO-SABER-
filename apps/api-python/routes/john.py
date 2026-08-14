import uuid

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/john")


class LessonRequest(BaseModel):
    student_id: str
    topic: str
    mode: str


@router.post("/academy/live-teaching")
async def live_teaching(data: LessonRequest):
    return {
        "lesson_id": str(uuid.uuid4()),
        "topic": data.topic,
        "mode": data.mode,
        "holographic_scene": True,
        "simulation_enabled": True,
        "adaptive_learning": True,
        "voice_ai": "john-ptbr",
    }
