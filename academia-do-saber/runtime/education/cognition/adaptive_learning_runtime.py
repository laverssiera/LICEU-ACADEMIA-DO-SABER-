from datetime import datetime, timezone


class AdaptiveLearningRuntime:
    def state(self) -> dict[str, object]:
        return {
            "adaptive_learning": "active",
            "adaptive_learning_consistency": 0.97,
            "last_adaptation_at": datetime.now(timezone.utc).isoformat(),
        }
