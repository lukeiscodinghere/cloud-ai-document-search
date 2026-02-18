from __future__ import annotations

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.storage.files import build_and_store_chunks, extract_text_from_file, save_upload

router = APIRouter(tags=["api"])


@router.get("/info")
def info():
    return {
        "service": "cloud-ai-document-search",
        "features": ["upload", "chunking", "semantic search (kommt bald)", "RAG answers (kommt bald)"],
    }


@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="missing filename")

    # for now: accept .txt/.md 
    allowed = (".txt", ".md")
    if not file.filename.lower().endswith(allowed):
        raise HTTPException(status_code=400, detail="Only .txt and .md supported for now")

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="empty file")

    doc_id, path = save_upload(file.filename, content)
    text = extract_text_from_file(path)
    result = build_and_store_chunks(doc_id, text)

    text_stripped = text.strip()
    preview = (text.strip()[:300] + "...") if len(text.strip()) > 300 else text.strip()
    return {"doc_id": doc_id, "chunk_count": result["chunk_count"], "preview": preview}
