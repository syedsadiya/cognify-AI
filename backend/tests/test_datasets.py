import io
import pandas as pd
import pytest
from app.core.config import settings
from app.services import dataset_service

CSV = b"id,name,score\n1,a,10\n2,b,\n2,b,\n3,c,30\n"


@pytest.fixture(autouse=True)
def tmp_upload(tmp_path, monkeypatch):
    monkeypatch.setattr(dataset_service, "upload_dir", lambda: tmp_path)
    return tmp_path


def upload(client, name, content):
    return client.post(
        "/api/datasets/upload", files={"file": (name, content, "application/octet-stream")}
    )


def test_upload_csv(client, tmp_upload):
    r = upload(client, "data.csv", CSV)
    assert r.status_code == 201
    body = r.json()
    assert body["row_count"] == 4
    assert body["column_count"] == 3
    assert "stored_name" not in body
    files = list(tmp_upload.iterdir())
    assert len(files) == 1
    assert files[0].name != "data.csv"  # safe server-side name


def test_path_in_filename_is_removed(client):
    r = upload(client, "../../evil.csv", CSV)
    assert r.status_code == 201
    assert r.json()["original_name"] == "evil.csv"


def test_unsupported_type(client, tmp_upload):
    r = upload(client, "notes.txt", b"hello")
    assert r.status_code == 400
    assert list(tmp_upload.iterdir()) == []


def test_empty_file(client):
    assert upload(client, "empty.csv", b"").status_code == 400


def test_header_only_csv(client, tmp_upload):
    r = upload(client, "header.csv", b"a,b,c\n")
    assert r.status_code == 400
    assert list(tmp_upload.iterdir()) == []


def test_invalid_excel(client, tmp_upload):
    r = upload(client, "fake.xlsx", b"this is not an excel file")
    assert r.status_code == 400
    assert list(tmp_upload.iterdir()) == []


def test_file_too_large(client, tmp_upload, monkeypatch):
    monkeypatch.setattr(settings, "max_upload_mb", 0)
    r = upload(client, "data.csv", CSV)
    assert r.status_code == 413
    assert list(tmp_upload.iterdir()) == []


def test_parquet_and_excel(client):
    df = pd.DataFrame({"x": [1, 2, 3], "y": ["a", "b", "c"]})

    buf = io.BytesIO()
    df.to_parquet(buf)
    assert upload(client, "d.parquet", buf.getvalue()).json()["row_count"] == 3

    buf = io.BytesIO()
    df.to_excel(buf, index=False)
    assert upload(client, "d.xlsx", buf.getvalue()).json()["row_count"] == 3


def test_preview(client):
    ds_id = upload(client, "data.csv", CSV).json()["id"]
    body = client.get("/api/datasets/%d/preview?rows=2" % ds_id).json()
    assert body["columns"] == ["id", "name", "score"]
    assert len(body["rows"]) == 2
    assert body["total_rows"] == 4
    assert body["rows"][1][2] is None  # missing score


def test_profile(client):
    ds_id = upload(client, "data.csv", CSV).json()["id"]
    body = client.get("/api/datasets/%d/profile" % ds_id).json()
    assert body["total_missing"] == 2
    assert body["duplicate_rows"] == 1
    assert body["columns"][2]["dtype"] == "float64"
    assert "score" in body["statistics"]


def test_download(client):
    ds_id = upload(client, "data.csv", CSV).json()["id"]
    r = client.get("/api/datasets/%d/download" % ds_id)
    assert r.status_code == 200
    assert r.content == CSV


def test_delete(client, tmp_upload):
    ds_id = upload(client, "data.csv", CSV).json()["id"]
    assert client.delete("/api/datasets/%d" % ds_id).status_code == 204
    assert list(tmp_upload.iterdir()) == []
    assert client.get("/api/datasets/%d" % ds_id).status_code == 404


def test_not_found(client):
    assert client.get("/api/datasets/999").status_code == 404
    assert client.get("/api/datasets/999/preview").status_code == 404
