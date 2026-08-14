from pathlib import Path
import sys
import os
import asyncio
import json
import queue
import threading
import copy

import pytest

from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).resolve().parents[1]))

from nats.aio.client import Client as NATS
from runtime.education.educational_autonomic_runtime import LEARNING_MEMORY
from runtime.education.educational_memory_mesh import (
    MEMORY_MESH,
    SCIENTIFIC_KNOWLEDGE_EDGES,
    SCIENTIFIC_KNOWLEDGE_NODES,
)
from runtime.education.pedagogical_reasoning_runtime import REASONING_MEMORY
from runtime.education.civilization_education_sync import CIVILIZATION_SYNC_MEMORY
from runtime.education.federated_learning_identity import FEDERATED_IDENTITY_MEMORY

os.environ.setdefault("GRAPH_URI", "bolt://localhost:7687")
os.environ.setdefault("GRAPH_USER", "neo4j")
os.environ.setdefault("GRAPH_PASSWORD", "liceu")
os.environ.setdefault("NATS_URL", "nats://localhost:4222")

import main


def _get_token(client: TestClient, role: str = "professor") -> str:
    response = client.post(
        "/auth/token",
        json={"subject": "test-user", "role": role, "expires_minutes": 60},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


def test_health_is_public(monkeypatch):
    async def fake_connect():
        return None

    monkeypatch.setattr(main.federation_runtime, "connect", fake_connect)

    with TestClient(main.app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["runtime"] == "academia-do-saber"


def test_protected_route_requires_bearer(monkeypatch):
    async def fake_connect():
        return None

    monkeypatch.setattr(main.federation_runtime, "connect", fake_connect)

    with TestClient(main.app) as client:
        response = client.post(
            "/courses",
            json={
                "course_id": "ENG-101",
                "title": "Orbital Engineering",
                "area": "space-engineering",
                "instructor": "John Professor",
            },
        )
        assert response.status_code == 401


def test_course_with_token_publishes_event_and_exposes_metrics(monkeypatch):
    async def fake_connect():
        return None

    published_events: list[tuple[str, dict]] = []

    async def fake_publish(subject: str, payload: dict):
        published_events.append((subject, payload))

    monkeypatch.setattr(main.federation_runtime, "connect", fake_connect)
    monkeypatch.setattr(main.federation_runtime, "publish", fake_publish)

    with TestClient(main.app) as client:
        token = _get_token(client, role="professor")
        headers = {"Authorization": f"Bearer {token}"}

        response = client.post(
            "/courses",
            headers=headers,
            json={
                "course_id": "MARS-101",
                "title": "Mars City Simulation",
                "area": "interplanetary",
                "instructor": "John Professor",
            },
        )

        assert response.status_code == 200
        assert response.json()["created"] is True
        assert published_events
        subjects = [event[0] for event in published_events]
        assert "liceu.academia.course.created" in subjects
        assert "liceu.academia.authorization.audit" in subjects

        metrics = client.get("/metrics")
        assert metrics.status_code == 200
        assert "academia_subject_events_total" in metrics.text
        assert 'subject="liceu.academia.course.created"' in metrics.text


def test_role_forbidden_returns_403(monkeypatch):
    async def fake_connect():
        return None

    async def fake_publish(subject: str, payload: dict):
        return None

    monkeypatch.setattr(main.federation_runtime, "connect", fake_connect)
    monkeypatch.setattr(main.federation_runtime, "publish", fake_publish)

    with TestClient(main.app) as client:
        token = _get_token(client, role="viewer")
        headers = {"Authorization": f"Bearer {token}"}
        response = client.post(
            "/courses",
            headers=headers,
            json={
                "course_id": "MARS-102",
                "title": "Mars Law",
                "area": "juridicotech",
                "instructor": "John Professor",
            },
        )
        assert response.status_code == 403


def test_rbac_status_and_reload(monkeypatch, tmp_path):
    async def fake_connect():
        return None

    async def fake_publish(subject: str, payload: dict):
        return None

    policy_file = tmp_path / "rbac_policy.json"
    policy_file.write_text(
        json.dumps(
            {
                "version": "9.9.9",
                "permissions": {
                    "courses.create": ["viewer"],
                    "certifications.issue": ["admin"],
                    "knowledge.register": ["admin"],
                    "collective.synchronize": ["admin"],
                    "holographic.rooms.create": ["admin"],
                    "interplanetary.curriculum": ["admin"],
                    "agents.john.mentor": ["admin"],
                    "admin.rbac.status": ["admin"],
                    "admin.rbac.reload": ["admin"],
                },
            }
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(main.federation_runtime, "connect", fake_connect)
    monkeypatch.setattr(main.federation_runtime, "publish", fake_publish)
    monkeypatch.setattr(main, "RBAC_POLICY_PATH", str(policy_file))

    original_state = copy.deepcopy(main.RBAC_STATE)
    try:
        with TestClient(main.app) as client:
            admin_token = _get_token(client, role="admin")
            admin_headers = {"Authorization": f"Bearer {admin_token}"}

            reload_response = client.post("/admin/rbac/reload", headers=admin_headers)
            assert reload_response.status_code == 200
            assert reload_response.json()["version"] == "9.9.9"
            assert reload_response.json()["checksum"]

            status_response = client.get("/admin/rbac/status", headers=admin_headers)
            assert status_response.status_code == 200
            assert status_response.json()["version"] == "9.9.9"
            assert status_response.json()["checksum"]

            viewer_token = _get_token(client, role="viewer")
            viewer_headers = {"Authorization": f"Bearer {viewer_token}"}
            course_response = client.post(
                "/courses",
                headers=viewer_headers,
                json={
                    "course_id": "VIEW-1",
                    "title": "Viewer Allowed by Reload",
                    "area": "federation",
                    "instructor": "John Professor",
                },
            )
            assert course_response.status_code == 200
    finally:
        main.RBAC_STATE = original_state


def test_authorization_audit_emits_allow_and_deny(monkeypatch):
    async def fake_connect():
        return None

    published_events: list[tuple[str, dict]] = []

    async def fake_publish(subject: str, payload: dict):
        published_events.append((subject, payload))

    monkeypatch.setattr(main.federation_runtime, "connect", fake_connect)
    monkeypatch.setattr(main.federation_runtime, "publish", fake_publish)

    with TestClient(main.app) as client:
        deny_token = _get_token(client, role="viewer")
        deny_headers = {"Authorization": f"Bearer {deny_token}"}
        deny_response = client.post(
            "/courses",
            headers=deny_headers,
            json={
                "course_id": "DENY-1",
                "title": "Denied",
                "area": "federation",
                "instructor": "John Professor",
            },
        )
        assert deny_response.status_code == 403

        allow_token = _get_token(client, role="professor")
        allow_headers = {"Authorization": f"Bearer {allow_token}"}
        allow_response = client.post(
            "/courses",
            headers=allow_headers,
            json={
                "course_id": "ALLOW-1",
                "title": "Allowed",
                "area": "federation",
                "instructor": "John Professor",
            },
        )
        assert allow_response.status_code == 200

    audits = [payload for subject, payload in published_events if subject == "liceu.academia.authorization.audit"]
    assert audits
    decisions = {entry["decision"] for entry in audits}
    assert "deny" in decisions
    assert "allow" in decisions


def test_knowledge_register_fallback_on_graph_error(monkeypatch):
    async def fake_connect():
        return None

    async def fake_publish(subject: str, payload: dict):
        return None

    async def fake_register_knowledge(**kwargs):
        raise RuntimeError("graph unavailable")

    monkeypatch.setattr(main.federation_runtime, "connect", fake_connect)
    monkeypatch.setattr(main.federation_runtime, "publish", fake_publish)
    monkeypatch.setattr(main, "register_knowledge", fake_register_knowledge)

    with TestClient(main.app) as client:
        token = _get_token(client, role="researcher")
        headers = {"Authorization": f"Bearer {token}"}
        response = client.post(
            "/knowledge/register",
            headers=headers,
            json={
                "user_id": "u-test",
                "knowledge_area": "orbital_architecture",
                "certification": "space_law",
            },
        )
        assert response.status_code == 200
        body = response.json()
        assert body["registered"] is False
        assert "graph_error" in body


def test_earth_knowledge_persist_endpoint_integrates_mesh_and_graph(monkeypatch):
    async def fake_connect():
        return None

    async def fake_publish(subject: str, payload: dict):
        return None

    monkeypatch.setattr(main.federation_runtime, "connect", fake_connect)
    monkeypatch.setattr(main.federation_runtime, "publish", fake_publish)
    MEMORY_MESH.clear()
    SCIENTIFIC_KNOWLEDGE_NODES.clear()
    SCIENTIFIC_KNOWLEDGE_EDGES.clear()

    with TestClient(main.app) as client:
        token = _get_token(client, role="researcher")
        headers = {"Authorization": f"Bearer {token}"}
        response = client.post(
            "/earth/knowledge/persist",
            headers=headers,
            json={
                "student_id": "earth-student-http",
                "researcher": "gaia",
                "discipline": "earth_systems",
                "certification": "earth_runtime_mastery",
                "cognition_score": 0.87,
                "consistency": 0.83,
                "engagement": 0.94,
                "scientific_finding": "systems learning increases retention",
                "model": "earth adaptive model",
                "lesson_learned": "feedback shortens adaptation cycles",
                "engineering_knowledge": "solar labs strengthen local resilience",
                "economic_knowledge": "skills mobility expands local productivity",
                "climate_knowledge": "community observatories improve adaptation readiness",
            },
        )

    assert response.status_code == 200
    body = response.json()
    assert body["earth_runtime_state"] == "earth_knowledge_runtime_operational"
    assert body["knowledge_registry"]["registered_types"] == [
        "scientific_findings",
        "models",
        "lessons_learned",
        "engineering_knowledge",
        "economic_knowledge",
        "climate_knowledge",
    ]
    assert body["integrations"]["memory_mesh"]["runtime_state"] == "educational_memory_mesh_operational"
    assert body["integrations"]["scientific_graph"]["runtime_state"] == "scientific_knowledge_graph_operational"
    assert body["integrations"]["scientific_graph"]["node_count"] == 6
    assert body["integrations"]["scientific_graph"]["relation_count"] == 5
    assert body["ledger"]["total_entries"] >= 1


def test_autonomic_runtime_evaluate_and_history(monkeypatch):
    async def fake_connect():
        return None

    monkeypatch.setattr(main.federation_runtime, "connect", fake_connect)
    LEARNING_MEMORY.clear()

    with TestClient(main.app) as client:
        evaluate = client.post(
            "/education/autonomic/evaluate",
            json={
                "student_id": "student-001",
                "discipline": "physics",
                "cognition_score": 0.82,
                "consistency": 0.74,
                "engagement": 0.91,
            },
        )
        assert evaluate.status_code == 200
        payload = evaluate.json()["result"]
        assert payload["learning_state"]["student_id"] == "student-001"
        assert payload["learning_state"]["intervention"] == "accelerated_mastery"
        assert payload["runtime_state"] == "educational_autonomic_operational"

        history = client.get("/education/autonomic/history?limit=20")
        assert history.status_code == 200
        body = history.json()
        assert body["runtime_identity"] == "Educational Autonomic Runtime"
        assert len(body["history"]) >= 1


def test_memory_mesh_upsert_student_and_snapshot(monkeypatch):
    async def fake_connect():
        return None

    monkeypatch.setattr(main.federation_runtime, "connect", fake_connect)
    MEMORY_MESH.clear()

    with TestClient(main.app) as client:
        upsert = client.post(
            "/education/memory-mesh/upsert",
            json={
                "student_id": "student-002",
                "discipline": "chemistry",
                "cognition_score": 0.65,
                "consistency": 0.55,
                "engagement": 0.62,
            },
        )
        assert upsert.status_code == 200
        result = upsert.json()["result"]
        assert result["runtime_state"] == "educational_memory_mesh_operational"
        assert result["learning_state"]["student_id"] == "student-002"

        student_history = client.get("/education/memory-mesh/student/student-002?limit=20")
        assert student_history.status_code == 200
        assert len(student_history.json()["history"]) >= 1

        snapshot = client.get("/education/memory-mesh/snapshot?limit=20")
        assert snapshot.status_code == 200
        snapshot_body = snapshot.json()["snapshot"]
        assert snapshot_body["mesh_size"] >= 1
        assert isinstance(snapshot_body["intervention_distribution"], dict)


def test_scientific_knowledge_graph_upsert_link_and_snapshot(monkeypatch):
    async def fake_connect():
        return None

    monkeypatch.setattr(main.federation_runtime, "connect", fake_connect)
    SCIENTIFIC_KNOWLEDGE_NODES.clear()
    SCIENTIFIC_KNOWLEDGE_EDGES.clear()

    with TestClient(main.app) as client:
        upsert_astro = client.post(
            "/education/scientific-knowledge-graph/concepts/upsert",
            json={
                "discipline": "astronomy",
                "concept": "stellar nucleosynthesis",
                "confidence": 0.92,
                "source": "research_paper",
                "tags": ["stars", "chemistry"],
            },
        )
        assert upsert_astro.status_code == 200
        assert upsert_astro.json()["result"]["runtime_state"] == "scientific_knowledge_graph_operational"

        upsert_cosmo = client.post(
            "/education/scientific-knowledge-graph/concepts/upsert",
            json={
                "discipline": "astronomy",
                "concept": "cosmic element formation",
                "confidence": 0.89,
                "source": "simulation",
            },
        )
        assert upsert_cosmo.status_code == 200

        link_response = client.post(
            "/education/scientific-knowledge-graph/relations/link",
            json={
                "discipline": "astronomy",
                "source_concept": "stellar nucleosynthesis",
                "target_concept": "cosmic element formation",
                "relation_type": "supports",
                "weight": 1.5,
            },
        )
        assert link_response.status_code == 200
        relation = link_response.json()["result"]["relation"]
        assert relation["relation_type"] == "supports"
        assert relation["weight"] == 1.5

        concept_response = client.get(
            "/education/scientific-knowledge-graph/concepts/astronomy/stellar nucleosynthesis"
        )
        assert concept_response.status_code == 200
        concept_result = concept_response.json()["result"]
        assert concept_result["node"]["concept"] == "stellar nucleosynthesis"
        assert len(concept_result["outgoing_relations"]) >= 1

        snapshot_response = client.get(
            "/education/scientific-knowledge-graph/snapshot?discipline=astronomy&limit=10"
        )
        assert snapshot_response.status_code == 200
        snapshot = snapshot_response.json()["snapshot"]
        assert snapshot["node_count"] == 2
        assert snapshot["relation_count"] == 1
        assert snapshot["relation_distribution"]["supports"] == 1


def test_pedagogical_reasoning_runtime_reason_and_history(monkeypatch):
    async def fake_connect():
        return None

    monkeypatch.setattr(main.federation_runtime, "connect", fake_connect)
    REASONING_MEMORY.clear()

    with TestClient(main.app) as client:
        reason = client.post(
            "/education/pedagogical-reasoning/reason",
            json={
                "student_id": "student-003",
                "discipline": "mathematics",
                "cognition_score": 0.48,
                "consistency": 0.52,
                "engagement": 0.5,
            },
        )
        assert reason.status_code == 200
        payload = reason.json()["result"]
        assert payload["runtime_state"] == "pedagogical_reasoning_operational"
        assert payload["reasoning_state"]["student_id"] == "student-003"
        assert payload["reasoning_state"]["curriculum_action"] == "rebalance_learning_blocks"

        history = client.get("/education/pedagogical-reasoning/history?limit=20")
        assert history.status_code == 200
        body = history.json()
        assert body["runtime_identity"] == "Pedagogical Reasoning Runtime"
        assert len(body["history"]) >= 1


def test_civilization_education_sync_synchronize_and_history(monkeypatch):
    async def fake_connect():
        return None

    monkeypatch.setattr(main.federation_runtime, "connect", fake_connect)
    CIVILIZATION_SYNC_MEMORY.clear()

    with TestClient(main.app) as client:
        sync = client.post(
            "/education/civilization-sync/synchronize",
            json={
                "federation_id": "federation-01",
                "region": "americas",
                "cognition_sync": 0.83,
                "curriculum_sync": 0.78,
                "intervention_sync": 0.81,
            },
        )
        assert sync.status_code == 200
        result = sync.json()["result"]
        assert result["runtime_state"] == "civilization_education_sync_operational"
        assert result["sync_payload"]["sync_state"] == "civilization_sync_stable"

        history = client.get("/education/civilization-sync/history?limit=20")
        assert history.status_code == 200
        assert history.json()["runtime_identity"] == "Civilization Education Sync"
        assert len(history.json()["history"]) >= 1


def test_federated_learning_identity_generate_and_history(monkeypatch):
    async def fake_connect():
        return None

    monkeypatch.setattr(main.federation_runtime, "connect", fake_connect)
    FEDERATED_IDENTITY_MEMORY.clear()

    with TestClient(main.app) as client:
        generated = client.post(
            "/education/federated-identity/generate",
            json={
                "student_id": "student-004",
                "ecosystem": "academy",
                "discipline": "biology",
                "cognition_score": 0.79,
                "consistency": 0.73,
                "engagement": 0.76,
            },
        )
        assert generated.status_code == 200
        result = generated.json()["result"]
        assert result["runtime_state"] == "federated_learning_identity_operational"
        assert result["identity_payload"]["student_id"] == "student-004"
        assert result["identity_payload"]["federated_identity"]

        history = client.get("/education/federated-identity/history?limit=20")
        assert history.status_code == 200
        body = history.json()
        assert body["runtime_identity"] == "Federated Learning Identity"
        assert len(body["history"]) >= 1


def _can_connect_nats() -> bool:
    async def _probe() -> bool:
        nc = NATS()
        try:
            await nc.connect(servers=[os.environ["NATS_URL"]], connect_timeout=1)
            await nc.drain()
            return True
        except Exception:
            return False

    return asyncio.run(_probe())


@pytest.mark.integration
def test_real_nats_publish_with_compose():
    if not _can_connect_nats():
        pytest.skip("NATS indisponivel em nats://localhost:4222")

    received: queue.Queue[str] = queue.Queue()
    ready = threading.Event()

    def subscriber() -> None:
        async def _run() -> None:
            nc = NATS()
            await nc.connect(servers=[os.environ["NATS_URL"]])

            async def cb(msg):
                received.put(msg.data.decode())

            await nc.subscribe("liceu.academia.course.created", cb=cb)
            await nc.flush()
            ready.set()
            await asyncio.sleep(4)
            await nc.drain()

        asyncio.run(_run())

    thread = threading.Thread(target=subscriber, daemon=True)
    thread.start()

    assert ready.wait(timeout=3)

    with TestClient(main.app) as client:
        token = _get_token(client, role="professor")
        headers = {"Authorization": f"Bearer {token}"}
        response = client.post(
            "/courses",
            headers=headers,
            json={
                "course_id": "NATS-200",
                "title": "Federation Messaging",
                "area": "federation",
                "instructor": "John Professor",
            },
        )
        assert response.status_code == 200

    payload = json.loads(received.get(timeout=5))
    assert payload["course_id"] == "NATS-200"