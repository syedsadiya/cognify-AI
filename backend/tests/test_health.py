from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_ok():
    r = client.get("/api/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    names = [e["name"] for e in body["engines"]]
    assert names == ["pandas", "polars", "duckdb", "fireducks"]
