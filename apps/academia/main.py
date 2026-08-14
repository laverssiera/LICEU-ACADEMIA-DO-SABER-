from fastapi import FastAPI

from runtime.adaptive_learning_runtime import router as adaptive_learning_router
from runtime.civilization_brain_runtime import router as civilization_brain_router
from runtime.educational_cognition_runtime import router as educational_cognition_router
from runtime.educational_evolution_runtime import router as educational_evolution_router

app = FastAPI(
    title="Academia do Saber - Educational Runtime",
    version="1.0.0",
)

app.include_router(adaptive_learning_router)
app.include_router(educational_cognition_router)
app.include_router(educational_evolution_router)
app.include_router(civilization_brain_router)


@app.get("/")
async def root() -> dict[str, str]:
    return {
        "runtime": "Academia do Saber",
        "module": "Educational Cognition",
        "status": "running",
    }
