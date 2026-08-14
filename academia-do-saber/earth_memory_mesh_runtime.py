"""
WAVE 30 — Earth Memory Mesh Runtime
Aprendizado

Captura o conhecimento produzido pelas waves no EducationalMemoryMesh,
transformando cada unidade de conhecimento em memória persistente de aprendizado.
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any


LEDGER_PATH = Path(__file__).resolve().parent / "runtime" / "storage" / "earth_memory_mesh_ledger.json"


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
    parser = argparse.ArgumentParser(description="Earth Memory Mesh Runtime — Wave 30")
    parser.add_argument("--wave-id", default=os.getenv("EMM_WAVE_ID", "wave-30"))
    parser.add_argument("--student-id", default=os.getenv("EMM_STUDENT_ID", "earth-learner"))
    parser.add_argument("--discipline", default=os.getenv("EMM_DISCIPLINE", "earth_systems"))
    parser.add_argument("--cognition-score", type=float, default=float(os.getenv("EMM_COGNITION", "0.91")))
    parser.add_argument("--consistency", type=float, default=float(os.getenv("EMM_CONSISTENCY", "0.87")))
    parser.add_argument("--engagement", type=float, default=float(os.getenv("EMM_ENGAGEMENT", "0.94")))
    parser.add_argument(
        "--knowledge",
        default=os.getenv("EMM_KNOWLEDGE", "earth-scale educational pattern: distributed cognition accelerates mastery"),
    )
    parser.add_argument(
        "--relation",
        default=os.getenv("EMM_RELATION", "distributed cognition relates to collective intelligence formation"),
    )
    parser.add_argument(
        "--causality",
        default=os.getenv("EMM_CAUSALITY", "collective intelligence causes emergent learning capacity at planetary scale"),
    )
    parser.add_argument(
        "--learning",
        default=os.getenv("EMM_LEARNING", "students in distributed networks achieve mastery 40% faster than isolated learners"),
    )
    return parser.parse_args()


def _load_ledger() -> dict[str, Any]:
    if not LEDGER_PATH.exists():
        return {"runtime": "earth_memory_mesh_runtime", "entries": []}
    with LEDGER_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        return {"runtime": "earth_memory_mesh_runtime", "entries": []}
    entries = data.get("entries", [])
    return {"runtime": "earth_memory_mesh_runtime", "entries": entries if isinstance(entries, list) else []}


def _persist_entry(payload: dict[str, Any]) -> dict[str, Any]:
    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
    ledger = _load_ledger()
    ledger["entries"].append(payload)
    with LEDGER_PATH.open("w", encoding="utf-8") as f:
        json.dump(ledger, f, ensure_ascii=True, indent=2, sort_keys=True)
    return {"ledger_path": str(LEDGER_PATH), "total_entries": len(ledger["entries"])}


def run_runtime(payload: dict[str, Any]) -> dict[str, Any]:
    project_root = Path(__file__).resolve().parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    _load_dotenv()

    from runtime.education.educational_memory_mesh import EducationalMemoryMesh

    now = time.time()
    wave_id   = str(payload["wave_id"])
    student_id = str(payload["student_id"])
    discipline = str(payload["discipline"])
    cognition  = float(payload["cognition_score"])
    consistency = float(payload["consistency"])
    engagement  = float(payload["engagement"])

    # ── Camadas de memória por etapa do pipeline causal completo ──────────
    memory_layers: list[tuple[str, str]] = [
        ("evento",       str(payload["event"])),
        ("conhecimento", str(payload["knowledge"])),
        ("relacao",      str(payload["relation"])),
        ("causalidade",  str(payload["causality"])),
        ("aprendizado",  str(payload["learning"])),
        ("decisao_futura", str(payload["future_decision"])),
    ]

    captured_states = []
    for layer_name, content in memory_layers:
        state_result = EducationalMemoryMesh.upsert_learning_state({
            "student_id":      student_id,
            "discipline":      f"{discipline}::{layer_name}",
            "cognition_score": cognition,
            "consistency":     consistency,
            "engagement":      engagement,
            "intervention":    f"wave_memory::{wave_id}::{layer_name}::{content}",
        })
        captured_states.append({
            "layer":          layer_name,
            "content":        content,
            "signature":      state_result["learning_state"]["signature"],
            "overload_risk":  state_result["learning_state"]["overload_risk"],
            "intervention":   state_result["learning_state"]["intervention"],
        })

    # Snapshot geral do estudante após ingestão
    student_history = EducationalMemoryMesh.student_memory(student_id, limit=1000)
    mesh_snapshot   = EducationalMemoryMesh.mesh_snapshot(limit=1000)

    entry = {
        "timestamp":       now,
        "wave_id":         wave_id,
        "student_id":      student_id,
        "discipline":      discipline,
        "layers_captured": len(captured_states),
        "captured_states": captured_states,
        "student_mesh_size": len(student_history),
        "global_mesh_size":  mesh_snapshot["mesh_size"],
    }

    ledger_result = _persist_entry(entry)

    return {
        "earth_memory_mesh_runtime_state": "operational",
        "wave_id":   wave_id,
        "student_id": student_id,
        "memory_pipeline": {
            "layers_captured": len(captured_states),
            "states": captured_states,
        },
        "mesh_state": {
            "student_entries": len(student_history),
            "global_mesh_size": mesh_snapshot["mesh_size"],
            "intervention_distribution": mesh_snapshot["intervention_distribution"],
        },
        "ledger": ledger_result,
    }


def main() -> None:
    args = _parse_args()
    payload = {
        "wave_id":        args.wave_id,
        "student_id":     args.student_id,
        "discipline":     args.discipline,
        "cognition_score": args.cognition_score,
        "consistency":    args.consistency,
        "engagement":     args.engagement,
        "event":          os.getenv("EMM_EVENT", "planetary-scale learning event detected in wave-30"),
        "knowledge":      args.knowledge,
        "relation":       args.relation,
        "causality":      args.causality,
        "learning":       args.learning,
        "future_decision": os.getenv(
            "EMM_FUTURE_DECISION",
            "expand distributed learning networks across all earth regions to maximise collective intelligence",
        ),
    }
    result = run_runtime(payload)
    print(json.dumps(result, ensure_ascii=True, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
