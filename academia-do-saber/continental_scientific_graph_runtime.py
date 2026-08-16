import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any


LEDGER_PATH = Path(__file__).resolve().parent / "runtime" / "storage" / "continental_scientific_graph_ledger.json"


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
    parser = argparse.ArgumentParser(description="Continental Scientific Graph Runtime")
    parser.add_argument("--continent", default=os.getenv("CONTINENT_GRAPH_NAME", "south-america"))
    parser.add_argument("--discipline", default=os.getenv("CONTINENT_GRAPH_DISCIPLINE", "educational_policy"))
    parser.add_argument("--source", default=os.getenv("CONTINENT_GRAPH_SOURCE", "continental_scientific_graph_runtime"))
    parser.add_argument("--confidence", type=float, default=float(os.getenv("CONTINENT_GRAPH_CONFIDENCE", "0.92")))
    parser.add_argument(
        "--event",
        default=os.getenv("CONTINENT_EVENT", "institutional memory event detected across continental networks"),
    )
    parser.add_argument(
        "--knowledge",
        default=os.getenv("CONTINENT_KNOWLEDGE", "distributed institutional memory accelerates curriculum continuity"),
    )
    parser.add_argument(
        "--relation",
        default=os.getenv("CONTINENT_RELATION", "knowledge retention relates to governance confidence"),
    )
    parser.add_argument(
        "--causality",
        default=os.getenv("CONTINENT_CAUSALITY", "governance confidence causes adaptive institutional resilience"),
    )
    parser.add_argument("--cause", default=os.getenv("CONTINENT_MEMORY_CAUSE", "institutional memory reveals a governance inflection"))
    parser.add_argument("--decision", default=os.getenv("CONTINENT_MEMORY_DECISION", "adopt evidence-informed educational governance"))
    parser.add_argument("--execution", default=os.getenv("CONTINENT_MEMORY_EXECUTION", "coordinate the decision across learning networks"))
    parser.add_argument("--impact", default=os.getenv("CONTINENT_MEMORY_IMPACT", "curriculum continuity and governance confidence improve"))
    parser.add_argument("--mitigation", default=os.getenv("CONTINENT_MEMORY_MITIGATION", "close knowledge gaps through shared institutional practice"))
    parser.add_argument("--result", default=os.getenv("CONTINENT_MEMORY_RESULT", "the intervention stabilizes adaptive institutional resilience"))
    parser.add_argument("--lesson-learned", default=os.getenv("CONTINENT_MEMORY_LESSON_LEARNED", "traceable decisions turn experience into reusable institutional knowledge"))
    parser.add_argument("--future-decision", default=os.getenv("CONTINENT_MEMORY_FUTURE_DECISION", "reuse the lesson in the next evidence-informed governance decision"))
    return parser.parse_args()


def _load_ledger() -> dict[str, Any]:
    if not LEDGER_PATH.exists():
        return {"runtime": "continental_scientific_graph_runtime", "entries": []}
    with LEDGER_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        return {"runtime": "continental_scientific_graph_runtime", "entries": []}
    entries = data.get("entries", [])
    return {"runtime": "continental_scientific_graph_runtime", "entries": entries if isinstance(entries, list) else []}


def _persist_entry(payload: dict[str, Any]) -> dict[str, Any]:
    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
    ledger = _load_ledger()
    ledger["entries"].append(payload)
    with LEDGER_PATH.open("w", encoding="utf-8") as f:
        json.dump(ledger, f, ensure_ascii=True, indent=2, sort_keys=True)
    return {"ledger_path": str(LEDGER_PATH), "total_entries": len(ledger["entries"]) }


def _build_institutional_memory_chain(payload: dict[str, Any]) -> list[tuple[str, Any, str, Any, str]]:
    return [
        ("event", payload["event"], "cause", payload["cause"], "causes"),
        ("cause", payload["cause"], "decision", payload["decision"], "informs_decision"),
        ("decision", payload["decision"], "execution", payload["execution"], "requires_execution"),
        ("execution", payload["execution"], "impact", payload["impact"], "produces_impact"),
        ("impact", payload["impact"], "mitigation", payload["mitigation"], "motivates_mitigation"),
        ("mitigation", payload["mitigation"], "result", payload["result"], "produces_result"),
        ("result", payload["result"], "lesson_learned", payload["lesson_learned"], "generates_lesson_learned"),
    ]


def _capture_scientific_memory(
    payload: dict[str, Any],
    chain: list[tuple[str, Any, str, Any, str]],
) -> dict[str, Any]:
    from runtime.education.educational_memory_mesh import EducationalMemoryMesh

    stages = [("event", payload["event"])] + [
        (target_name, target_concept) for _, _, target_name, target_concept, _ in chain
    ]
    captured = []
    for stage, content in stages:
        result = EducationalMemoryMesh.upsert_learning_state({
            "student_id": f"institutional-memory::{payload['continent']}",
            "discipline": f"{payload['discipline']}/scientific_memory",
            "cognition_score": payload["confidence"],
            "consistency": payload["confidence"],
            "engagement": payload["confidence"],
            "intervention": f"scientific_memory::{stage}::{content}",
            "layer": stage,
            "content": str(content),
        })
        captured.append({
            "layer": stage,
            "content": str(content),
            "signature": result["learning_state"]["signature"],
        })

    return {
        "runtime_state": "educational_memory_mesh_operational",
        "sequence": [stage for stage, _ in stages],
        "layers_captured": len(captured),
        "captured": captured,
    }


