# cloud-ai-document-search
**Idee:**
### Struktur:
Client → FastAPI → Retrieval → Chunk Storage

- theoretisch könnte es dann auch andocken an:
FastAPI → Vector DB → OpenAI → Respons
[kostet aber Geld, da OpenAI API calls nötig wären]



### Lokale Kurzbefehle und wichtige Links:
Start the server:
uvicorn app.main:app --reload


User Interface (Lokal):

http://127.0.0.1:8000/ (UI)

http://127.0.0.1:8000/docs (Swagger)

http://127.0.0.1:8000/health (Health)