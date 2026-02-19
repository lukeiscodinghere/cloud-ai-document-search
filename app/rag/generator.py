from __future__ import annotations
from typing import List, Dict


def generate_answer(question: str, contexts: List[Dict]) -> str:
    """
    Lokaler Fallback Generator.
    Synthesizes an answer based purely on retrieved context.
    """

    if not contexts:
        return "No relevant information found in the indexed documents."

    context_text = "\n\n".join(c["text"] for c in contexts)

    return (
        f"Question: {question}\n\n"
        f"Based on the indexed documents:\n\n"
        f"{context_text}"
    )
