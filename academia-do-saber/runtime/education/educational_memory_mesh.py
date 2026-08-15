from collections import Counter
from fastapi import APIRouter, HTTPException
import hashlib
import statistics
import time
from typing import Any

router = APIRouter()

MEMORY_MESH = []
SCIENTIFIC_KNOWLEDGE_NODES: dict[str, dict[str, Any]] = {}
SCIENTIFIC_KNOWLEDGE_EDGES: list[dict[str, Any]] = []


class EducationalMemoryMesh:

    @staticmethod
    def upsert_learning_state(payload: dict) -> dict:
        cognition_score = payload.get("cognition_score", 0.5)
        consistency = payload.get("consistency", 0.5)
        engagement = payload.get("engagement", 0.5)
        overload_risk = payload.get("overload_risk")

        if overload_risk is None:
            overload_risk = round(
                1 - (
                    cognition_score * 0.4 +
                    consistency * 0.3 +
                    engagement * 0.3
                ),
                6,
            )

        intervention = payload.get("intervention")
        if intervention is None:
            if overload_risk >= 0.7:
                intervention = "critical_recovery"
            elif overload_risk >= 0.5:
                intervention = "adaptive_support"
            else:
                intervention = "accelerated_mastery"

        learning_state = {
            "timestamp": time.time(),
            "student_id": payload.get("student_id"),
            "discipline": payload.get("discipline"),
            "cognition_score": cognition_score,
            "consistency": consistency,
            "engagement": engagement,
            "overload_risk": overload_risk,
            "intervention": intervention,
        }

        for metadata_key in ("layer", "content"):
            if metadata_key in payload:
                learning_state[metadata_key] = payload[metadata_key]

        state_signature = hashlib.sha256(
            str(learning_state).encode()
        ).hexdigest()

        learning_state["signature"] = state_signature
        MEMORY_MESH.append(learning_state)

        overload_average = statistics.mean(
            [state["overload_risk"] for state in MEMORY_MESH]
        )

        return {
            "learning_state": learning_state,
            "mesh_size": len(MEMORY_MESH),
            "mesh_overload_average": round(overload_average, 6),
            "runtime_state": "educational_memory_mesh_operational",
        }

    @staticmethod
    def student_memory(student_id: str, limit: int = 20) -> list[dict]:
        limit = max(1, min(limit, 1000))
        filtered = [
            item
            for item in MEMORY_MESH
            if item.get("student_id") == student_id
        ]
        return filtered[-limit:]

    @staticmethod
    def mesh_snapshot(limit: int = 20) -> dict:
        limit = max(1, min(limit, 1000))
        history = MEMORY_MESH[-limit:]
        intervention_distribution = dict(
            Counter(item.get("intervention", "unknown") for item in history)
        )

        return {
            "history": history,
            "intervention_distribution": intervention_distribution,
            "mesh_size": len(MEMORY_MESH),
        }


