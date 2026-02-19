from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

CHUNKS_DIR = Path("data/chunks")


def _load_all_chunks() -> List[Dict]:
    all_chunks: List[Dict] = []
    if not CHUNKS_DIR.exists():
        return all_chunks

    for file in CHUNKS_DIR.glob("*.json"):
        payload = json.loads(file.read_text(encoding="utf-8"))
        doc_id = payload.get("doc_id")
        for chunk in payload.get("chunks", []):
            all_chunks.append(
                {
                    "doc_id": doc_id,
                    "chunk_index": chunk.get("index"),
                    "text": chunk.get("text", ""),
                }
            )
    return all_chunks


def search_chunks_semantic(query: str, top_k: int = 3) -> List[Dict]:
    chunks = _load_all_chunks()
    if not chunks:
        return []

    texts = [c["text"] for c in chunks]

    
    vectorizer = TfidfVectorizer(stop_words="english")
    X = vectorizer.fit_transform(texts)          # (n_chunks, n_features)
    q = vectorizer.transform([query])            # (1, n_features)

    sims = cosine_similarity(q, X)[0]            # (n_chunks,)

    # top_k indices
    top_idx = np.argsort(-sims)[:top_k]

    results: List[Dict] = []
    for i in top_idx:
        score = float(sims[i])
        if score <= 0:
            continue
        c = chunks[int(i)]
        results.append({**c, "score": score})

    return results
