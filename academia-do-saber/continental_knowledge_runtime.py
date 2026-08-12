import argparse
import asyncio
import json
import os
import sys
import time
from pathlib import Path
from typing import Any


PERSISTENT_LEDGER_PATH = Path(__file__).resolve().parent / "runtime" / "storage" / "continental_knowledge_ledger.json"


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
    parser = argparse.ArgumentParser(description="Run the continental knowledge runtime")
    parser.add_argument("--continent", default=os.getenv("CONTINENT_NAME", "south-america"))
    parser.add_argument("--student-id", default=os.getenv("CONTINENT_STUDENT_ID", "continental-student"))
    parser.add_argument("--researcher", default=os.getenv("CONTINENT_RESEARCHER", "continental-researcher"))
    parser.add_argument("--discipline", default=os.getenv("CONTINENT_DISCIPLINE", "educational_policy"))
    parser.add_argument("--certification", default=os.getenv("CONTINENT_CERTIFICATION", "continental_runtime_mastery"))
    parser.add_argument("--cognition-score", type=float, default=float(os.getenv("CONTINENT_COGNITION", "0.92")))
    parser.add_argument("--consistency", type=float, default=float(os.getenv("CONTINENT_CONSISTENCY", "0.89")))
    parser.add_argument("--engagement", type=float, default=float(os.getenv("CONTINENT_ENGAGEMENT", "0.94")))
    parser.add_argument(
        "--scientific-finding",
        default=os.getenv("CONTINENT_SCIENTIFIC_FINDING", "institutional memory stabilizes resilient educational governance"),
    )
    parser.add_argument(
        "--model",
        default=os.getenv("CONTINENT_MODEL", "continental adaptive learning model with resilient memory loops"),
    )
    parser.add_argument(
        "--lesson-learned",
        default=os.getenv("CONTINENT_LESSON_LEARNED", "shared memory improves curriculum continuity across regions"),
    )
    parser.add_argument(
        "--engineering-knowledge",
        default=os.getenv("CONTINENT_ENGINEERING_KNOWLEDGE", "distributed regional labs increase school resilience and educational access"),
    )
    parser.add_argument(
        "--economic-knowledge",
        default=os.getenv("CONTINENT_ECONOMIC_KNOWLEDGE", "institutional memory accelerates regional skills investment and labor mobility"),
    )
    parser.add_argument(
        "--climate-knowledge",
        default=os.getenv("CONTINENT_CLIMATE_KNOWLEDGE", "continental climate intelligence improves adaptation and public planning"),
    )
    return parser.parse_args()


def _load_ledger() -> dict[str, Any]:
    if not PERSISTENT_LEDGER_PATH.exists():
        return {"runtime": "continental_knowledge_runtime", "entries": []}

    with PERSISTENT_LEDGER_PATH.open("r", encoding="utf-8") as ledger_file:
        data = json.load(ledger_file)

    if not isinstance(data, dict):
        return {"runtime": "continental_knowledge_runtime", "entries": []}

    entries = data.get("entries", [])
    return {"runtime": "continental_knowledge_runtime", "entries": entries if isinstance(entries, list) else []}


def _persist_entry(payload: dict[str, Any]) -> dict[str, Any]:
    PERSISTENT_LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
    ledger = _load_ledger()
    ledger["entries"].append(payload)

    with PERSISTENT_LEDGER_PATH.open("w", encoding="utf-8") as ledger_file:
        json.dump(ledger, ledger_file, ensure_ascii=True, indent=2, sort_keys=True)

    return {"ledger_path": str(PERSISTENT_LEDGER_PATH), "total_entries": len(ledger["entries"]) }


def _build_knowledge_items(payload: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {"knowledge_type": "scientific_findings", "content": str(payload["scientific_finding"])},
        {"knowledge_type": "models", "content": str(payload["model"])},
        {"knowledge_type": "lessons_learned", "content": str(payload["lesson_learned"])},
        {"knowledge_type": "engineering_knowledge", "content": str(payload["engineering_knowledge"])},
        {"knowledge_type": "economic_knowledge", "content": str(payload["economic_knowledge"])},
        {"knowledge_type": "climate_knowledge", "content": str(payload["climate_knowledge"])},
    ]


async def _propagate_to_knowledge_graph(payload: dict[str, Any], knowledge_items: list[dict[str, str]]) -> dict[str, Any]:
    from graph.knowledge_graph import register_knowledge

    registered: list[str] = []
    errors: list[dict[str, str]] = []

    for item in knowledge_items:
        try:
            await register_knowledge(
                user_id=str(payload["researcher"]),
                knowledge_area=f"{payload['continent']}::{item['knowledge_type']}",
                certification=str(payload["certification"]),
            )
            registered.append(item["knowledge_type"])
        except Exception as exc:  # pragma: no cover - defensive for external graph runtime
            errors.append({"knowledge_type": item["knowledge_type"], "error": str(exc)})

    return {"registered_areas": registered, "errors": errors, "runtime_identity": "Knowledge Graph"}


def _propagate_to_memory_mesh(payload: dict[str, Any], knowledge_items: list[dict[str, str]], educational_memory_mesh: Any) -> dict[str, Any]:
    base_memory_payload = {
        "student_id": payload["student_id"],
        "discipline": payload["discipline"],
        "cognition_score": payload["cognition_score"],
        "consistency": payload["consistency"],
        "engagement": payload["engagement"],
        "intervention": "continental_knowledge_persistence",
    }
    base_result = educational_memory_mesh.upsert_learning_state(base_memory_payload)

    captured_types: list[str] = []
    for item in knowledge_items:
        capture_payload = {
            "student_id": payload["student_id"],
            "discipline": f"{payload['discipline']}::{payload['continent']}::{item['knowledge_type']}",
            "cognition_score": payload["cognition_score"],
            "consistency": payload["consistency"],
            "engagement": payload["engagement"],
            "intervention": f"continental_knowledge_capture::{payload['continent']}::{item['knowledge_type']}::{item['content']}",
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

    from runtime.education.educational_memory_mesh import EducationalMemoryMesh, ScientificKnowledgeGraph

    knowledge_items = _build_knowledge_items(payload)
    now = time.time()

    scientific_nodes: dict[str, str] = {}
    for item in knowledge_items:
        concept_result = ScientificKnowledgeGraph.upsert_concept(
            {
                "discipline": payload["discipline"],
                "concept": item["content"],
                "confidence": payload["cognition_score"],
                "source": "continental_knowledge_runtime",
                "tags": [payload["continent"], "continental_runtime", item["knowledge_type"]],
            }
        )
        scientific_nodes[item["knowledge_type"]] = concept_result["node"]["node_key"]

    relation_results: list[dict[str, Any]] = []
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
        "continent": payload["continent"],
        "student_id": payload["student_id"],
        "researcher": payload["researcher"],
        "discipline": payload["discipline"],
        "knowledge_items": knowledge_items,
        "scientific_graph_nodes": scientific_nodes,
        "scientific_graph_relations": [
            {"source": relation["source_key"], "target": relation["target_key"], "relation_type": relation["relation_type"]}
            for relation in relation_results
        ],
    }
    ledger_result = _persist_entry(persistent_entry)

    return {
        "continental_runtime_state": "continental_knowledge_runtime_operational",
        "continent": payload["continent"],
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
        "continent": args.continent,
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
