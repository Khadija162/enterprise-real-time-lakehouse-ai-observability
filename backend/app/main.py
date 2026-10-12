"""Read-only FastAPI control plane for the lakehouse prototype."""
import json
import os
import sqlite3
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from .services.llama import analyze_incident

ROOT = Path(__file__).resolve().parents[2]
DB_FILE = Path(os.getenv("MONITORING_DB", str(ROOT / "monitoring" / "monitoring.db")))
app = FastAPI(title="Lakehouse Control Center", version="0.2.0")


def query_rows(query: str, params: tuple = ()):
    if not DB_FILE.is_file():
        return []
    with sqlite3.connect(f"file:{DB_FILE.as_posix()}?mode=ro", uri=True) as conn:
        conn.row_factory = sqlite3.Row
        return [dict(row) for row in conn.execute(query, params).fetchall()]


@app.get("/api/health")
def health():
    return {"status": "ok", "monitoring_db_present": DB_FILE.is_file()}


@app.get("/api/metrics")
def latest_metrics():
    rows = query_rows(
        "SELECT * FROM monitoring_runs ORDER BY started_at DESC LIMIT 1"
    )
    return {"latest": rows[0] if rows else None}


@app.get("/api/pipelines")
def pipelines():
    return {"pipelines": [{"id": "ecommerce-orders", "name": "E-commerce Orders", "type": "Kafka → Spark → Delta"}]}


@app.get("/api/pipelines/{pipeline_id}/runs")
def pipeline_runs(pipeline_id: str):
    if pipeline_id != "ecommerce-orders":
        raise HTTPException(404, "Unknown pipeline")
    return {"runs": query_rows("SELECT * FROM monitoring_runs ORDER BY started_at DESC LIMIT 50")}


@app.get("/api/alerts")
def alerts():
    return {"alerts": query_rows("SELECT * FROM alerts ORDER BY alert_id DESC LIMIT 100")}


class IncidentRequest(BaseModel):
    run_id: str = Field(min_length=1, max_length=128)


@app.post("/api/ai/analyze")
def ai_analyze(payload: IncidentRequest):
    rows = query_rows(
        "SELECT * FROM monitoring_runs WHERE run_id = ?", (payload.run_id,)
    )
    if not rows:
        raise HTTPException(404, "Monitoring run not found")
    matched_alerts = query_rows(
        "SELECT severity, rule, message FROM alerts WHERE run_id = ?",
        (payload.run_id,)
    )
    evidence = {
        "run_id": payload.run_id,
        "metrics": {key: rows[0].get(key) for key in (
            "bronze_count", "silver_count", "rejected_count",
            "duplicate_count", "rejection_rate", "duplicate_rate",
            "latest_event_at"
        )},
        "alerts": matched_alerts,
    }
    try:
        return analyze_incident(evidence)
    except Exception as exc:
        raise HTTPException(502, "Model inference unavailable") from exc
