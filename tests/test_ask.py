from fastapi.testclient import TestClient
from app.main import app
import json
from pathlib import Path

client = TestClient(app)


def test_ask_returns_results(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    # create fake chunk file
    chunks_dir = Path("data/chunks")
    chunks_dir.mkdir(parents=True)

    payload = {
        "doc_id": "test-doc",
        "chunks": [
            {"index": 0, "text": "Retrieval Augmented Generation is powerful."},
            {"index": 1, "text": "Completely unrelated sentence."}
        ]
    }

    (chunks_dir / "test.json").write_text(json.dumps(payload))

    response = client.post("/api/ask", json={"question": "What is Retrieval?"})

    assert response.status_code == 200
    data = response.json()
    assert len(data["results"]) >= 1
