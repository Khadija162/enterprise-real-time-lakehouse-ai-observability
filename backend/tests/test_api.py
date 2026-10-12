import sqlite3
from fastapi.testclient import TestClient
from backend.app import main


def test_health_without_database(tmp_path, monkeypatch):
    monkeypatch.setattr(main, "DB_FILE", tmp_path / "missing.db")
    client = TestClient(main.app)
    assert client.get("/api/health").json()["status"] == "ok"
    assert client.get("/api/alerts").json() == {"alerts": []}
    assert client.get("/api/metrics").json() == {"latest": None}


def test_ai_mock():
    from backend.app.services.llama import analyze_incident
    result = analyze_incident({"metrics": {"rejection_rate": 12}, "alerts": [{"rule": "HIGH_REJECTION_RATE"}]})
    assert result["mode"] == "mock"
    assert result["human_approval_required"] is True


def test_unknown_pipeline():
    client = TestClient(main.app)
    assert client.get("/api/pipelines/unknown/runs").status_code == 404
