import random

from fastapi import FastAPI

app = FastAPI()


@app.post("/adaptive-learning")
async def adaptive_learning():
    return {
        "recommended_content": [
            "bim-advanced",
            "lean-construction",
            "structural-ai",
        ],
        "focus_probability": random.randint(70, 99),
    }
