from fastapi import APIRouter
import statistics
import hashlib
import time

router = APIRouter()

LEARNING_MEMORY = []


class EducationalAutonomicRuntime:

    @staticmethod
    def evaluate_student(payload):

        cognition_score = payload.get(
            "cognition_score",
            0.5
        )

        consistency = payload.get(
            "consistency",
            0.5
        )

        engagement = payload.get(
            "engagement",
            0.5
        )

        overload_risk = round(
            1 - (
                cognition_score * 0.4 +
                consistency * 0.3 +
                engagement * 0.3
            ),
            6
        )

        if overload_risk >= 0.7:
            intervention = "critical_recovery"

        elif overload_risk >= 0.5:
            intervention = "adaptive_support"

        else:
            intervention = "accelerated_mastery"

        learning_state = {
            "timestamp":
            time.time(),

            "student_id":
            payload.get(
                "student_id"
            ),

            "discipline":
            payload.get(
                "discipline"
            ),

            "cognition_score":
            cognition_score,

            "consistency":
            consistency,

            "engagement":
            engagement,

            "overload_risk":
            overload_risk,

            "intervention":
            intervention
        }

        signature = hashlib.sha256(
            str(learning_state).encode()
        ).hexdigest()

        learning_state[
            "signature"
        ] = signature

        LEARNING_MEMORY.append(
            learning_state
        )

        cognition_average = statistics.mean([
            x["cognition_score"]
            for x in LEARNING_MEMORY
        ])

        return {
            "learning_state":
            learning_state,

            "global_cognition":
            cognition_average,

            "memory_size":
            len(LEARNING_MEMORY),

            "runtime_state":
            "educational_autonomic_operational"
        }

    @staticmethod
    def learning_history(limit=20):

        limit = max(
            1,
            min(limit, 1000)
        )

        return LEARNING_MEMORY[-limit:]


@router.post(
    "/education/autonomic/evaluate"
)
async def autonomic_evaluate(
    payload: dict
):

    result = (
        EducationalAutonomicRuntime
        .evaluate_student(payload)
    )

    return {
        "result": result,

        "runtime_identity":
        "Educational Autonomic Runtime"
    }


@router.get(
    "/education/autonomic/history"
)
async def autonomic_history(
    limit: int = 20
):

    return {
        "history":
        EducationalAutonomicRuntime
        .learning_history(limit),

        "runtime_identity":
        "Educational Autonomic Runtime"
    }
