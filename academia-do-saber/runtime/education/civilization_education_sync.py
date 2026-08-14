from fastapi import APIRouter
import hashlib
import statistics
import time

router = APIRouter()

CIVILIZATION_SYNC_MEMORY = []


class CivilizationEducationSync:

    @staticmethod
    def synchronize(payload: dict) -> dict:
        cognition_sync = payload.get("cognition_sync", 0.5)
        curriculum_sync = payload.get("curriculum_sync", 0.5)
        intervention_sync = payload.get("intervention_sync", 0.5)

        federation_sync_score = round(
            cognition_sync * 0.4 +
            curriculum_sync * 0.3 +
            intervention_sync * 0.3,
            6,
        )

        if federation_sync_score >= 0.8:
            sync_state = "civilization_sync_stable"
            orchestrator_action = "advance_federated_curriculum"
        elif federation_sync_score >= 0.6:
            sync_state = "civilization_sync_adaptive"
            orchestrator_action = "rebalance_federated_curriculum"
        else:
            sync_state = "civilization_sync_recovery"
            orchestrator_action = "recover_federated_alignment"

        sync_payload = {
            "timestamp": time.time(),
            "federation_id": payload.get("federation_id", "academy-federation"),
            "region": payload.get("region", "global"),
            "cognition_sync": cognition_sync,
            "curriculum_sync": curriculum_sync,
            "intervention_sync": intervention_sync,
            "federation_sync_score": federation_sync_score,
            "sync_state": sync_state,
            "orchestrator_action": orchestrator_action,
        }

        signature = hashlib.sha256(str(sync_payload).encode()).hexdigest()
        sync_payload["signature"] = signature

        CIVILIZATION_SYNC_MEMORY.append(sync_payload)

        global_sync = statistics.mean(
            [item["federation_sync_score"] for item in CIVILIZATION_SYNC_MEMORY]
        )

        return {
            "sync_payload": sync_payload,
            "global_sync_score": round(global_sync, 6),
            "memory_size": len(CIVILIZATION_SYNC_MEMORY),
            "runtime_state": "civilization_education_sync_operational",
        }

    @staticmethod
    def history(limit: int = 20) -> list[dict]:
        limit = max(1, min(limit, 1000))
        return CIVILIZATION_SYNC_MEMORY[-limit:]


@router.post("/education/civilization-sync/synchronize")
async def civilization_sync_synchronize(payload: dict):
    result = CivilizationEducationSync.synchronize(payload)
    return {
        "result": result,
        "runtime_identity": "Civilization Education Sync",
    }


@router.get("/education/civilization-sync/history")
async def civilization_sync_history(limit: int = 20):
    return {
        "history": CivilizationEducationSync.history(limit),
        "runtime_identity": "Civilization Education Sync",
    }
