import os
import sys
import tempfile
from pathlib import Path

from fastapi.testclient import TestClient

db_file = Path(tempfile.gettempdir()) / "academia_cognition_test.db"
if db_file.exists():
    db_file.unlink()
os.environ["ACADEMIA_COGNITION_DB_PATH"] = str(db_file)

sys.path.append(str(Path(__file__).resolve().parents[1]))
from main import app

client = TestClient(app)


def test_root_runtime_status_contract():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "runtime": "Academia do Saber",
        "module": "Educational Cognition",
        "status": "running",
    }


def test_educational_cognition_contract():
    payload = {
        "student_id": "STU-42",
        "subject": "matematica",
        "event": "weekly-evaluation",
        "skill_signals": {
            "algebra": 0.83,
            "geometria": 0.74,
        },
        "progression_score": 0.82,
        "retention_score": 0.79,
        "current_stage": "intermediate",
        "target_stage": "advanced",
        "next_cycle_hours": 12,
    }

    response = client.post("/education/educational-cognition", json=payload)
    data = response.json()

    assert response.status_code == 200
    assert data["runtime_identity"] == "Educational Cognition Runtime"
    assert data["learning_memory"]["student_id"] == "STU-42"
    assert data["learning_memory"]["subject"] == "matematica"
    assert data["cognitive_progression"]["progression_score"] == 0.82
    assert data["knowledge_retention"]["retention_score"] == 0.79
    assert data["skill_mapping"]["skills"]["algebra"] == 0.83
    assert data["learning_trajectory"]["target_stage"] == "advanced"
    assert data["educational_analytics"]["events_in_memory"] >= 1
    assert data["educational_analytics"]["federated_educational_intelligence"] is True
    assert data["educational_analytics"]["sovereign_pedagogy_intelligence"] == "enabled"


def test_educational_cognition_history_contract():
    payload_a = {
        "student_id": "STU-HISTORY",
        "subject": "matematica",
        "event": "checkpoint-a",
        "progression_score": 0.78,
        "retention_score": 0.73,
    }
    payload_b = {
        "student_id": "STU-HISTORY",
        "subject": "matematica",
        "event": "checkpoint-b",
        "progression_score": 0.84,
        "retention_score": 0.81,
    }

    post_a = client.post("/education/educational-cognition", json=payload_a)
    post_b = client.post("/education/educational-cognition", json=payload_b)

    assert post_a.status_code == 200
    assert post_b.status_code == 200

    response = client.get(
        "/education/educational-cognition/history",
        params={"student_id": "STU-HISTORY", "subject": "matematica", "limit": 2},
    )
    data = response.json()

    assert response.status_code == 200
    assert data["runtime_identity"] == "Educational Cognition Runtime"
    assert data["filters"]["student_id"] == "STU-HISTORY"
    assert data["filters"]["subject"] == "matematica"
    assert data["filters"]["limit"] == 2
    assert data["total_returned"] == 2
    assert len(data["records"]) == 2
    assert data["records"][0]["event"] == "checkpoint-b"
    assert data["records"][1]["event"] == "checkpoint-a"


def test_educational_cognition_analytics_contract():
    payloads = [
        {
            "student_id": "STU-ANALYTICS",
            "subject": "fisica",
            "event": "analytics-1",
            "progression_score": 0.7,
            "retention_score": 0.69,
        },
        {
            "student_id": "STU-ANALYTICS",
            "subject": "fisica",
            "event": "analytics-2",
            "progression_score": 0.75,
            "retention_score": 0.74,
        },
        {
            "student_id": "STU-ANALYTICS",
            "subject": "fisica",
            "event": "analytics-3",
            "progression_score": 0.8,
            "retention_score": 0.78,
        },
    ]

    for payload in payloads:
        posted = client.post("/education/educational-cognition", json=payload)
        assert posted.status_code == 200

    response = client.get(
        "/education/educational-cognition/analytics",
        params={"student_id": "STU-ANALYTICS", "subject": "fisica", "limit": 3},
    )
    data = response.json()

    assert response.status_code == 200
    assert data["runtime_identity"] == "Educational Cognition Runtime"
    assert data["filters"]["student_id"] == "STU-ANALYTICS"
    assert data["filters"]["subject"] == "fisica"
    assert data["filters"]["limit"] == 3
    assert data["analytics"]["sample_size"] == 3
    assert data["analytics"]["avg_progression_score"] == 0.75
    assert data["analytics"]["avg_retention_score"] == 0.7367
    assert data["analytics"]["progression_trend"] == "ascending"
    assert data["analytics"]["retention_trend"] == "ascending"
    assert data["analytics"]["window"]["from"] is not None
    assert data["analytics"]["window"]["to"] is not None


