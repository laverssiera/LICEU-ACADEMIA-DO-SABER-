from fastapi import APIRouter

try:
    from transformers import pipeline
except ImportError:  # pragma: no cover - optional dependency
    pipeline = None

router = APIRouter()

teacher = None


def _get_teacher():
    global teacher

    if teacher is not None:
        return teacher

    if pipeline is None:
        return None

    teacher = pipeline(
        "text-generation",
        model="google/flan-t5-base"
    )
    return teacher


@router.post("/education/adaptive-teaching")
async def adaptive_teaching(payload: dict):
    prompt = f'''
Subject: {payload["subject"]}
Difficulty: {payload["difficulty"]}
Student: {payload["profile"]}
'''

    runtime_teacher = _get_teacher()

    if runtime_teacher is None:
        strategy = (
            "Adaptive strategy fallback: personalize content depth for the learner profile, "
            "increase guided practice in difficult topics, and track progress every cycle."
        )
    else:
        result = runtime_teacher(
            prompt,
            max_new_tokens=200
        )
        strategy = result[0]["generated_text"]

    return {
        "strategy": strategy,
        "runtime_identity": "Adaptive Education Runtime"
    }
