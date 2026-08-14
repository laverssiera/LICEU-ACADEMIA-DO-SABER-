from fastapi import FastAPI

app = FastAPI()


@app.post("/simulate/structural")
async def structural():
    return {
        "simulation": "structural",
        "status": "completed",
        "stress_factor": 0.82,
        "risk": "low",
    }
