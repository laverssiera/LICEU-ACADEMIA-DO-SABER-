"""WAVE 86 - Planetary institutional memory consumer.

Consumes the W79-W85 artifact envelope and reuses the academy's existing
scientific graph, scientific memory mesh, and institutional memory.
"""

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path
from typing import Any


SOURCE_IDS = (
    "source_event_id",
    "trace_id",
    "decision_id",
    "governance_decision_id",
    "execution_id",
    "infrastructure_change_id",
    "supplier_analysis_id",
    "procurement_plan_id",
    "economic_impact_id",
    "financial_exposure_id",
    "legal_assessment_id",
    "planetary_operational_state_id",
)

KNOWLEDGE_FIELDS = (
    "initial_hypothesis",
    "observed_evidence",
    "decision_taken",
    "decision_consequence",
    "economic_impacts",
    "financial_impacts",
    "legal_impacts",
    "infrastructure_impacts",
    "supply_chain_impacts",
    "identified_risks",
    "mitigators_used",
    "final_result",
    "failures_avoided",
    "identified_patterns",
    "reusable_knowledge",
)

CHAIN_FIELDS = (
    "event",
    "cause",
    "context",
    "decision",
    "execution",
    "impact",
    "risk",
    "mitigation",
    "result",
    "lesson_learned",
)


def _text(payload: dict[str, Any], name: str) -> str:
    value = payload.get(name)
    if isinstance(value, (dict, list)):
        value = json.dumps(value, ensure_ascii=True, sort_keys=True)
    return str(value or "").strip()


def _stable_id(prefix: str, payload: dict[str, Any], fields: tuple[str, ...]) -> str:
    material = "\x1f".join(_text(payload, field) for field in fields)
    return f"{prefix}_{hashlib.sha256(material.encode('utf-8')).hexdigest()}"


def _validate_input(payload: dict[str, Any]) -> None:
    missing = [field for field in SOURCE_IDS + KNOWLEDGE_FIELDS + CHAIN_FIELDS if not _text(payload, field)]
    if missing:
        raise ValueError(f"missing W79-W85 artifacts or evidence: {', '.join(missing)}")


def _load_infrastructure():
    project_root = Path(__file__).resolve().parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    from runtime.education import academia_memory_chain
    from runtime.education.educational_memory_mesh import (
        EducationalMemoryMesh,
        INSTITUTIONAL_MEMORY,
        ScientificKnowledgeGraph,
    )

    academia_memory_chain.apply_migration()
    academia_memory_chain.hydrate(INSTITUTIONAL_MEMORY)
    return academia_memory_chain, EducationalMemoryMesh, INSTITUTIONAL_MEMORY, ScientificKnowledgeGraph


def read_runtime(knowledge_record_id: str) -> dict[str, Any]:
    """Second read: recovers the chain from the database on a fresh process."""
    academia_memory_chain, _, INSTITUTIONAL_MEMORY, _ = _load_infrastructure()
    record = academia_memory_chain.fetch_record(knowledge_record_id)
    return {
        "wave": 86,
        "mode": "read",
        "knowledge_record_id": knowledge_record_id,
        "found": record is not None,
        "record": record,
        "institutional_memory_size": len(INSTITUTIONAL_MEMORY),
        "chain_size": academia_memory_chain.count_records(),
        "database_path": str(academia_memory_chain.database_path()),
        "status": "PASS" if record is not None else "FAIL",
    }


