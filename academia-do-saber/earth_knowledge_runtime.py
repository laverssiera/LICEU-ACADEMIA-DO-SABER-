import argparse
import asyncio
import json
import os
import sys
import time
from pathlib import Path
from typing import Any


PERSISTENT_LEDGER_PATH = Path(__file__).resolve().parent / "runtime" / "storage" / "earth_knowledge_ledger.json"


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
    parser = argparse.ArgumentParser(description="Run the earth knowledge runtime")
    parser.add_argument("--student-id", default=os.getenv("EARTH_STUDENT_ID", "earth-student"))
    parser.add_argument("--researcher", default=os.getenv("EARTH_RESEARCHER", "earth-researcher"))
    parser.add_argument("--discipline", default=os.getenv("EARTH_DISCIPLINE", "earth_systems"))
    parser.add_argument("--certification", default=os.getenv("EARTH_CERTIFICATION", "earth_runtime_mastery"))
    parser.add_argument("--cognition-score", type=float, default=float(os.getenv("EARTH_COGNITION", "0.9")))
    parser.add_argument("--consistency", type=float, default=float(os.getenv("EARTH_CONSISTENCY", "0.86")))
    parser.add_argument("--engagement", type=float, default=float(os.getenv("EARTH_ENGAGEMENT", "0.93")))
    parser.add_argument(
        "--scientific-finding",
        default=os.getenv("EARTH_SCIENTIFIC_FINDING", "planetary literacy improves long-term scientific retention"),
    )
    parser.add_argument(
        "--model",
        default=os.getenv("EARTH_MODEL", "adaptive earth classroom model with feedback loops"),
    )
    parser.add_argument(
        "--lesson-learned",
        default=os.getenv("EARTH_LESSON_LEARNED", "continuous assessment reduces knowledge decay"),
    )
    parser.add_argument(
        "--engineering-knowledge",
        default=os.getenv("EARTH_ENGINEERING_KNOWLEDGE", "modular solar labs improve resilience of school infrastructure"),
    )
    parser.add_argument(
        "--economic-knowledge",
        default=os.getenv("EARTH_ECONOMIC_KNOWLEDGE", "micro-credential pathways increase employability and local productivity"),
    )
    parser.add_argument(
        "--climate-knowledge",
        default=os.getenv("EARTH_CLIMATE_KNOWLEDGE", "community climate observatories improve adaptation planning"),
    )
    return parser.parse_args()


def _load_ledger() -> dict[str, Any]:
    if not PERSISTENT_LEDGER_PATH.exists():
        return {
            "runtime": "earth_knowledge_runtime",
            "entries": [],
        }

    with PERSISTENT_LEDGER_PATH.open("r", encoding="utf-8") as ledger_file:
        data = json.load(ledger_file)

    if not isinstance(data, dict):
        return {
            "runtime": "earth_knowledge_runtime",
            "entries": [],
        }

    entries = data.get("entries", [])
    if not isinstance(entries, list):
        entries = []

    return {
        "runtime": "earth_knowledge_runtime",
        "entries": entries,
    }


def _persist_entry(payload: dict[str, Any]) -> dict[str, Any]:
    PERSISTENT_LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
    ledger = _load_ledger()

    ledger["entries"].append(payload)

    with PERSISTENT_LEDGER_PATH.open("w", encoding="utf-8") as ledger_file:
        json.dump(ledger, ledger_file, ensure_ascii=True, indent=2, sort_keys=True)

    return {
        "ledger_path": str(PERSISTENT_LEDGER_PATH),
        "total_entries": len(ledger["entries"]),
    }


def _build_knowledge_items(payload: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "knowledge_type": "scientific_findings",
            "content": str(payload["scientific_finding"]),
        },
        {
            "knowledge_type": "models",
            "content": str(payload["model"]),
        },
        {
            "knowledge_type": "lessons_learned",
            "content": str(payload["lesson_learned"]),
        },
        {
            "knowledge_type": "engineering_knowledge",
            "content": str(payload["engineering_knowledge"]),
        },
        {
            "knowledge_type": "economic_knowledge",
            "content": str(payload["economic_knowledge"]),
        },
        {
            "knowledge_type": "climate_knowledge",
            "content": str(payload["climate_knowledge"]),
        },
    ]


async def _propagate_to_knowledge_graph(payload: dict[str, Any], knowledge_items: list[dict[str, str]]) -> dict[str, Any]:
    from graph.knowledge_graph import register_knowledge

    registered = []
    errors = []

    for item in knowledge_items:
        try:
            await register_knowledge(
                user_id=str(payload["researcher"]),
                knowledge_area=item["knowledge_type"],
                certification=str(payload["certification"]),
            )
            registered.append(item["knowledge_type"])
        except Exception as exc:  # pragma: no cover - defensive for external graph runtime
            errors.append(
                {
                    "knowledge_type": item["knowledge_type"],
                    "error": str(exc),
                }
            )

    return {
        "registered_areas": registered,
        "errors": errors,
        "runtime_identity": "Knowledge Graph",
    }


