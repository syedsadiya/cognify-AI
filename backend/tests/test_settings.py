def test_default_settings(client):
    body = client.get("/api/settings").json()
    assert body["default_engine"] == "auto"
    assert body["repetitions"] == "5"


def test_update_setting(client):
    r = client.put("/api/settings", json={"key": "default_engine", "value": "polars"})
    assert r.status_code == 200
    assert client.get("/api/settings").json()["default_engine"] == "polars"


def test_unknown_key_rejected(client):
    r = client.put("/api/settings", json={"key": "hack", "value": "x"})
    assert r.status_code == 400


def test_invalid_value_rejected(client):
    r = client.put("/api/settings", json={"key": "repetitions", "value": "999"})
    assert r.status_code == 400
