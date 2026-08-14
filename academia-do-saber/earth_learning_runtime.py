"""
WAVE 30 — Earth Learning Runtime
Orquestrador completo do pipeline de conhecimento:

    Evento → Conhecimento → Relação → Causalidade → Aprendizado → Decisão futura

Executa earth_knowledge_graph_runtime e earth_memory_mesh_runtime em sequência
e sintetiza uma Decisão futura a partir do aprendizado acumulado.
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any


LEDGER_PATH = Path(__file__).resolve().parent / "runtime" / "storage" / "earth_learning_ledger.json"


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
    parser = argparse.ArgumentParser(description="Earth Learning Runtime — Wave 30")
    parser.add_argument("--wave-id", default=os.getenv("ELR_WAVE_ID", "wave-30"))
    parser.add_argument("--student-id", default=os.getenv("ELR_STUDENT_ID", "earth-learner"))
    parser.add_argument("--researcher", default=os.getenv("ELR_RESEARCHER", "earth-researcher"))
    parser.add_argument("--discipline", default=os.getenv("ELR_DISCIPLINE", "earth_systems"))
    parser.add_argument("--confidence", type=float, default=float(os.getenv("ELR_CONFIDENCE", "0.91")))
    parser.add_argument("--cognition-score", type=float, default=float(os.getenv("ELR_COGNITION", "0.91")))
    parser.add_argument("--consistency", type=float, default=float(os.getenv("ELR_CONSISTENCY", "0.87")))
    parser.add_argument("--engagement", type=float, default=float(os.getenv("ELR_ENGAGEMENT", "0.94")))
    # Pipeline causal completo
    parser.add_argument(
        "--event",
        default=os.getenv("ELR_EVENT", "planetary-scale learning event detected in wave-30"),
    )
    parser.add_argument(
        "--knowledge",
        default=os.getenv("ELR_KNOWLEDGE", "earth-scale educational pattern: distributed cognition accelerates mastery"),
    )
    parser.add_argument(
        "--relation",
        default=os.getenv("ELR_RELATION", "distributed cognition relates to collective intelligence formation"),
    )
    parser.add_argument(
        "--causality",
        default=os.getenv("ELR_CAUSALITY", "collective intelligence causes emergent learning capacity at planetary scale"),
    )
    parser.add_argument(
        "--learning",
        default=os.getenv("ELR_LEARNING", "students in distributed networks achieve mastery 40% faster than isolated learners"),
    )
    parser.add_argument(
        "--future-decision",
        default=os.getenv(
            "ELR_FUTURE_DECISION",
            "expand distributed learning networks across all earth regions to maximise collective intelligence",
        ),
    )
    return parser.parse_args()


def _load_ledger() -> dict[str, Any]:
    if not LEDGER_PATH.exists():
        return {"runtime": "earth_learning_runtime", "entries": []}
    with LEDGER_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        return {"runtime": "earth_learning_runtime", "entries": []}
    entries = data.get("entries", [])
    return {"runtime": "earth_learning_runtime", "entries": entries if isinstance(entries, list) else []}


def _persist_entry(payload: dict[str, Any]) -> dict[str, Any]:
    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
    ledger = _load_ledger()
    ledger["entries"].append(payload)
    with LEDGER_PATH.open("w", encoding="utf-8") as f:
        json.dump(ledger, f, ensure_ascii=True, indent=2, sort_keys=True)
    return {"ledger_path": str(LEDGER_PATH), "total_entries": len(ledger["entries"])}


def _synthesize_future_decision(
    payload: dict[str, Any],
    graph_result: dict[str, Any],
    mesh_result: dict[str, Any],
) -> dict[str, Any]:
    """
    Sintetiza a Decisão futura com base no aprendizado acumulado no grafo e na mesh.
    A decisão é ponderada pela média de confiança do grafo e saúde da mesh de memória.
    """
    graph_edge_count   = graph_result["graph"]["edges_created"]
    mesh_layers        = mesh_result["memory_pipeline"]["layers_captured"]
    mesh_student_size  = mesh_result["mesh_state"]["student_entries"]

    # Pontuação composta: grafo causal + profundidade de memória
    causal_depth_score = min(1.0, graph_edge_count / 3.0)
    memory_depth_score = min(1.0, mesh_student_size / 10.0)
    decision_confidence = round(
        causal_depth_score * 0.5 + memory_depth_score * 0.3 + float(payload["confidence"]) * 0.2,
        6,
    )

    rationale_parts = [
        f"causal chain depth: {graph_edge_count} edges",
        f"memory layers absorbed: {mesh_layers}",
        f"student memory entries: {mesh_student_size}",
    ]

    return {
        "decision": str(payload["future_decision"]),
        "decision_confidence": decision_confidence,
        "rationale": "; ".join(rationale_parts),
        "grounded_in": {
            "evento":      payload["event"],
            "conhecimento": payload["knowledge"],
            "relacao":     payload["relation"],
            "causalidade": payload["causality"],
            "aprendizado": payload["learning"],
        },
    }


def run_runtime(payload: dict[str, Any]) -> dict[str, Any]:
    project_root = Path(__file__).resolve().parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    _load_dotenv()

    from earth_knowledge_graph_runtime import run_runtime as run_knowledge_graph
    from earth_memory_mesh_runtime import run_runtime as run_memory_mesh

    now = time.time()

    # ── Fase 1–4: Evento → Conhecimento → Relação → Causalidade ──────────
    kg_payload = {
        "wave_id":    payload["wave_id"],
        "discipline": payload["discipline"],
        "source":     "earth_learning_runtime",
        "confidence": payload["confidence"],
        "event":      payload["event"],
        "knowledge":  payload["knowledge"],
        "relation":   payload["relation"],
        "causality":  payload["causality"],
    }
    graph_result = run_knowledge_graph(kg_payload)

    # ── Fase 5: Aprendizado ───────────────────────────────────────────────
    mm_payload = {
        "wave_id":        payload["wave_id"],
        "student_id":     payload["student_id"],
        "discipline":     payload["discipline"],
        "cognition_score": payload["cognition_score"],
        "consistency":    payload["consistency"],
        "engagement":     payload["engagement"],
        "event":          payload["event"],
        "knowledge":      payload["knowledge"],
        "relation":       payload["relation"],
        "causality":      payload["causality"],
        "learning":       payload["learning"],
        "future_decision": payload["future_decision"],
    }
    mesh_result = run_memory_mesh(mm_payload)

    # ── Fase 6: Decisão futura ────────────────────────────────────────────
    future_decision = _synthesize_future_decision(payload, graph_result, mesh_result)

    entry = {
        "timestamp":       now,
        "wave_id":         payload["wave_id"],
        "student_id":      payload["student_id"],
        "discipline":      payload["discipline"],
        "pipeline": {
            "evento":       payload["event"],
            "conhecimento":  payload["knowledge"],
            "relacao":      payload["relation"],
            "causalidade":  payload["causality"],
            "aprendizado":  payload["learning"],
            "decisao_futura": future_decision["decision"],
        },
        "graph_ledger":  graph_result["ledger"],
        "mesh_ledger":   mesh_result["ledger"],
        "decision_confidence": future_decision["decision_confidence"],
    }

    ledger_result = _persist_entry(entry)

    return {
        "earth_learning_runtime_state": "operational",
        "wave_id":   payload["wave_id"],
        "student_id": payload["student_id"],
        "pipeline": {
            "1_evento":        payload["event"],
            "2_conhecimento":  payload["knowledge"],
            "3_relacao":       payload["relation"],
            "4_causalidade":   payload["causality"],
            "5_aprendizado":   payload["learning"],
            "6_decisao_futura": future_decision,
        },
        "integrations": {
            "earth_knowledge_graph": {
                "runtime_state": graph_result["earth_knowledge_graph_runtime_state"],
                "graph":         graph_result["graph"],
            },
            "earth_memory_mesh": {
                "runtime_state": mesh_result["earth_memory_mesh_runtime_state"],
                "memory_pipeline": mesh_result["memory_pipeline"],
                "mesh_state":      mesh_result["mesh_state"],
            },
        },
        "ledger": ledger_result,
    }


def main() -> None:
    args = _parse_args()
    payload = {
        "wave_id":        args.wave_id,
        "student_id":     args.student_id,
        "researcher":     args.researcher,
        "discipline":     args.discipline,
        "confidence":     args.confidence,
        "cognition_score": args.cognition_score,
        "consistency":    args.consistency,
        "engagement":     args.engagement,
        "event":          args.event,
        "knowledge":      args.knowledge,
        "relation":       args.relation,
        "causality":      args.causality,
        "learning":       args.learning,
        "future_decision": args.future_decision,
    }
    result = run_runtime(payload)
    print(json.dumps(result, ensure_ascii=True, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