def _propagate_to_memory_mesh(
    payload: dict[str, Any],
    knowledge_items: list[dict[str, str]],
    educational_memory_mesh: Any,
) -> dict[str, Any]:
    base_memory_payload = {
        "student_id": payload["student_id"],
        "discipline": payload["discipline"],
        "cognition_score": payload["cognition_score"],
        "consistency": payload["consistency"],
        "engagement": payload["engagement"],
        "intervention": "earth_knowledge_persistence",
    }
    base_result = educational_memory_mesh.upsert_learning_state(base_memory_payload)

    captured_types = []
    for item in knowledge_items:
        capture_payload = {
            "student_id": payload["student_id"],
            "discipline": f"{payload['discipline']}::{item['knowledge_type']}",
            "cognition_score": payload["cognition_score"],
            "consistency": payload["consistency"],
            "engagement": payload["engagement"],
            # Encodes the captured content in the persistent mesh timeline.
            "intervention": f"earth_knowledge_capture::{item['knowledge_type']}::{item['content']}",
        }
        educational_memory_mesh.upsert_learning_state(capture_payload)
        captured_types.append(item["knowledge_type"])

    return {
        "runtime_state": base_result["runtime_state"],
        "mesh_size": len(educational_memory_mesh.student_memory(payload["student_id"], limit=1000)),
        "knowledge_capture_count": len(captured_types),
        "knowledge_capture_types": captured_types,
    }


async def run_runtime_async(payload: dict[str, Any]) -> dict[str, Any]:
    project_root = Path(__file__).resolve().parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    _load_dotenv()

    from runtime.education.educational_memory_mesh import (
        EducationalMemoryMesh,
        ScientificKnowledgeGraph,
    )

    knowledge_items = _build_knowledge_items(payload)
    now = time.time()

    scientific_nodes = {}
    for item in knowledge_items:
        concept_result = ScientificKnowledgeGraph.upsert_concept(
            {
                "discipline": payload["discipline"],
                "concept": item["content"],
                "confidence": payload["cognition_score"],
                "source": "earth_knowledge_runtime",
                "tags": ["earth_runtime", item["knowledge_type"]],
            }
        )
        scientific_nodes[item["knowledge_type"]] = concept_result["node"]["node_key"]

    relation_results = []
    relation_plan = [
        ("scientific_findings", "models", "validated_by"),
        ("models", "engineering_knowledge", "implemented_by"),
        ("engineering_knowledge", "climate_knowledge", "mitigates"),
        ("economic_knowledge", "climate_knowledge", "funds"),
        ("lessons_learned", "models", "improves"),
    ]

    for source_type, target_type, relation_type in relation_plan:
        link_result = ScientificKnowledgeGraph.link_concepts(
            {
                "discipline": payload["discipline"],
                "source_concept": next(item["content"] for item in knowledge_items if item["knowledge_type"] == source_type),
                "target_concept": next(item["content"] for item in knowledge_items if item["knowledge_type"] == target_type),
                "relation_type": relation_type,
                "weight": 1.0,
            }
        )
        relation_results.append(link_result["relation"])

    memory_result = _propagate_to_memory_mesh(payload, knowledge_items, EducationalMemoryMesh)

    graph_result = await _propagate_to_knowledge_graph(payload, knowledge_items)

    persistent_entry = {
        "timestamp": now,
        "student_id": payload["student_id"],
        "researcher": payload["researcher"],
        "discipline": payload["discipline"],
        "knowledge_items": knowledge_items,
        "scientific_graph_nodes": scientific_nodes,
        "scientific_graph_relations": [
            {
                "source_key": relation["source_key"],
                "target_key": relation["target_key"],
                "relation_type": relation["relation_type"],
                "weight": relation["weight"],
            }
            for relation in relation_results
        ],
        "memory_mesh_capture": {
            "knowledge_capture_count": memory_result["knowledge_capture_count"],
            "knowledge_capture_types": memory_result["knowledge_capture_types"],
        },
    }
    ledger_result = _persist_entry(persistent_entry)

    return {
        "earth_runtime_state": "earth_knowledge_runtime_operational",
        "knowledge_registry": {
            "registered_types": [item["knowledge_type"] for item in knowledge_items],
            "scientific_findings": payload["scientific_finding"],
            "models": payload["model"],
            "lessons_learned": payload["lesson_learned"],
            "engineering_knowledge": payload["engineering_knowledge"],
            "economic_knowledge": payload["economic_knowledge"],
            "climate_knowledge": payload["climate_knowledge"],
        },
        "integrations": {
            "knowledge_graph": graph_result,
            "memory_mesh": {
                "runtime_state": memory_result["runtime_state"],
                "mesh_size": memory_result["mesh_size"],
                "knowledge_capture_count": memory_result["knowledge_capture_count"],
                "knowledge_capture_types": memory_result["knowledge_capture_types"],
            },
            "scientific_graph": {
                "node_count": len(scientific_nodes),
                "relation_count": len(relation_results),
                "runtime_state": "scientific_knowledge_graph_operational",
            },
        },
        "ledger": ledger_result,
    }


def run_runtime(payload: dict[str, Any]) -> dict[str, Any]:
    return asyncio.run(run_runtime_async(payload))


def main() -> None:
    args = _parse_args()
    payload = {
        "student_id": args.student_id,
        "researcher": args.researcher,
        "discipline": args.discipline,
        "certification": args.certification,
        "cognition_score": args.cognition_score,
        "consistency": args.consistency,
        "engagement": args.engagement,
        "scientific_finding": args.scientific_finding,
        "model": args.model,
        "lesson_learned": args.lesson_learned,
        "engineering_knowledge": args.engineering_knowledge,
        "economic_knowledge": args.economic_knowledge,
        "climate_knowledge": args.climate_knowledge,
    }
    result = run_runtime(payload)
    print(json.dumps(result, ensure_ascii=True, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()