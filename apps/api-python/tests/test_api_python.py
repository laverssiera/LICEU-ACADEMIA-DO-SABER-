import sys
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).resolve().parents[1]))
from main import app

client = TestClient(app)


def test_root_returns_platform_status():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "platform": "LICEU Academia do Saber",
        "version": "7.0",
        "status": "running",
    }


def test_john_live_teaching_contract():
    payload = {
        "student_id": "USR-001",
        "topic": "Estruturas metalicas",
        "mode": "immersive",
    }

    response = client.post("/john/academy/live-teaching", json=payload)
    data = response.json()

    assert response.status_code == 200
    assert isinstance(data["lesson_id"], str)
    assert data["topic"] == payload["topic"]
    assert data["mode"] == payload["mode"]
    assert data["holographic_scene"] is True
    assert data["simulation_enabled"] is True
    assert data["adaptive_learning"] is True
    assert data["voice_ai"] == "john-ptbr"


def test_holography_start_contract():
    response = client.post("/holography/start")

    assert response.status_code == 200
    assert response.json() == {
        "started": True,
        "engine": "webxr",
        "scene": "classroom_v1",
    }


def test_simulations_start_contract():
    response = client.post("/simulations/start")

    assert response.status_code == 200
    assert response.json() == {
        "started": True,
        "simulation": "structural",
        "status": "queued",
    }


def test_cognitive_behavior_analysis_contract():
    response = client.post("/cefeida/behavior-analysis")

    assert response.status_code == 200
    assert response.json() == {
        "focus_score": 91,
        "learning_velocity": 88,
        "burnout_risk": 12,
        "recommended_mode": "immersive",
    }
