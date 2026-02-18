from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_upload_txt_success(tmp_path, monkeypatch):
    # test: in temp working dir so we don't pollute repo data/
    monkeypatch.chdir(tmp_path)

    content = b"Hello world.\n" * 200
    files = {"file": ("example.txt", content, "text/plain")}
    r = client.post("/api/upload", files=files)

    assert r.status_code == 200
    data = r.json()
    assert "doc_id" in data
    assert data["chunk_count"] >= 1
    assert "preview" in data


def test_upload_rejects_non_txt():
    files = {"file": ("example.pdf", b"%PDF-1.4", "application/pdf")}
    r = client.post("/api/upload", files=files)
    assert r.status_code == 400