def test_educational_cognition_federated_analytics_contract():
    subject_payloads = [
        {
            "student_id": "FED-1",
            "subject": "astro-federada",
            "event": "fed-astro-1",
            "progression_score": 0.92,
            "retention_score": 0.9,
        },
        {
            "student_id": "FED-2",
            "subject": "astro-federada",
            "event": "fed-astro-2",
            "progression_score": 0.9,
            "retention_score": 0.88,
        },
        {
            "student_id": "FED-3",
            "subject": "quimica-federada",
            "event": "fed-quimica-1",
            "progression_score": 0.7,
            "retention_score": 0.72,
        },
        {
            "student_id": "FED-4",
            "subject": "quimica-federada",
            "event": "fed-quimica-2",
            "progression_score": 0.73,
            "retention_score": 0.71,
        },
    ]

    for payload in subject_payloads:
        posted = client.post("/education/educational-cognition", json=payload)
        assert posted.status_code == 200

    response = client.get(
        "/education/educational-cognition/federated-analytics",
        params={"limit": 5, "min_events": 2},
    )
    data = response.json()

    assert response.status_code == 200
    assert data["runtime_identity"] == "Educational Cognition Runtime"
    assert data["federated_intelligence"] == "enabled"
    assert data["filters"]["limit"] == 5
    assert data["filters"]["min_events"] == 2
    assert data["analytics"]["subjects_ranked"] >= 2
    assert data["analytics"]["min_events"] == 2
    assert len(data["analytics"]["rankings"]) >= 2
    assert data["analytics"]["rankings"][0]["subject"] == "astro-federada"
    assert data["analytics"]["rankings"][0]["rank"] == 1


def test_educational_evolution_longitudinal_contract():
    payloads = [
        {
            "student_id": "STU-EVO-1",
            "subject": "biologia-evolutiva",
            "event": "evo-cycle-1",
            "progression_score": 0.81,
            "retention_score": 0.8,
        },
        {
            "student_id": "STU-EVO-1",
            "subject": "biologia-evolutiva",
            "event": "evo-cycle-2",
            "progression_score": 0.75,
            "retention_score": 0.74,
        },
        {
            "student_id": "STU-EVO-1",
            "subject": "biologia-evolutiva",
            "event": "evo-cycle-3",
            "progression_score": 0.7,
            "retention_score": 0.69,
        },
    ]

    for payload in payloads:
        posted = client.post("/education/educational-cognition", json=payload)
        assert posted.status_code == 200

    response = client.get(
        "/education/educational-evolution",
        params={"student_id": "STU-EVO-1", "subject": "biologia-evolutiva", "limit": 10},
    )
    data = response.json()

    assert response.status_code == 200
    assert data["runtime_identity"] == "Educational Evolution Runtime"
    assert data["filters"]["student_id"] == "STU-EVO-1"
    assert data["evolution"]["sample_size"] == 3
    assert data["evolution"]["cognitive_evolution"]["trend"] == "descending"
    assert data["evolution"]["regression_detection"]["risk_level"] in {"medium", "high"}
    assert data["evolution"]["mastery_prediction"]["mastery_target"] == 0.9
    assert data["evolution"]["temporal_educational_memory"]["events"] == 3
    assert data["evolution"]["sovereign_learning_analytics"]["federated_evolution_ready"] is True


