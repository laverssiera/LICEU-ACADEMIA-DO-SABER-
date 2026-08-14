import argparse
import asyncio
import json
import os
import sys
import time
from pathlib import Path
from typing import Any


LEDGER_PATH = Path(__file__).resolve().parent / "runtime" / "storage" / "continental_learning_ledger.json"


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
    parser = argparse.ArgumentParser(description="Continental learning runtime")
    parser.add_argument("--continent", default=os.getenv("CONTINENT_LEARNING_NAME", "south-america"))
    parser.add_argument("--student-id", default=os.getenv("CONTINENT_LEARNING_STUDENT_ID", "continental-student"))
    parser.add_argument("--researcher", default=os.getenv("CONTINENT_LEARNING_RESEARCHER", "continental-researcher"))
    parser.add_argument("--discipline", default=os.getenv("CONTINENT_LEARNING_DISCIPLINE", "educational_policy"))
    parser.add_argument("--certification", default=os.getenv("CONTINENT_LEARNING_CERTIFICATION", "continental_runtime_mastery"))
    parser.add_argument("--confidence", type=float, default=float(os.getenv("CONTINENT_LEARNING_CONFIDENCE", "0.92")))
    parser.add_argument("--cognition-score", type=float, default=float(os.getenv("CONTINENT_LEARNING_COGNITION", "0.91")))
    parser.add_argument("--consistency", type=float, default=float(os.getenv("CONTINENT_LEARNING_CONSISTENCY", "0.87")))
    parser.add_argument("--engagement", type=float, default=float(os.getenv("CONTINENT_LEARNING_ENGAGEMENT", "0.94")))
    parser.add_argument(
        "--event",
        default=os.getenv("CONTINENT_LEARNING_EVENT", "institutional memory event detected across continental networks"),
    )
    parser.add_argument(
        "--knowledge",
        default=os.getenv("CONTINENT_LEARNING_KNOWLEDGE", "distributed institutional memory accelerates curriculum continuity"),
    )
    parser.add_argument(
        "--relation",
        default=os.getenv("CONTINENT_LEARNING_RELATION", "knowledge retention relates to governance confidence"),
    )
    parser.add_argument(
        "--causality",
        default=os.getenv("CONTINENT_LEARNING_CAUSALITY", "governance confidence causes adaptive institutional resilience"),
    )
    parser.add_argument(
        "--learning",
        default=os.getenv("CONTINENT_LEARNING_LEARNING", "continental learning loops increase retention and policy coherence"),
    )
    parser.add_argument(
        "--future-decision",
        default=os.getenv("CONTINENT_LEARNING_FUTURE_DECISION", "scale institutional memory across every regional learning network"),
    )
    return parser.parse_args()


def _load_ledger() -> dict[str, Any]:
    if not LEDGER_PATH.exists():
        return {"runtime": "continental_learning_runtime", "entries": []}
    with LEDGER_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        return {"runtime": "continental_learning_runtime", "entries": []}
    entries = data.get("entries", [])
    return {"runtime": "continental_learning_runtime", "entries": entries if isinstance(entries, list) else []}


def _persist_entry(payload: dict[str, Any]) -> dict[str, Any]:
    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
    ledger = _load_ledger()
    ledger["entries"].append(payload)
    with LEDGER_PATH.open("w", encoding="utf-8") as f:
        json.dump(ledger, f, ensure_ascii=True, indent=2, sort_keys=True)
    return {"ledger_path": str(LEDGER_PATH), "total_entries": len(ledger["entries"]) }


def _synthesize_future_decision(payload: dict[str, Any], graph_result: dict[str, Any], training_result: dict[str, Any]) -> dict[str, Any]:
    graph_edge_count = graph_result["graph"]["edges_created"]
    training_memory = training_result["institutional_memory"]["mesh_size"]
    decision_confidence = round(min(1.0, (graph_edge_count / 3.0) * 0.6 + (training_memory / 10.0) * 0.4), 6)
    rationale = [
        f"causal graph edges: {graph_edge_count}",
        f"institutional memory entries: {training_memory}",
    ]

    return {
        "decision": str(payload["future_decision"]),
        "decision_confidence": decision_confidence,
        "rationale": "; ".join(rationale),
        "grounded_in": {
            "evento": payload["event"],
            "conhecimento": payload["knowledge"],
            "relacao": payload["relation"],
            "causalidade": payload["causality"],
            "aprendizado": payload["learning"],
        },
    }


