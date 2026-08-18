from pathlib import Path
import json
import os
import subprocess
import sys

from fastapi.testclient import TestClient


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

os.environ.setdefault("GRAPH_URI", "bolt://localhost:7687")
os.environ.setdefault("GRAPH_USER", "neo4j")
os.environ.setdefault("GRAPH_PASSWORD", "liceu")
os.environ.setdefault("NATS_URL", "nats://localhost:4222")

import main
from runtime.education.educational_memory_mesh import MEMORY_MESH


def _run_script(*args: str) -> dict[str, object]:
    completed = subprocess.run(
        [sys.executable, *args],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(completed.stdout)


def _get_token(client: TestClient, role: str = "admin") -> str:
    response = client.post(
        "/auth/token",
        json={"subject": "test-admin", "role": role, "expires_minutes": 60},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


def test_interplanetary_knowledge_runtime_accepts_cli_args():
    payload = _run_script(
        "interplanetary_knowledge_runtime.py",
        "--researcher",
        "helena",
        "--track",
        "deep-space-policy",
    )

    assert payload["researcher"] == "helena"
    assert payload["track"] == "deep-space-policy"
    assert payload["mars_engineering"] is True


def test_planet_runtime_earth_triggers_automatic_knowledge_persistence_cycle():
    payload = _run_script(
        "planet_runtime.py",
        "--planet",
        "earth",
        "--track",
        "foundational-earth-cycle",
        "--student-id",
        "earth-cycle-student-01",
        "--researcher",
        "gaia-cycle",
        "--discipline",
        "earth_systems",
        "--scientific-finding",
        "planetary loops increase long-term retention",
        "--model",
        "earth-cycle adaptive model",
        "--lesson-learned",
        "continuous observability improves educational adaptation",
        "--engineering-knowledge",
        "distributed energy labs increase school uptime",
        "--economic-knowledge",
        "skills stackability accelerates regional development",
        "--climate-knowledge",
        "local climate sensing improves adaptation execution",
    )

    assert payload["planet"] == "earth"
    assert payload["track"] == "foundational-earth-cycle"
    assert payload["mars_engineering"] is True

    assert "earth_knowledge_persistence" in payload
    earth_persistence = payload["earth_knowledge_persistence"]
    assert earth_persistence["earth_runtime_state"] == "earth_knowledge_runtime_operational"
    assert earth_persistence["integrations"]["memory_mesh"]["runtime_state"] == "educational_memory_mesh_operational"
    assert earth_persistence["integrations"]["scientific_graph"]["runtime_state"] == "scientific_knowledge_graph_operational"
    assert earth_persistence["integrations"]["scientific_graph"]["node_count"] == 6


def test_planet_runtime_non_earth_does_not_trigger_automatic_knowledge_persistence_cycle():
    payload = _run_script(
        "planet_runtime.py",
        "--planet",
        "mars",
        "--track",
        "orbital-cycle",
        "--student-id",
        "mars-cycle-student-01",
        "--researcher",
        "ares-cycle",
    )

    assert payload["planet"] == "mars"
    assert payload["track"] == "orbital-cycle"
    assert payload["mars_engineering"] is True
    assert "earth_knowledge_persistence" not in payload


def test_scientific_memory_runtime_accepts_cli_args():
    payload = _run_script(
        "scientific_memory_runtime.py",
        "--student-id",
        "student-42",
        "--discipline",
        "astrobiology",
        "--cognition-score",
        "0.81",
        "--consistency",
        "0.74",
        "--engagement",
        "0.95",
    )

    learning_state = payload["learning_state"]
    assert learning_state["student_id"] == "student-42"
    assert learning_state["discipline"] == "astrobiology"
    assert learning_state["cognition_score"] == 0.81
    assert payload["runtime_state"] == "educational_memory_mesh_operational"


def test_continental_scientific_graph_registers_institutional_memory_chain():
    payload = _run_script(
        "continental_scientific_graph_runtime.py",
        "--cause", "the review exposed a retention gap",
        "--decision", "adopt a continuity protocol",
        "--execution", "run the protocol across regional schools",
        "--impact", "handoffs become more reliable",
        "--mitigation", "share the protocol with every coordinator",
        "--result", "continuity variance decreases",
        "--lesson-learned", "shared practice preserves institutional knowledge",
    )

    memory = payload["institutional_memory"]
    assert memory["knowledge_registered"] is True
    assert memory["sequence"] == [
        "event", "cause", "decision", "execution", "impact", "mitigation", "result", "lesson_learned",
    ]
    assert memory["chain_key"] == "eventcausedecisionexecutionimpactmitigationresultlesson_learned"
    assert memory["graph_link"]["source_key"].endswith("::eventcausedecisionexecutionimpactmitigationresultlesson_learned")
    assert memory["graph_link"]["target_key"].endswith("::shared practice preserves institutional knowledge")
    assert memory["nodes_registered"] == 9
    assert memory["edges_created"] == 8

    scientific_memory = payload["scientific_memory"]
    assert scientific_memory["sequence"] == memory["sequence"]
    assert scientific_memory["layers_captured"] == 8
    assert [state["layer"] for state in scientific_memory["captured"]] == memory["sequence"]
    assert scientific_memory["captured"][-1]["content"] == "shared practice preserves institutional knowledge"

    decision_learning = payload["decision_learning"]["record"]
    assert decision_learning["chain_key"] == memory["chain_key"]
    assert decision_learning["lesson_learned"] == "shared practice preserves institutional knowledge"
    assert decision_learning["usable_for_future_decision"] is True
    assert decision_learning["future_decision"]


def test_continental_scientific_graph_runtime_uses_defaults_for_institutional_memory_chain():
    payload = {
        "continent": "south-america",
        "discipline": "educational_policy",
        "source": "partial_payload_test",
        "confidence": 0.91,
        "event": "institutional memory event detected across continental networks",
        "knowledge": "distributed institutional memory accelerates curriculum continuity",
        "relation": "knowledge retention relates to governance confidence",
        "causality": "governance confidence causes adaptive institutional resilience",
    }

    result = main.continental_scientific_graph_run_runtime(payload)

    assert result["continental_scientific_graph_runtime_state"] == "operational"
    assert result["institutional_memory"]["nodes_registered"] == 9
    assert result["institutional_memory"]["edges_created"] == 8


def test_research_lineage_runtime_accepts_cli_flag():
    payload = _run_script(
        "research_lineage_runtime.py",
        "--include-source",
    )

    assert payload["runtime"] == "knowledge_lineage_runtime"
    assert payload["knowledge_lineage_propagation"] == "stable"
    assert payload["knowledge_synchronization_consistency"] == 0.97


def test_global_knowledge_runtime_propagates_all_destinations():
    payload = _run_script(
        "global_knowledge_runtime.py",
        "--discovery",
        "holographic pedagogy",
        "--discipline",
        "education_research",
        "--student-id",
        "student-global",
        "--researcher",
        "aurora",
        "--track",
        "continuity-lab",
        "--cognition-score",
        "0.83",
        "--consistency",
        "0.79",
        "--engagement",
        "0.95",
    )

    assert payload["global_runtime_state"] == "global_knowledge_runtime_operational"
    assert payload["all_destinations_propagated"] is True

    propagation = payload["propagation"]
    assert propagation["knowledge_graph"]["runtime_state"] == "scientific_knowledge_graph_operational"
    assert propagation["training"]["runtime_state"] == "educational_autonomic_operational"
    assert propagation["memory"]["runtime_state"] == "educational_memory_mesh_operational"
    assert propagation["research"]["knowledge_lineage_propagation"] == "stable"


def test_earth_knowledge_runtime_persists_and_integrates_all_knowledge_types():
    payload = _run_script(
        "earth_knowledge_runtime.py",
        "--student-id",
        "earth-student-01",
        "--researcher",
        "gaia",
        "--discipline",
        "earth_systems",
        "--scientific-finding",
        "learning ecologies raise scientific retention",
        "--model",
        "planetary adaptive model",
        "--lesson-learned",
        "feedback loops improve curriculum continuity",
        "--engineering-knowledge",
        "distributed solar labs increase infrastructure uptime",
        "--economic-knowledge",
        "skills compounding improves regional productivity",
        "--climate-knowledge",
        "local climate observatories accelerate adaptation",
    )

    assert payload["earth_runtime_state"] == "earth_knowledge_runtime_operational"

    knowledge_registry = payload["knowledge_registry"]
    assert knowledge_registry["registered_types"] == [
        "scientific_findings",
        "models",
        "lessons_learned",
        "engineering_knowledge",
        "economic_knowledge",
        "climate_knowledge",
    ]

    integrations = payload["integrations"]
    assert integrations["memory_mesh"]["runtime_state"] == "educational_memory_mesh_operational"
    assert integrations["scientific_graph"]["runtime_state"] == "scientific_knowledge_graph_operational"
    assert integrations["scientific_graph"]["node_count"] == 6
    assert integrations["scientific_graph"]["relation_count"] == 5
    assert integrations["knowledge_graph"]["runtime_identity"] == "Knowledge Graph"

    ledger = payload["ledger"]
    assert ledger["total_entries"] >= 1
    assert ledger["ledger_path"].endswith("runtime/storage/earth_knowledge_ledger.json")


def test_continental_knowledge_runtime_persists_institutional_memory():
    payload = _run_script(
        "continental_knowledge_runtime.py",
        "--continent",
        "south-america",
        "--student-id",
        "continental-student-01",
        "--researcher",
        "institucional-matrix",
        "--discipline",
        "educational_policy",
        "--scientific-finding",
        "institutional memory improves long-term governance continuity",
        "--model",
        "continental adaptive learning model",
        "--lesson-learned",
        "cross-border memory stabilizes curriculum adoption",
        "--engineering-knowledge",
        "shared lab networks improve regional teaching infrastructure",
        "--economic-knowledge",
        "institutional memory accelerates public investment in skills",
        "--climate-knowledge",
        "community climate intelligence strengthens adaptation policy",
    )

    assert payload["continental_runtime_state"] == "continental_knowledge_runtime_operational"
    assert payload["knowledge_registry"]["registered_types"] == [
        "scientific_findings",
        "models",
        "lessons_learned",
        "engineering_knowledge",
        "economic_knowledge",
        "climate_knowledge",
    ]
    assert payload["integrations"]["memory_mesh"]["runtime_state"] == "educational_memory_mesh_operational"
    assert payload["integrations"]["scientific_graph"]["runtime_state"] == "scientific_knowledge_graph_operational"
    assert payload["integrations"]["knowledge_graph"]["runtime_identity"] == "Knowledge Graph"


def test_continental_learning_runtime_uses_continental_graph_and_memory_stack():
    payload = _run_script(
        "continental_learning_runtime.py",
        "--continent",
        "europe",
        "--student-id",
        "continental-student-02",
        "--researcher",
        "eu-matrix",
        "--discipline",
        "higher_education",
        "--event",
        "institutional memory event detected across continental networks",
        "--knowledge",
        "distributed institutional memory accelerates curriculum continuity",
        "--relation",
        "knowledge retention relates to governance confidence",
        "--causality",
        "governance confidence causes adaptive institutional resilience",
        "--learning",
        "continental learning loops increase retention and policy coherence",
        "--future-decision",
        "scale institutional memory across every regional learning network",
    )

    assert payload["continental_learning_runtime_state"] == "continental_learning_runtime_operational"
    assert payload["integrations"]["continental_knowledge"]["continental_runtime_state"] == "continental_knowledge_runtime_operational"
    assert payload["integrations"]["continental_graph"]["graph"]["edges_created"] >= 1
    assert payload["integrations"]["continental_training"]["knowledge_graph"]["runtime_state"] == "scientific_knowledge_graph_operational"
    assert payload["decision"]["decision_confidence"] >= 0.0


def test_continental_summary_endpoint_returns_integrated_institutional_memory():
    with TestClient(main.app) as client:
        token = _get_token(client, role="admin")
        response = client.get(
            "/academy/continental/summary",
            headers={
                "Authorization": f"Bearer {token}",
                "x-holding-user-id": "HLD-001",
            },
        )

    assert response.status_code == 200
    body = response.json()
    assert body["runtime_identity"] == "Continental Institutional Memory"
    assert set(body["runtimes"]) == {"knowledge", "learning", "scientific_graph", "institutional_memory"}
    assert body["institutional_memory_status"] in {"ready", "partial"}
    assert "memory_mesh" in body
    assert "scientific_knowledge_graph" in body


def test_local_http_flow_works_with_optional_federation(monkeypatch):
    async def fail_connect():
        raise RuntimeError("nats offline")

    async def fail_publish(subject: str, payload: dict):
        raise RuntimeError("publish unavailable")

    monkeypatch.setattr(main, "FEDERATION_OPTIONAL", True)
    monkeypatch.setattr(main, "AUTH_ENABLED", True)
    monkeypatch.setattr(main.federation_runtime, "connect", fail_connect)
    monkeypatch.setattr(main.federation_runtime, "publish", fail_publish)
    MEMORY_MESH.clear()

    with TestClient(main.app) as client:
        token = _get_token(client, role="admin")
        headers = {"Authorization": f"Bearer {token}"}

        memory_response = client.get("/education/memory-mesh/snapshot")
        metrics_response = client.get("/education/cognition-metrics", headers=headers)
        interplanetary_response = client.post(
            "/interplanetary/curriculum",
            headers=headers,
            json={"researcher": "demo", "track": "orbital-systems"},
        )

    assert memory_response.status_code == 200
    assert memory_response.json()["snapshot"]["mesh_size"] == 0

    assert metrics_response.status_code == 200
    assert metrics_response.json()["educational_continuity_metrics"]["knowledge_lineage"] == "stable"

    assert interplanetary_response.status_code == 200
    assert interplanetary_response.json()["mars_engineering"] is True


def test_wave_86_replays_planetary_institutional_memory_without_duplication(tmp_path, monkeypatch):
    monkeypatch.setenv("ACADEMIA_MEMORY_DB_PATH", str(tmp_path / "academia_memory.db"))
    from planetary_institutional_memory_runtime import read_runtime, run_runtime
    from runtime.education.educational_memory_mesh import (
        INSTITUTIONAL_MEMORY,
        MEMORY_MESH,
        SCIENTIFIC_KNOWLEDGE_EDGES,
        SCIENTIFIC_KNOWLEDGE_NODES,
    )

    payload = {
        "source_event_id": "w85-event-001",
        "trace_id": "w85-trace-001",
        "decision_id": "w82-decision-001",
        "governance_decision_id": "w82-governance-001",
        "execution_id": "w83-execution-001",
        "infrastructure_change_id": "w79-infrastructure-001",
        "supplier_analysis_id": "w80-supplier-001",
        "procurement_plan_id": "w80-procurement-001",
        "economic_impact_id": "w81-economic-001",
        "financial_exposure_id": "w81-financial-001",
        "legal_assessment_id": "w82-legal-001",
        "planetary_operational_state_id": "w85-state-001",
        "initial_hypothesis": "causal memory reduces operational variance",
        "observed_evidence": "the replay preserved every source reference",
        "decision_taken": "reuse the validated institutional protocol",
        "decision_consequence": "the planetary handoff remained consistent",
        "economic_impacts": "regional productivity loss was avoided",
        "financial_impacts": "financial exposure remained bounded",
        "legal_impacts": "the governance record stayed auditable",
        "infrastructure_impacts": "critical service uptime was preserved",
        "supply_chain_impacts": "supplier fallback remained available",
        "identified_risks": "duplicate knowledge registration",
        "mitigators_used": "deterministic identity and replay lookup",
        "final_result": "institutional memory was reconstructed successfully",
        "failures_avoided": "duplicate learning and disconnected lineage",
        "identified_patterns": "state-linked causal chains are reusable",
        "reusable_knowledge": "replay the protocol for future planetary decisions",
        "event": "W79-W85 event envelope",
        "cause": "observed operational variance required analysis",
        "context": "planetary operational state was under governance",
        "decision": "adopt the evidence-informed protocol",
        "execution": "coordinate the protocol across the academy",
        "impact": "continuity improved across institutional handoffs",
        "risk": "uncoordinated replay could duplicate knowledge",
        "mitigation": "use the existing graph and memory registries",
        "result": "the chain became reusable institutional knowledge",
        "lesson_learned": "causal evidence makes planetary memory reusable",
    }

    before = (len(INSTITUTIONAL_MEMORY), len(MEMORY_MESH), len(SCIENTIFIC_KNOWLEDGE_NODES), len(SCIENTIFIC_KNOWLEDGE_EDGES))
    first = run_runtime(payload)
    after_first = (len(INSTITUTIONAL_MEMORY), len(MEMORY_MESH), len(SCIENTIFIC_KNOWLEDGE_NODES), len(SCIENTIFIC_KNOWLEDGE_EDGES))
    second = run_runtime(payload)
    after_second = (len(INSTITUTIONAL_MEMORY), len(MEMORY_MESH), len(SCIENTIFIC_KNOWLEDGE_NODES), len(SCIENTIFIC_KNOWLEDGE_EDGES))

    assert first == second
    assert first["wave"] == 86
    assert first["knowledge_record_id"]
    assert first["lesson_learned_id"]
    assert all(first[field] is True for field in (
        "contract_valid", "lineage_valid", "knowledge_graph_valid",
        "scientific_memory_valid", "institutional_memory_valid",
        "causal_context_valid", "lesson_learned_valid", "knowledge_reuse_valid",
        "persistence_valid", "replay_valid", "idempotency_valid", "rollback_valid",
        "recovery_valid", "audit_valid",
    ))
    assert first["status"] == "PASS"
    assert first["memory_chain_table"] == "academia_memory_chain"
    assert after_first[0] == before[0] + 1
    assert after_second == after_first

    INSTITUTIONAL_MEMORY.clear()
    reopened = read_runtime(first["knowledge_record_id"])
    assert reopened["status"] == "PASS"
    assert reopened["found"] is True
    assert reopened["record"]["lesson_learned_id"] == first["lesson_learned_id"]
    assert reopened["record"]["chain"]["lesson_learned"] == payload["lesson_learned"]
    assert reopened["record"]["source_artifacts"]["planetary_operational_state_id"] == payload["planetary_operational_state_id"]

    restarted = _run_script(
        "planetary_institutional_memory_runtime.py",
        "--read",
        first["knowledge_record_id"],
    )
    assert restarted["status"] == "PASS"
    assert restarted["record"]["knowledge_record_id"] == first["knowledge_record_id"]