def test_educational_evolution_federated_analytics_contract():
    payloads = [
        {
            "student_id": "FED-EVO-1",
            "subject": "engenharia-civil",
            "event": "fed-evo-eng-1",
            "progression_score": 0.88,
            "retention_score": 0.86,
        },
        {
            "student_id": "FED-EVO-2",
            "subject": "engenharia-civil",
            "event": "fed-evo-eng-2",
            "progression_score": 0.9,
            "retention_score": 0.89,
        },
        {
            "student_id": "FED-EVO-3",
            "subject": "engenharia-civil",
            "event": "fed-evo-eng-3",
            "progression_score": 0.92,
            "retention_score": 0.9,
        },
        {
            "student_id": "FED-EVO-4",
            "subject": "historia-global",
            "event": "fed-evo-his-1",
            "progression_score": 0.65,
            "retention_score": 0.66,
        },
        {
            "student_id": "FED-EVO-5",
            "subject": "historia-global",
            "event": "fed-evo-his-2",
            "progression_score": 0.67,
            "retention_score": 0.68,
        },
        {
            "student_id": "FED-EVO-6",
            "subject": "historia-global",
            "event": "fed-evo-his-3",
            "progression_score": 0.69,
            "retention_score": 0.7,
        },
    ]

    for payload in payloads:
        posted = client.post("/education/educational-cognition", json=payload)
        assert posted.status_code == 200

    response = client.get(
        "/education/educational-evolution/federated-analytics",
        params={"limit": 10, "min_events": 3},
    )
    data = response.json()

    assert response.status_code == 200
    assert data["runtime_identity"] == "Educational Evolution Runtime"
    assert data["filters"]["limit"] == 10
    assert data["filters"]["min_events"] == 3
    assert data["analytics"]["subjects_ranked"] >= 2
    assert data["analytics"]["sovereign_educational_continuity"] is True
    assert data["analytics"]["rankings"][0]["subject"] == "engenharia-civil"
    assert data["analytics"]["rankings"][0]["rank"] == 1


def test_civilization_brain_sync_contract():
    payloads = [
        {
            "student_id": "BRAIN-1",
            "subject": "sistemas-distribuidos",
            "event": "brain-sync-1",
            "progression_score": 0.86,
            "retention_score": 0.82,
        },
        {
            "student_id": "BRAIN-2",
            "subject": "sistemas-distribuidos",
            "event": "brain-sync-2",
            "progression_score": 0.88,
            "retention_score": 0.84,
        },
        {
            "student_id": "BRAIN-3",
            "subject": "ciencia-cognitiva",
            "event": "brain-sync-3",
            "progression_score": 0.8,
            "retention_score": 0.79,
        },
    ]

    for payload in payloads:
        posted = client.post("/education/educational-cognition", json=payload)
        assert posted.status_code == 200

    response = client.post("/education/civilization-brain/sync", json={"limit": 5})
    data = response.json()

    assert response.status_code == 200
    assert data["runtime_identity"] == "Civilization Brain Runtime"
    assert data["education_to_civilization_brain"] == "synchronized"
    assert data["learning_signals_federation"]["total_signals"] >= 2
    assert data["global_knowledge_state"]["events"] >= 3
    assert data["global_knowledge_state"]["subjects"] >= 2
    assert data["collective_educational_intelligence"]["status"] == "active"
    assert data["civilization_memory_sync"]["shared_memory"] is True
    assert data["civilization_learning_intelligence"]["sovereign"] is True


def test_civilization_brain_state_and_history_contract():
    state_response = client.get("/education/civilization-brain/state", params={"limit": 5})
    state_data = state_response.json()

    assert state_response.status_code == 200
    assert state_data["runtime_identity"] == "Civilization Brain Runtime"
    assert state_data["global_knowledge_state"]["events"] >= 1
    assert state_data["collective_educational_intelligence"]["score"] >= 0

    history_response = client.get("/education/civilization-brain/sync-history", params={"limit": 3})
    history_data = history_response.json()

    assert history_response.status_code == 200
    assert history_data["runtime_identity"] == "Civilization Brain Runtime"
    assert history_data["total_returned"] >= 1
    assert len(history_data["records"]) >= 1
    assert history_data["records"][0]["global_events"] >= 1
