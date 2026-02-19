from __future__ import annotations

import json
import os
import uuid
from pathlib import Path

from app.rag.chunking import Chunk, chunk_text

DATA_DIR = Path("data")
UPLOADS_DIR = DATA_DIR / "uploads"
CHUNKS_DIR = DATA_DIR / "chunks"


def ensure_data_dirs() -> None:
    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
    CHUNKS_DIR.mkdir(parents=True, exist_ok=True)


def save_upload(filename: str, content: bytes) -> tuple[str, Path]:
    ensure_data_dirs()
    doc_id = str(uuid.uuid4())
    safe_name = Path(filename).name  # strips any path
    target = UPLOADS_DIR / f"{doc_id}__{safe_name}"
    target.write_bytes(content)
    return doc_id, target


def extract_text_from_file(path: Path) -> str:
    # einfach nur für gerade: only treat as plain text. (PDF support später)
    return path.read_text(encoding="utf-8", errors="ignore")


def build_and_store_chunks(doc_id: str, text: str) -> dict:
    ensure_data_dirs()
    chunks = chunk_text(text)

    from app.rag.embeddings import embed_texts
    vectors = embed_texts([c.text for c in chunks]) if chunks else []

    payload = {
        "doc_id": doc_id,
        "chunk_count": len(chunks),
        "chunks": [
            {"index": c.index, "text": c.text, "embedding": vectors[i]}
            for i, c in enumerate(chunks)
        ],
    }

    (CHUNKS_DIR / f"{doc_id}.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return payload

