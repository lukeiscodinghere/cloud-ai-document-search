from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Chunk:
    index: int
    text: str


def chunk_text(text: str, *, max_chars: int = 900, overlap: int = 150) -> list[Chunk]:
    """
    Character - based chunking with overlap.
    - max_chars: max size per chunk
    - overlap: repeated tail from previous chunk to preserve context
    """
    clean = (text or "").strip()
    if not clean:
        return []

    if overlap >= max_chars:
        raise ValueError("overlap must be smaller than max_chars")

    chunks: list[Chunk] = []
    start = 0
    idx = 0

    while start < len(clean):
        end = min(start + max_chars, len(clean))
        chunk = clean[start:end].strip()
        if chunk:
            chunks.append(Chunk(index=idx, text=chunk))
            idx += 1

        if end >= len(clean):
            break

        start = max(0, end - overlap)

    return chunks
