import sys
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).resolve().parents[1]))
from main import app

client = TestClient(app)


def test_structural_simulation_contract():
    response = client.post("/simulate/structural")
    data = response.json()

    assert response.status_code == 200
    assert data["simulation"] == "structural"
    assert data["status"] == "completed"
    assert data["risk"] == "low"
    assert 0 <= data["stress_factor"] <= 1
