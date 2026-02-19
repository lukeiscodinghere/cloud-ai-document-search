from __future__ import annotations

from app.rag.retrieval import search_chunks_semantic
from app.rag.generator import generate_answer


def rag_answer(question: str):
    chunks = search_chunks_semantic(question)
    answer = generate_answer(question, chunks)

    return {
        "question": question,
        "answer": answer,
        "sources": chunks
    }
