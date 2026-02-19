from __future__ import annotations

from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel

from app.rag.retrieval import search_chunks_semantic
from app.rag.pipeline import rag_answer
from app.storage.files import build_and_store_chunks, extract_text_from_file, save_upload
import logging

router = APIRouter(tags=["api"])

logger = logging.getLogger(__name__)

@router.get("/info")
def info():
    return {
        "service": "cloud-ai-document-search",
        "features": ["upload", "chunking", "semantic search", "RAG answers (kommt bald)"],
    }

@router.get("/health")
def health():
    logger.info("Health is ok")
    return {"status": "ok"}



@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="missing filename")

    allowed = (".txt", ".md")
    if not file.filename.lower().endswith(allowed):
        raise HTTPException(status_code=400, detail="Only .txt and .md supported for now")

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="empty file")

    doc_id, path = save_upload(file.filename, content)
    text = extract_text_from_file(path)

    try:
        result = build_and_store_chunks(doc_id, text)
    except RuntimeError as e:
        # paid API disabled / missing API key
        raise HTTPException(status_code=403, detail=str(e))

    text_stripped = text.strip()
    preview = (text_stripped[:300] + "...") if len(text_stripped) > 300 else text_stripped
    logger.info(
    "File uploaded",
    extra={
        "filename": file.filename,
        "doc_id": doc_id,
        "chunk_count": result["chunk_count"],
    },
)
    return {"doc_id": doc_id, "chunk_count": result["chunk_count"], "preview": preview}


class AskRequest(BaseModel):
    question: str


@router.post("/ask")
def ask(request: AskRequest):
    logger.info("Question asked")
    return rag_answer(request.question)