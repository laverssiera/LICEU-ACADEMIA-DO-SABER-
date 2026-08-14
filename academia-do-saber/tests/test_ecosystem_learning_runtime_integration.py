from pathlib import Path
import importlib
import os
import sys

from fastapi.testclient import TestClient


sys.path.append(str(Path(__file__).resolve().parents[1]))


def _load_runtime_module(monkeypatch):
    monkeypatch.setenv("AUTH_ENABLED", "true")
    monkeypatch.setenv("JWT_SECRET", "test-secret")
    monkeypatch.setenv("JWT_ALGORITHM", "HS256")
    monkeypatch.setenv("NEO4J_URI", "")
    monkeypatch.setenv("NEO4J_PASSWORD", "")

    if "ecosystem_learning_runtime" in sys.modules:
        module = importlib.reload(sys.modules["ecosystem_learning_runtime"])
    else:
        module = importlib.import_module("ecosystem_learning_runtime")
    return module


def _get_token(client: TestClient) -> str:
    response = client.post(
        "/auth/token",
        json={"subject": "integration-user", "role": "professor", "expires_minutes": 60},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


def test_health_is_public(monkeypatch):
    runtime = _load_runtime_module(monkeypatch)
    with TestClient(runtime.app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        payload = response.json()
        assert payload["status"] == "ok"
        assert payload["chroma_ready"] is True


def test_protected_memory_requires_bearer(monkeypatch):
    runtime = _load_runtime_module(monkeypatch)
    with TestClient(runtime.app) as client:
        response = client.post("/memory/query", json={"query": "orbital", "limit": 1})
        assert response.status_code == 401


def test_memory_roundtrip_with_token(monkeypatch):
    runtime = _load_runtime_module(monkeypatch)
    with TestClient(runtime.app) as client:
        token = _get_token(client)
        headers = {"Authorization": f"Bearer {token}"}

        upsert = client.post(
            "/memory/upsert",
            headers=headers,
            json={
                "memory_id": "test-memory-1",
                "content": "Curriculo de engenharia interplanetaria",
                "metadata": {"track": "space-engineering"},
            },
        )
        assert upsert.status_code == 200

        query = client.post(
            "/memory/query",
            headers=headers,
            json={"query": "interplanetaria", "limit": 1},
        )
        assert query.status_code == 200
        assert isinstance(query.json().get("matches"), list)


def test_learn_compose_requires_auth_and_returns_messages(monkeypatch):
    runtime = _load_runtime_module(monkeypatch)
    with TestClient(runtime.app) as client:
        unauthorized = client.post(
            "/learn/compose",
            json={"topic": "astrofisica", "goal": "resumo", "context": "base"},
        )
        assert unauthorized.status_code == 401

        token = _get_token(client)
        headers = {"Authorization": f"Bearer {token}"}
        authorized = client.post(
            "/learn/compose",
            headers=headers,
            json={"topic": "astrofisica", "goal": "resumo", "context": "base"},
        )
        assert authorized.status_code == 200
        data = authorized.json()
        assert isinstance(data.get("messages"), list)
        assert len(data["messages"]) >= 2
