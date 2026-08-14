from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import cognitive
from routes import holography
from routes import john
from routes import simulations

app = FastAPI(title="LICEU Academia API", version="7.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(john.router)
app.include_router(holography.router)
app.include_router(simulations.router)
app.include_router(cognitive.router)


@app.get("/")
async def root():
    return {
        "platform": "LICEU Academia do Saber",
        "version": "7.0",
        "status": "running",
    }