def run_runtime(payload: dict[str, Any]) -> dict[str, Any]:
    project_root = Path(__file__).resolve().parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    _load_dotenv()

    payload = dict(payload)
    payload.setdefault("continent", os.getenv("CONTINENT_GRAPH_NAME", "south-america"))
    payload.setdefault("discipline", os.getenv("CONTINENT_GRAPH_DISCIPLINE", "educational_policy"))
    payload.setdefault("source", os.getenv("CONTINENT_GRAPH_SOURCE", "continental_scientific_graph_runtime"))
    payload.setdefault("confidence", float(os.getenv("CONTINENT_GRAPH_CONFIDENCE", "0.92")))
    payload.setdefault("event", os.getenv("CONTINENT_EVENT", "institutional memory event detected across continental networks"))
    payload.setdefault("knowledge", os.getenv("CONTINENT_KNOWLEDGE", "distributed institutional memory accelerates curriculum continuity"))
    payload.setdefault("relation", os.getenv("CONTINENT_RELATION", "knowledge retention relates to governance confidence"))
    payload.setdefault("causality", os.getenv("CONTINENT_CAUSALITY", "governance confidence causes adaptive institutional resilience"))
    payload.setdefault("cause", os.getenv("CONTINENT_MEMORY_CAUSE", "institutional memory reveals a governance inflection"))
    payload.setdefault("decision", os.getenv("CONTINENT_MEMORY_DECISION", "adopt evidence-informed educational governance"))
    payload.setdefault("execution", os.getenv("CONTINENT_MEMORY_EXECUTION", "coordinate the decision across learning networks"))
    payload.setdefault("impact", os.getenv("CONTINENT_MEMORY_IMPACT", "curriculum continuity and governance confidence improve"))
    payload.setdefault("mitigation", os.getenv("CONTINENT_MEMORY_MITIGATION", "close knowledge gaps through shared institutional practice"))
    payload.setdefault("result", os.getenv("CONTINENT_MEMORY_RESULT", "the intervention stabilizes adaptive institutional resilience"))
    payload.setdefault("lesson_learned", os.getenv("CONTINENT_MEMORY_LESSON_LEARNED", "traceable decisions turn experience into reusable institutional knowledge"))
    payload.setdefault("future_decision", os.getenv("CONTINENT_MEMORY_FUTURE_DECISION", "reuse the lesson in the next evidence-informed governance decision"))

    from runtime.education.educational_memory_mesh import EducationalMemoryMesh, ScientificKnowledgeGraph

    now = time.time()
    continent = str(payload["continent"])
    discipline = str(payload["discipline"])
    source = str(payload["source"])
    confidence = float(payload["confidence"])

    event_node = ScientificKnowledgeGraph.upsert_concept({
        "discipline": discipline,
        "concept": str(payload["event"]),
        "confidence": confidence,
        "source": source,
        "tags": [continent, "event", "continental_graph"],
    })

    knowledge_node = ScientificKnowledgeGraph.upsert_concept({
        "discipline": discipline,
        "concept": str(payload["knowledge"]),
        "confidence": confidence,
        "source": source,
        "tags": [continent, "knowledge", "continental_graph"],
    })

    relation_node = ScientificKnowledgeGraph.upsert_concept({
        "discipline": discipline,
        "concept": str(payload["relation"]),
        "confidence": confidence,
        "source": source,
        "tags": [continent, "relation", "continental_graph"],
    })

    causality_node = ScientificKnowledgeGraph.upsert_concept({
        "discipline": discipline,
        "concept": str(payload["causality"]),
        "confidence": confidence,
        "source": source,
        "tags": [continent, "causality", "continental_graph"],
    })

    causal_chain = [
        (payload["event"], payload["knowledge"], "generates_knowledge"),
        (payload["knowledge"], payload["relation"], "establishes_relation"),
        (payload["relation"], payload["causality"], "produces_causality"),
    ]

    institutional_memory_chain = _build_institutional_memory_chain(payload)
    memory_chain_key = "eventcausedecisionexecutionimpactmitigationresultlesson_learned"
    scientific_memory = _capture_scientific_memory(payload, institutional_memory_chain)
    decision_learning = EducationalMemoryMesh.record_decision_learning(payload)

    institutional_memory_nodes = {}
    for node_name, concept in [("event", payload["event"])] + [
        (target_name, target_concept) for _, _, target_name, target_concept, _ in institutional_memory_chain
    ]:
        node = ScientificKnowledgeGraph.upsert_concept({
            "discipline": f"{discipline}/institutional_memory",
            "concept": concept,
            "confidence": confidence,
            "source": source,
            "tags": [continent, "institutional_memory", node_name],
        })
        institutional_memory_nodes[node_name] = node["node"]["node_key"]

    edges = []
    for src, tgt, rel_type in causal_chain:
        link = ScientificKnowledgeGraph.link_concepts({
            "discipline": discipline,
            "source_concept": src,
            "target_concept": tgt,
            "relation_type": rel_type,
            "weight": confidence,
        })
        edges.append({
            "source_key": link["relation"]["source_key"],
            "target_key": link["relation"]["target_key"],
            "relation_type": link["relation"]["relation_type"],
            "weight": link["relation"]["weight"],
        })

    institutional_memory_edges = []
    for _, source_concept, _, target_concept, relation_type in institutional_memory_chain:
        link = ScientificKnowledgeGraph.link_concepts({
            "discipline": f"{discipline}/institutional_memory",
            "source_concept": source_concept,
            "target_concept": target_concept,
            "relation_type": relation_type,
            "weight": confidence,
        })
        institutional_memory_edges.append({
            "source_key": link["relation"]["source_key"],
            "target_key": link["relation"]["target_key"],
            "relation_type": link["relation"]["relation_type"],
            "weight": link["relation"]["weight"],
        })

    memory_chain_node = ScientificKnowledgeGraph.upsert_concept({
        "discipline": f"{discipline}/institutional_memory",
        "concept": memory_chain_key,
        "confidence": confidence,
        "source": source,
        "tags": [continent, "institutional_memory", "memory_chain", "eventcausedecisionexecutionimpactmitigationresultlesson_learned"],
    })
    institutional_memory_nodes["chain_key"] = memory_chain_node["node"]["node_key"]

    memory_chain_link = ScientificKnowledgeGraph.link_concepts({
        "discipline": f"{discipline}/institutional_memory",
        "source_concept": memory_chain_key,
        "target_concept": payload["lesson_learned"],
        "relation_type": "encodes_lesson_learned",
        "weight": confidence,
    })
    institutional_memory_edges.append({
        "source_key": memory_chain_link["relation"]["source_key"],
        "target_key": memory_chain_link["relation"]["target_key"],
        "relation_type": memory_chain_link["relation"]["relation_type"],
        "weight": memory_chain_link["relation"]["weight"],
    })

    snapshot = ScientificKnowledgeGraph.graph_snapshot(discipline=discipline)

    entry = {
        "timestamp": now,
        "continent": continent,
        "discipline": discipline,
        "causal_chain": {
            "event": event_node["node"]["node_key"],
            "knowledge": knowledge_node["node"]["node_key"],
            "relation": relation_node["node"]["node_key"],
            "causality": causality_node["node"]["node_key"],
        },
        "edges": edges,
        "institutional_memory": {
            "chain_key": memory_chain_key,
            "nodes": institutional_memory_nodes,
            "edges": institutional_memory_edges,
            "graph_link": {
                "source_key": memory_chain_link["relation"]["source_key"],
                "target_key": memory_chain_link["relation"]["target_key"],
                "relation_type": memory_chain_link["relation"]["relation_type"],
                "weight": memory_chain_link["relation"]["weight"],
            },
        },
        "scientific_memory": scientific_memory,
        "decision_learning": decision_learning,
        "graph_snapshot": {
            "node_count": snapshot["node_count"],
            "edge_count": snapshot["relation_count"],
        },
    }

    ledger_result = _persist_entry(entry)

    return {
        "continental_scientific_graph_runtime_state": "operational",
        "continent": continent,
        "causal_pipeline": {
            "evento": payload["event"],
            "conhecimento": payload["knowledge"],
            "relacao": payload["relation"],
            "causalidade": payload["causality"],
        },
        "graph": {
            "nodes_registered": 4 + len(institutional_memory_nodes),
            "edges_created": len(edges) + len(institutional_memory_edges),
            "total_nodes": snapshot["node_count"],
            "total_edges": snapshot["relation_count"],
        },
        "institutional_memory": {
            "knowledge_registered": True,
            "sequence": ["event", "cause", "decision", "execution", "impact", "mitigation", "result", "lesson_learned"],
            "chain_key": memory_chain_key,
            "graph_link": {
                "source_key": memory_chain_link["relation"]["source_key"],
                "target_key": memory_chain_link["relation"]["target_key"],
                "relation_type": memory_chain_link["relation"]["relation_type"],
                "weight": memory_chain_link["relation"]["weight"],
            },
            "nodes_registered": len(institutional_memory_nodes),
            "edges_created": len(institutional_memory_edges),
        },
        "scientific_memory": scientific_memory,
        "decision_learning": decision_learning,
        "ledger": ledger_result,
    }


def main() -> None:
    args = _parse_args()
    payload = {
        "continent": args.continent,
        "discipline": args.discipline,
        "source": args.source,
        "confidence": args.confidence,
        "event": args.event,
        "knowledge": args.knowledge,
        "relation": args.relation,
        "causality": args.causality,
        "cause": args.cause,
        "decision": args.decision,
        "execution": args.execution,
        "impact": args.impact,
        "mitigation": args.mitigation,
        "result": args.result,
        "lesson_learned": args.lesson_learned,
        "future_decision": args.future_decision,
    }
    result = run_runtime(payload)
    print(json.dumps(result, ensure_ascii=True, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
