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
    parser = argparse.ArgumentParser(description="Run the global knowledge runtime")
    parser.add_argument("--discovery", default=os.getenv("GLOBAL_DISCOVERY", "educational sovereignty"))
    parser.add_argument("--discipline", default=os.getenv("GLOBAL_DISCIPLINE", "general_science"))
    parser.add_argument("--student-id", default=os.getenv("GLOBAL_STUDENT_ID", "global-demo"))
    parser.add_argument("--researcher", default=os.getenv("GLOBAL_RESEARCHER", "global-researcher"))
    parser.add_argument("--track", default=os.getenv("GLOBAL_TRACK", "knowledge-propagation"))
    parser.add_argument("--cognition-score", type=float, default=float(os.getenv("GLOBAL_COGNITION", "0.9")))
    parser.add_argument("--consistency", type=float, default=float(os.getenv("GLOBAL_CONSISTENCY", "0.88")))
    parser.add_argument("--engagement", type=float, default=float(os.getenv("GLOBAL_ENGAGEMENT", "0.92")))
    return parser.parse_args()


def run_runtime(payload: dict[str, Any]) -> dict[str, Any]:
    project_root = Path(__file__).resolve().parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    _load_dotenv()

    from runtime.education.educational_autonomic_runtime import EducationalAutonomicRuntime
    from runtime.education.educational_memory_mesh import (
        EducationalMemoryMesh,
        ScientificKnowledgeGraph,
    )
    from runtime.education.observability.knowledge_lineage_runtime import KnowledgeLineageRuntime

    discipline = str(payload["discipline"])
    discovery = str(payload["discovery"])

    training_payload = {
        "student_id": payload["student_id"],
        "discipline": discipline,
        "cognition_score": payload["cognition_score"],
        "consistency": payload["consistency"],
        "engagement": payload["engagement"],
    }

    # One discovery fan-outs into graph, training, memory and research lineage.
    knowledge_graph_result = ScientificKnowledgeGraph.upsert_concept(
        {
            "discipline": discipline,
            "concept": discovery,
            "confidence": payload["cognition_score"],
            "source": "global_knowledge_runtime",
            "tags": ["global_discovery", payload["track"]],
        }
    )

    training_result = EducationalAutonomicRuntime.evaluate_student(training_payload)
    memory_result = EducationalMemoryMesh.upsert_learning_state(training_payload)
    research_result = KnowledgeLineageRuntime().lineage()

    return {
        "discovery": {
            "concept": discovery,
            "discipline": discipline,
            "researcher": payload["researcher"],
            "track": payload["track"],
            "student_id": payload["student_id"],
        },
        "propagation": {
            "knowledge_graph": knowledge_graph_result,
            "training": training_result,
            "memory": memory_result,
            "research": research_result,
        },
        "global_runtime_state": "global_knowledge_runtime_operational",
        "all_destinations_propagated": True,
    }


def main() -> None:
    args = _parse_args()
    payload = {
        "discovery": args.discovery,
        "discipline": args.discipline,
        "student_id": args.student_id,
        "researcher": args.researcher,
        "track": args.track,
        "cognition_score": args.cognition_score,
        "consistency": args.consistency,
        "engagement": args.engagement,
    }
    result = run_runtime(payload)
    print(json.dumps(result, ensure_ascii=True, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
