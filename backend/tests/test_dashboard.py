def test_dashboard_empty(client):
    r = client.get("/api/dashboard/summary")
    assert r.status_code == 200
    body = r.json()
    assert body["total_datasets"] == 0
    assert body["total_benchmark_runs"] == 0
    assert body["recent_runs"] == []
    assert "pandas" in body["available_engines"]


def test_lists_empty(client):
    assert client.get("/api/datasets").json() == []
    assert client.get("/api/benchmarks/history").json() == []
