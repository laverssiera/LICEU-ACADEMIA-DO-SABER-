import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any


def _load_dotenv() -> None:
    env_path = Path(__file__).resolve().parent / ".env"
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Continental training runtime")
    parser.add_argument("--continent", default=os.getenv("CONTINENT_TRAINING_NAME", "south-america"))
    parser.add_argument("--student-id", default=os.getenv("CONTINENT_TRAINING_STUDENT_ID", "continental-student"))
    parser.add_argument("--researcher", default=os.getenv("CONTINENT_TRAINING_RESEARCHER", "continental-researcher"))
    parser.add_argument("--discipline", default=os.getenv("CONTINENT_TRAINING_DISCIPLINE", "educational_policy"))
    parser.add_argument("--cognition-score", type=float, default=float(os.getenv("CONTINENT_TRAINING_COGNITION", "0.91")))
    parser.add_argument("--consistency", type=float, default=float(os.getenv("CONTINENT_TRAINING_CONSISTENCY", "0.88")))
    parser.add_argument("--engagement", type=float, default=float(os.getenv("CONTINENT_TRAINING_ENGAGEMENT", "0.93")))
    parser.add_argument("--track", default=os.getenv("CONTINENT_TRAINING_TRACK", "institutional-memory"))
    return parser.parse_args()


def run_runtime(payload: dict[str, Any]) -> dict[str, Any]:
    project_root = Path(__file__).resolve().parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    _load_dotenv()

    from runtime.education.educational_autonomic_runtime import EducationalAutonomicRuntime
    from runtime.education.educational_memory_mesh import EducationalMemoryMesh, ScientificKnowledgeGraph

    training_payload = {
        "student_id": payload["student_id"],
        "discipline": payload["discipline"],
        "cognition_score": payload["cognition_score"],
        "consistency": payload["consistency"],
        "engagement": payload["engagement"],
    }

    training_result = EducationalAutonomicRuntime.evaluate_student(training_payload)
    memory_result = EducationalMemoryMesh.upsert_learning_state({
        "student_id": payload["student_id"],
        "discipline": f"{payload['discipline']}::{payload['continent']}",
        "cognition_score": payload["cognition_score"],
        "consistency": payload["consistency"],
        "engagement": payload["engagement"],
        "intervention": f"continental_training::{payload['continent']}::{payload['track']}",
    })
    graph_result = ScientificKnowledgeGraph.upsert_concept({
        "discipline": payload["discipline"],
        "concept": f"training track: {payload['track']}",
        "confidence": payload["cognition_score"],
        "source": "continental_training_runtime",
        "tags": [payload["continent"], "training", "institutional_memory"],
    })

    return {
        "continental_training_runtime_state": "continental_training_runtime_operational",
        "continent": payload["continent"],
        "track": payload["track"],
        "training": training_result,
        "institutional_memory": {
            "runtime_state": memory_result["runtime_state"],
            "mesh_size": memory_result["mesh_size"],
            "intervention": memory_result["learning_state"]["intervention"],
        },
        "knowledge_graph": {
            "runtime_state": graph_result["runtime_state"],
            "node_key": graph_result["node"]["node_key"],
            "total_nodes": graph_result["total_nodes"],
            "total_relations": graph_result["total_relations"],
        },
    }


def main() -> None:
    args = _parse_args()
    payload = {
        "continent": args.continent,
        "student_id": args.student_id,
        "researcher": args.researcher,
        "discipline": args.discipline,
        "cognition_score": args.cognition_score,
        "consistency": args.consistency,
        "engagement": args.engagement,
        "track": args.track,
    }
    result = run_runtime(payload)
    print(json.dumps(result, ensure_ascii=True, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
