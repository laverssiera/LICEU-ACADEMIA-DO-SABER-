import asyncio
import json
import os
import queue
import threading
from pathlib import Path
import sys

import pytest
from fastapi.testclient import TestClient
from nats.aio.client import Client as NATS

sys.path.append(str(Path(__file__).resolve().parents[1]))

os.environ.setdefault("GRAPH_URI", "bolt://localhost:7687")
os.environ.setdefault("GRAPH_USER", "neo4j")
os.environ.setdefault("GRAPH_PASSWORD", "liceu")
os.environ.setdefault("NATS_URL", "nats://localhost:4222")

import main


def _get_token(client: TestClient, role: str = "professor") -> str:
    response = client.post(
        "/auth/token",
        json={"subject": "e2e-user", "role": role, "expires_minutes": 60},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


def _can_connect_nats() -> bool:
    async def _probe() -> bool:
        nc = NATS()
        try:
            await nc.connect(servers=[os.getenv("NATS_URL", "nats://localhost:4222")], connect_timeout=1)
            await nc.drain()
            return True
        except Exception:
            return False

    return asyncio.run(_probe())


@pytest.mark.integration
def test_federation_chain_with_persistent_consumer() -> None:
    if not _can_connect_nats():
        pytest.skip("NATS indisponivel em nats://localhost:4222")

    received: queue.Queue[dict] = queue.Queue()
    ready = threading.Event()

    def subscriber() -> None:
        async def _run() -> None:
            nc = NATS()
            await nc.connect(servers=[os.getenv("NATS_URL", "nats://localhost:4222")])

            async def cb(msg):
                received.put(
                    {
                        "subject": msg.subject,
                        "payload": json.loads(msg.data.decode()),
                    }
                )

            await nc.subscribe("liceu.academia.course.created", queue="e2e-consumer", cb=cb)
            await nc.subscribe("liceu.academia.john.training", queue="e2e-consumer", cb=cb)
            await nc.flush()
            ready.set()
            await asyncio.sleep(5)
            await nc.drain()

        asyncio.run(_run())

    consumer = threading.Thread(target=subscriber, daemon=True)
    consumer.start()
    assert ready.wait(timeout=3)

    with TestClient(main.app) as client:
        token = _get_token(client, role="professor")
        headers = {"Authorization": f"Bearer {token}"}

        course_response = client.post(
            "/courses",
            headers=headers,
            json={
                "course_id": "E2E-101",
                "title": "Federated Runtime",
                "area": "collective",
                "instructor": "John Professor",
            },
        )
        assert course_response.status_code == 200

        mentor_response = client.post("/agents/john/mentor", headers=headers)
        assert mentor_response.status_code == 200

    first = received.get(timeout=5)
    second = received.get(timeout=5)
    subjects = {first["subject"], second["subject"]}
    assert "liceu.academia.course.created" in subjects
    assert "liceu.academia.john.training" in subjects