class ScientificKnowledgeGraph:

    @staticmethod
    def _normalize_text(value: str) -> str:
        return " ".join(value.strip().split())

    @staticmethod
    def _node_key(discipline: str, concept: str) -> str:
        normalized_discipline = ScientificKnowledgeGraph._normalize_text(discipline).lower()
        normalized_concept = ScientificKnowledgeGraph._normalize_text(concept).lower()
        return f"{normalized_discipline}::{normalized_concept}"

    @staticmethod
    def _sanitize_confidence(confidence: float) -> float:
        return max(0.0, min(1.0, float(confidence)))

    @staticmethod
    def upsert_concept(payload: dict[str, Any]) -> dict[str, Any]:
        concept = str(payload.get("concept", "")).strip()
        if not concept:
            raise ValueError("concept is required")

        discipline = str(payload.get("discipline", "general_science")).strip() or "general_science"
        source = str(payload.get("source", "manual_input")).strip() or "manual_input"
        confidence = ScientificKnowledgeGraph._sanitize_confidence(payload.get("confidence", 0.75))
        raw_tags = payload.get("tags", [])
        tags = []
        if isinstance(raw_tags, list):
            tags = [str(tag).strip() for tag in raw_tags if str(tag).strip()]

        now = time.time()
        node_key = ScientificKnowledgeGraph._node_key(discipline, concept)
        node = SCIENTIFIC_KNOWLEDGE_NODES.get(node_key)

        if node is None:
            node = {
                "node_key": node_key,
                "discipline": ScientificKnowledgeGraph._normalize_text(discipline),
                "concept": ScientificKnowledgeGraph._normalize_text(concept),
                "first_seen": now,
                "last_seen": now,
                "mentions": 1,
                "sources": [source],
                "tags": sorted(set(tags)),
                "confidence_average": confidence,
            }
            SCIENTIFIC_KNOWLEDGE_NODES[node_key] = node
        else:
            node["last_seen"] = now
            node["mentions"] += 1

            if source not in node["sources"]:
                node["sources"].append(source)

            if tags:
                node["tags"] = sorted(set(node["tags"]).union(tags))

            mentions = node["mentions"]
            node["confidence_average"] = round(
                ((node["confidence_average"] * (mentions - 1)) + confidence) / mentions,
                6,
            )

        node["signature"] = hashlib.sha256(
            f"{node_key}:{node['mentions']}:{node['last_seen']}".encode()
        ).hexdigest()

        return {
            "node": node,
            "total_nodes": len(SCIENTIFIC_KNOWLEDGE_NODES),
            "total_relations": len(SCIENTIFIC_KNOWLEDGE_EDGES),
            "runtime_state": "scientific_knowledge_graph_operational",
        }

    @staticmethod
    def link_concepts(payload: dict[str, Any]) -> dict[str, Any]:
        source_concept = str(payload.get("source_concept", "")).strip()
        target_concept = str(payload.get("target_concept", "")).strip()
        if not source_concept or not target_concept:
            raise ValueError("source_concept and target_concept are required")

        discipline = str(payload.get("discipline", "general_science")).strip() or "general_science"
        source_discipline = str(payload.get("source_discipline", discipline)).strip() or discipline
        target_discipline = str(payload.get("target_discipline", discipline)).strip() or discipline
        relation_type = str(payload.get("relation_type", "related_to")).strip() or "related_to"
        weight = max(0.0, float(payload.get("weight", 1.0)))

        source_key = ScientificKnowledgeGraph._node_key(source_discipline, source_concept)
        target_key = ScientificKnowledgeGraph._node_key(target_discipline, target_concept)

        if source_key == target_key:
            raise ValueError("self-relations are not allowed")

        if source_key not in SCIENTIFIC_KNOWLEDGE_NODES:
            ScientificKnowledgeGraph.upsert_concept(
                {
                    "discipline": source_discipline,
                    "concept": source_concept,
                    "confidence": 0.5,
                    "source": "graph_link_autocreate",
                }
            )

        if target_key not in SCIENTIFIC_KNOWLEDGE_NODES:
            ScientificKnowledgeGraph.upsert_concept(
                {
                    "discipline": target_discipline,
                    "concept": target_concept,
                    "confidence": 0.5,
                    "source": "graph_link_autocreate",
                }
            )

        existing = None
        for edge in SCIENTIFIC_KNOWLEDGE_EDGES:
            if (
                edge["source_key"] == source_key
                and edge["target_key"] == target_key
                and edge["relation_type"] == relation_type
            ):
                existing = edge
                break

        now = time.time()
        if existing is None:
            relation = {
                "source_key": source_key,
                "target_key": target_key,
                "relation_type": relation_type,
                "weight": weight,
                "evidence_count": 1,
                "first_seen": now,
                "last_seen": now,
            }
            SCIENTIFIC_KNOWLEDGE_EDGES.append(relation)
        else:
            existing["weight"] = round(existing["weight"] + weight, 6)
            existing["evidence_count"] += 1
            existing["last_seen"] = now
            relation = existing

        return {
            "relation": relation,
            "total_nodes": len(SCIENTIFIC_KNOWLEDGE_NODES),
            "total_relations": len(SCIENTIFIC_KNOWLEDGE_EDGES),
            "runtime_state": "scientific_knowledge_graph_operational",
        }

    @staticmethod
    def concept_snapshot(discipline: str, concept: str) -> dict[str, Any]:
        node_key = ScientificKnowledgeGraph._node_key(discipline, concept)
        node = SCIENTIFIC_KNOWLEDGE_NODES.get(node_key)
        if node is None:
            raise ValueError("concept not found")

        outgoing = []
        incoming = []

        for relation in SCIENTIFIC_KNOWLEDGE_EDGES:
            if relation["source_key"] == node_key:
                outgoing.append(
                    {
                        **relation,
                        "target_concept": SCIENTIFIC_KNOWLEDGE_NODES[relation["target_key"]]["concept"],
                        "target_discipline": SCIENTIFIC_KNOWLEDGE_NODES[relation["target_key"]]["discipline"],
                    }
                )

            if relation["target_key"] == node_key:
                incoming.append(
                    {
                        **relation,
                        "source_concept": SCIENTIFIC_KNOWLEDGE_NODES[relation["source_key"]]["concept"],
                        "source_discipline": SCIENTIFIC_KNOWLEDGE_NODES[relation["source_key"]]["discipline"],
                    }
                )

        return {
            "node": node,
            "incoming_relations": incoming,
            "outgoing_relations": outgoing,
            "runtime_state": "scientific_knowledge_graph_operational",
        }

    @staticmethod
    def graph_snapshot(limit: int = 50, discipline: str | None = None) -> dict[str, Any]:
        limit = max(1, min(limit, 1000))

        filtered_nodes = list(SCIENTIFIC_KNOWLEDGE_NODES.values())
        if discipline:
            normalized = ScientificKnowledgeGraph._normalize_text(discipline).lower()
            filtered_nodes = [
                node for node in filtered_nodes
                if node["discipline"].lower() == normalized
            ]

        filtered_keys = {node["node_key"] for node in filtered_nodes}
        filtered_relations = [
            relation
            for relation in SCIENTIFIC_KNOWLEDGE_EDGES
            if relation["source_key"] in filtered_keys and relation["target_key"] in filtered_keys
        ]

        relation_distribution = dict(Counter(relation["relation_type"] for relation in filtered_relations))
        discipline_distribution = dict(Counter(node["discipline"] for node in filtered_nodes))

        degree_counter: Counter[str] = Counter()
        for relation in filtered_relations:
            degree_counter[relation["source_key"]] += 1
            degree_counter[relation["target_key"]] += 1

        top_concepts = [
            {
                "concept": SCIENTIFIC_KNOWLEDGE_NODES[node_key]["concept"],
                "discipline": SCIENTIFIC_KNOWLEDGE_NODES[node_key]["discipline"],
                "degree": degree,
            }
            for node_key, degree in degree_counter.most_common(limit)
        ]

        recent_nodes = sorted(
            filtered_nodes,
            key=lambda node: node["last_seen"],
            reverse=True,
        )[:limit]

        return {
            "node_count": len(filtered_nodes),
            "relation_count": len(filtered_relations),
            "discipline_distribution": discipline_distribution,
            "relation_distribution": relation_distribution,
            "top_concepts": top_concepts,
            "recent_nodes": recent_nodes,
            "runtime_state": "scientific_knowledge_graph_operational",
        }