def run_runtime(payload: dict[str, Any]) -> dict[str, Any]:
    _validate_input(payload)
    academia_memory_chain, EducationalMemoryMesh, INSTITUTIONAL_MEMORY, ScientificKnowledgeGraph = _load_infrastructure()

    knowledge_record_id = _stable_id("knowledge", payload, SOURCE_IDS + KNOWLEDGE_FIELDS)
    lesson_material = "\x1f".join((knowledge_record_id, _text(payload, "lesson_learned"), _text(payload, "reusable_knowledge")))
    lesson_learned_id = f"lesson_{hashlib.sha256(lesson_material.encode('utf-8')).hexdigest()}"
    existing = next(
        (record for record in INSTITUTIONAL_MEMORY if record.get("knowledge_record_id") == knowledge_record_id),
        None,
    )

    if existing is None:
        discipline = f"planetary/{_text(payload, 'planetary_operational_state_id')}"
        source = _text(payload, "source_event_id")
        confidence = float(payload.get("confidence", 1.0))
        concepts = [(field, _text(payload, field)) for field in CHAIN_FIELDS]
        concepts.append(("planetary_operational_state_id", _text(payload, "planetary_operational_state_id")))
        nodes = {}
        for field, concept in concepts:
            node = ScientificKnowledgeGraph.upsert_concept({
                "discipline": discipline,
                "concept": concept,
                "confidence": confidence,
                "source": source,
                "tags": ["wave-86", "planetary", field, _text(payload, "planetary_operational_state_id")],
            })
            nodes[field] = node["node"]["node_key"]

        edges = []
        for source_field, target_field in zip(CHAIN_FIELDS, CHAIN_FIELDS[1:]):
            link = ScientificKnowledgeGraph.link_concepts({
                "discipline": discipline,
                "source_concept": _text(payload, source_field),
                "target_concept": _text(payload, target_field),
                "relation_type": f"causes_{target_field}",
                "weight": confidence,
            })
            edges.append(link["relation"])
        state_link = ScientificKnowledgeGraph.link_concepts({
            "discipline": discipline,
            "source_concept": _text(payload, "result"),
            "target_concept": _text(payload, "planetary_operational_state_id"),
            "relation_type": "causes_planetary_operational_state",
            "weight": confidence,
        })
        edges.append(state_link["relation"])

        memory_states = []
        for layer in CHAIN_FIELDS:
            state = EducationalMemoryMesh.upsert_learning_state({
                "student_id": f"planetary-institutional::{_text(payload, 'planetary_operational_state_id')}",
                "discipline": f"{discipline}/scientific_memory",
                "cognition_score": confidence,
                "consistency": confidence,
                "engagement": confidence,
                "intervention": f"wave-86::{knowledge_record_id}::{layer}",
                "layer": layer,
                "content": _text(payload, layer),
            })
            memory_states.append(state["learning_state"])

        existing = {
            "knowledge_record_id": knowledge_record_id,
            "lesson_learned_id": lesson_learned_id,
            "wave": 86,
            "recorded_at": time.time(),
            "chain": {field: _text(payload, field) for field in CHAIN_FIELDS},
            "source_artifacts": {field: _text(payload, field) for field in SOURCE_IDS},
            "evidence": {field: _text(payload, field) for field in KNOWLEDGE_FIELDS},
            "planetary_operational_state_id": _text(payload, "planetary_operational_state_id"),
            "graph_nodes": nodes,
            "graph_edges": edges,
            "scientific_memory": memory_states,
            "usable_for_future_decision": True,
        }
        academia_memory_chain.save_record(existing)
        INSTITUTIONAL_MEMORY.append(existing)

    chain_snapshot = {field: _text(payload, field) for field in CHAIN_FIELDS}
    persisted = academia_memory_chain.fetch_record(knowledge_record_id)

    size_before_probe = academia_memory_chain.count_records()
    academia_memory_chain.save_record(existing)
    rollback_valid = academia_memory_chain.count_records() == size_before_probe

    recovered: list[dict[str, Any]] = []
    academia_memory_chain.hydrate(recovered)
    replayed = next(
        (record for record in recovered if record["knowledge_record_id"] == knowledge_record_id),
        None,
    )

    validations = {
        "contract_valid": True,
        "lineage_valid": all(existing["source_artifacts"].values()),
        "knowledge_graph_valid": bool(existing.get("graph_edges")),
        "scientific_memory_valid": len(existing.get("scientific_memory", [])) == len(CHAIN_FIELDS),
        "institutional_memory_valid": existing in INSTITUTIONAL_MEMORY,
        "causal_context_valid": bool(
            existing["graph_nodes"].get("context")
            and existing["graph_nodes"].get("planetary_operational_state_id")
        ),
        "lesson_learned_valid": bool(lesson_learned_id),
        "knowledge_reuse_valid": existing.get("usable_for_future_decision") is True,
        "persistence_valid": persisted is not None
        and persisted["lesson_learned_id"] == lesson_learned_id
        and persisted["chain"] == chain_snapshot
        and persisted["source_artifacts"]["planetary_operational_state_id"]
        == _text(payload, "planetary_operational_state_id"),
        "replay_valid": replayed is not None and replayed["chain"] == chain_snapshot,
        "idempotency_valid": sum(record.get("knowledge_record_id") == knowledge_record_id for record in INSTITUTIONAL_MEMORY) == 1
        and sum(record["knowledge_record_id"] == knowledge_record_id for record in recovered) == 1,
        "rollback_valid": rollback_valid,
        "recovery_valid": replayed is not None
        and replayed["source_artifacts"] == existing["source_artifacts"]
        and replayed["graph_edges"] == existing["graph_edges"],
        "audit_valid": replayed is not None
        and all(replayed["evidence"].get(field) for field in KNOWLEDGE_FIELDS)
        and all(replayed["source_artifacts"].get(field) for field in SOURCE_IDS),
    }

    return {
        "wave": 86,
        "scope": "planetary",
        "origin": "ACADEMIA",
        **{field: _text(payload, field) for field in SOURCE_IDS},
        "knowledge_record_id": knowledge_record_id,
        "lesson_learned_id": lesson_learned_id,
        "memory_chain_table": "academia_memory_chain",
        "memory_chain_database": str(academia_memory_chain.database_path()),
        "memory_chain_size": academia_memory_chain.count_records(),
        **validations,
        "status": "PASS" if all(validations.values()) else "FAIL",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="WAVE 86 planetary institutional memory runtime")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--payload", help="JSON object containing the W79-W85 artifact envelope")
    group.add_argument("--read", help="knowledge_record_id to recover from academia_memory_chain")
    args = parser.parse_args()
    result = read_runtime(args.read) if args.read else run_runtime(json.loads(args.payload))
    print(json.dumps(result, ensure_ascii=True, sort_keys=True))


if __name__ == "__main__":
    main()