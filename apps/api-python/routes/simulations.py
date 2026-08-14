from fastapi import APIRouter

router = APIRouter(prefix="/simulations")


@router.post("/start")
async def start_simulation():
    return {
        "started": True,
        "simulation": "structural",
        "status": "queued",
    }