async def run_runtime_async(payload: dict[str, Any]) -> dict[str, Any]:
    project_root = Path(__file__).resolve().parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    _load_dotenv()

    from continental_knowledge_runtime import run_runtime_async as continental_knowledge_run_runtime
    from continental_scientific_graph_runtime import run_runtime as run_continental_graph
    from continental_training_runtime import run_runtime as run_continental_training
    from runtime.education.educational_memory_mesh import EducationalMemoryMesh

    now = time.time()

    knowledge_payload = {
        "continent": payload["continent"],
        "student_id": payload["student_id"],
        "researcher": payload["researcher"],
        "discipline": payload["discipline"],
        "certification": payload["certification"],
        "cognition_score": payload["cognition_score"],
        "consistency": payload["consistency"],
        "engagement": payload["engagement"],
        "scientific_finding": payload["event"],
        "model": payload["knowledge"],
        "lesson_learned": payload["learning"],
        "engineering_knowledge": payload["relation"],
        "economic_knowledge": payload["causality"],
        "climate_knowledge": payload["future_decision"],
    }
    knowledge_result = await continental_knowledge_run_runtime(knowledge_payload)

    graph_payload = {
        "continent": payload["continent"],
        "discipline": payload["discipline"],
        "source": "continental_learning_runtime",
        "confidence": payload["confidence"],
        "event": payload["event"],
        "knowledge": payload["knowledge"],
        "relation": payload["relation"],
        "causality": payload["causality"],
        "cause": payload.get("cause", f"cause identified from {payload['event']}"),
        "decision": payload.get("decision", payload["future_decision"]),
        "execution": payload.get("execution", payload["learning"]),
        "impact": payload.get("impact", payload["knowledge"]),
        "mitigation": payload.get("mitigation", payload["relation"]),
        "result": payload.get("result", payload["causality"]),
        "lesson_learned": payload.get("lesson_learned", payload["learning"]),
    }
    graph_result = run_continental_graph(graph_payload)

    training_payload = {
        "continent": payload["continent"],
        "student_id": payload["student_id"],
        "researcher": payload["researcher"],
        "discipline": payload["discipline"],
        "cognition_score": payload["cognition_score"],
        "consistency": payload["consistency"],
        "engagement": payload["engagement"],
        "track": "institutional-memory",
    }
    training_result = run_continental_training(training_payload)

    memory_payload = {
        "student_id": payload["student_id"],
        "discipline": payload["discipline"],
        "cognition_score": payload["cognition_score"],
        "consistency": payload["consistency"],
        "engagement": payload["engagement"],
        "intervention": f"continental_learning::{payload['continent']}::{payload['future_decision']}",
    }
    memory_result = EducationalMemoryMesh.upsert_learning_state(memory_payload)
    decision = _synthesize_future_decision(payload, graph_result, training_result)

    entry = {
        "timestamp": now,
        "continent": payload["continent"],
        "student_id": payload["student_id"],
        "discipline": payload["discipline"],
        "decision": decision,
        "knowledge_result": knowledge_result,
        "graph_result": graph_result,
        "training_result": training_result,
    }
    ledger_result = _persist_entry(entry)

    return {
        "continental_learning_runtime_state": "continental_learning_runtime_operational",
        "continent": payload["continent"],
        "student_id": payload["student_id"],
        "discipline": payload["discipline"],
        "decision": decision,
        "integrations": {
            "continental_knowledge": knowledge_result,
            "continental_graph": graph_result,
            "continental_training": training_result,
            "memory_mesh": {
                "runtime_state": memory_result["runtime_state"],
                "mesh_size": memory_result["mesh_size"],
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
        "confidence": args.confidence,
        "cognition_score": args.cognition_score,
        "consistency": args.consistency,
        "engagement": args.engagement,
        "event": args.event,
        "knowledge": args.knowledge,
        "relation": args.relation,
        "causality": args.causality,
        "learning": args.learning,
        "future_decision": args.future_decision,
    }
    result = run_runtime(payload)
    print(json.dumps(result, ensure_ascii=True, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