@router.post("/education/memory-mesh/upsert")
async def memory_mesh_upsert(payload: dict):
    result = EducationalMemoryMesh.upsert_learning_state(payload)
    return {
        "result": result,
        "runtime_identity": "Educational Memory Mesh",
    }


@router.get("/education/memory-mesh/student/{student_id}")
async def memory_mesh_student(student_id: str, limit: int = 20):
    return {
        "student_id": student_id,
        "history": EducationalMemoryMesh.student_memory(student_id, limit),
        "runtime_identity": "Educational Memory Mesh",
    }


@router.get("/education/memory-mesh/snapshot")
async def memory_mesh_snapshot(limit: int = 20):
    return {
        "snapshot": EducationalMemoryMesh.mesh_snapshot(limit),
        "runtime_identity": "Educational Memory Mesh",
    }


@router.post("/education/scientific-knowledge-graph/concepts/upsert")
async def scientific_knowledge_graph_upsert(payload: dict):
    try:
        result = ScientificKnowledgeGraph.upsert_concept(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {
        "result": result,
        "runtime_identity": "Scientific Knowledge Graph",
    }


@router.post("/education/scientific-knowledge-graph/relations/link")
async def scientific_knowledge_graph_link(payload: dict):
    try:
        result = ScientificKnowledgeGraph.link_concepts(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {
        "result": result,
        "runtime_identity": "Scientific Knowledge Graph",
    }


@router.get("/education/scientific-knowledge-graph/concepts/{discipline}/{concept}")
async def scientific_knowledge_graph_concept(discipline: str, concept: str):
    try:
        result = ScientificKnowledgeGraph.concept_snapshot(discipline, concept)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    return {
        "result": result,
        "runtime_identity": "Scientific Knowledge Graph",
    }


@router.get("/education/scientific-knowledge-graph/snapshot")
async def scientific_knowledge_graph_snapshot(limit: int = 50, discipline: str | None = None):
    return {
        "snapshot": ScientificKnowledgeGraph.graph_snapshot(limit=limit, discipline=discipline),
        "runtime_identity": "Scientific Knowledge Graph",
    }
