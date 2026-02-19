from __future__ import annotations
from typing import List

from app.core.config import settings

def embed_texts(texts: List[str]) -> List[List[float]]:
    if settings.embeddings_provider == "openai":
        if not settings.allow_paid_api:
            raise RuntimeError("Paid API disabled (set APP_ALLOW_PAID_API=true to enable).")
        return _embed_openai(texts)

    return _embed_local_tfidf(texts)

def _embed_local_tfidf(texts: List[str]) -> List[List[float]]:
    # Fits a vectorizer on the fly for demo purposes.
    # (Later we can persist a vectorizer per corpus.)
    from sklearn.feature_extraction.text import TfidfVectorizer

    v = TfidfVectorizer(stop_words="english")
    mat = v.fit_transform(texts).toarray()
    return mat.tolist()

def _embed_openai(texts: List[str]) -> List[List[float]]:
    import os
    from openai import OpenAI

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set")

    client = OpenAI(api_key=api_key)
    resp = client.embeddings.create(model="text-embedding-3-small", input=texts)
    data_sorted = sorted(resp.data, key=lambda x: x.index)
    return [d.embedding for d in data_sorted]
