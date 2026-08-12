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


def run_runtime(payload: dict[str, Any]) -> dict[str, Any]:
    project_root = Path(__file__).resolve().parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    _load_dotenv()

    from runtime.education.educational_memory_mesh import ScientificKnowledgeGraph

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
            "nodes_registered": 4,
            "edges_created": len(edges),
            "total_nodes": snapshot["node_count"],
            "total_edges": snapshot["relation_count"],
        },
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
    }
    result = run_runtime(payload)
    print(json.dumps(result, ensure_ascii=True, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
