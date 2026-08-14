import sys
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).resolve().parents[1]))
from main import app

client = TestClient(app)


def test_adaptive_learning_contract():
    response = client.post("/adaptive-learning")
    data = response.json()

    assert response.status_code == 200
    assert data["recommended_content"] == [
        "bim-advanced",
        "lean-construction",
        "structural-ai",
    ]
    assert 70 <= data["focus_probability"] <= 99
