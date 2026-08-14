from fastapi import APIRouter

router = APIRouter(prefix="/holography")


@router.post("/start")
async def start_holography():
    return {
        "started": True,
        "engine": "webxr",
        "scene": "classroom_v1",
    }
