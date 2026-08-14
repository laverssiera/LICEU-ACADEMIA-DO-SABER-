from fastapi import APIRouter
import statistics
import hashlib
import time

router = APIRouter()

REASONING_MEMORY = []


class PedagogicalReasoningRuntime:

    @staticmethod
    def reason(payload: dict) -> dict:
        cognition_score = payload.get("cognition_score", 0.5)
        consistency = payload.get("consistency", 0.5)
        engagement = payload.get("engagement", 0.5)

        overload_risk = round(
            1 - (
                cognition_score * 0.4 +
                consistency * 0.3 +
                engagement * 0.3
            ),
            6,
        )

        mastery_signal = round(
            cognition_score * 0.5 +
            consistency * 0.25 +
            engagement * 0.25,
            6,
        )

        if overload_risk >= 0.7:
            intervention = "autonomous_intervention"
            curriculum_action = "reduce_cognitive_load"
            path_action = "guided_recovery_path"
        elif overload_risk >= 0.5:
            intervention = "adaptive_stabilization"
            curriculum_action = "rebalance_learning_blocks"
            path_action = "adaptive_support_path"
        else:
            intervention = "mastery_acceleration"
            curriculum_action = "advance_curriculum_depth"
            path_action = "accelerated_mastery_path"

        reasoning_state = {
            "timestamp": time.time(),
            "student_id": payload.get("student_id"),
            "discipline": payload.get("discipline"),
            "cognition_score": cognition_score,
            "consistency": consistency,
            "engagement": engagement,
            "overload_risk": overload_risk,
            "mastery_signal": mastery_signal,
            "intervention": intervention,
            "curriculum_action": curriculum_action,
            "path_action": path_action,
            "priority": "intervention_autonomy",
        }

        signature = hashlib.sha256(
            str(reasoning_state).encode()
        ).hexdigest()

        reasoning_state["signature"] = signature
        REASONING_MEMORY.append(reasoning_state)

        global_mastery_signal = statistics.mean(
            [state["mastery_signal"] for state in REASONING_MEMORY]
        )

        return {
            "reasoning_state": reasoning_state,
            "global_mastery_signal": round(global_mastery_signal, 6),
            "memory_size": len(REASONING_MEMORY),
            "runtime_state": "pedagogical_reasoning_operational",
        }

    @staticmethod
    def history(limit: int = 20) -> list[dict]:
        limit = max(1, min(limit, 1000))
        return REASONING_MEMORY[-limit:]


@router.post("/education/pedagogical-reasoning/reason")
async def pedagogical_reason(payload: dict):
    result = PedagogicalReasoningRuntime.reason(payload)
    return {
        "result": result,
        "runtime_identity": "Pedagogical Reasoning Runtime",
    }


@router.get("/education/pedagogical-reasoning/history")
async def pedagogical_reasoning_history(limit: int = 20):
    return {
        "history": PedagogicalReasoningRuntime.history(limit),
        "runtime_identity": "Pedagogical Reasoning Runtime",
    }
