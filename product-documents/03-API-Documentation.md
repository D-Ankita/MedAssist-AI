# API Documentation

## MedAssist AI - REST API Reference

---

### Base URLs

| Service | URL | Description |
|---------|-----|-------------|
| AI Service (FastAPI) | `http://localhost:8000` | Direct access to AI service |
| API Gateway (NestJS) | `http://localhost:3001/api` | Proxied access via gateway |

---

### 1. Health Check

Check if the AI service is running and return index statistics.

**Endpoint:** `GET /health`
**Gateway:** `GET /api/health`

#### Response

```json
{
  "status": "healthy",
  "service": "MedAssist AI",
  "documents_indexed": 40
}
```

| Field | Type | Description |
|-------|------|-------------|
| status | string | Service health status |
| service | string | Service name |
| documents_indexed | integer | Number of document chunks in ChromaDB |

#### Error Response (503)

```json
{
  "detail": "Service not initialized"
}
```

---

### 2. Query

Process a user's health question through the MedAssist agent pipeline.

**Endpoint:** `POST /query`
**Gateway:** `POST /api/query`
**Content-Type:** `application/json`

#### Request Body

```json
{
  "question": "What are the symptoms of Type 2 diabetes?",
  "chat_history": [
    {
      "role": "user",
      "content": "Tell me about diabetes"
    },
    {
      "role": "assistant",
      "content": "Diabetes is a chronic metabolic disease..."
    }
  ]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| question | string | Yes | The user's health question |
| chat_history | array | No | Previous conversation messages for context |
| chat_history[].role | string | Yes | `"user"` or `"assistant"` |
| chat_history[].content | string | Yes | Message content |

#### Response - ANSWER Intent

```json
{
  "intent": "ANSWER",
  "answer": "According to the Diabetes Overview guide, common symptoms of Type 2 diabetes include increased thirst and frequent urination, unexplained weight loss, extreme fatigue, blurred vision, and slow-healing sores. Type 2 symptoms often develop slowly over years and may go unnoticed.\n\nThis information is for educational purposes only and is not a substitute for professional medical advice.",
  "sources": [
    {
      "document": "Diabetes-Overview.pdf",
      "page": 1,
      "relevance": 0.8732
    },
    {
      "document": "Diabetes-Overview.pdf",
      "page": 2,
      "relevance": 0.7451
    }
  ],
  "chunks_retrieved": 5,
  "relevance_scores": [0.8732, 0.7451, 0.6890, 0.6234, 0.5891]
}
```

#### Response - CLARIFY Intent

```json
{
  "intent": "CLARIFY",
  "answer": "Could you clarify — are you asking about Type 1 diabetes, Type 2 diabetes, or gestational diabetes? This will help me find the most relevant information.",
  "sources": [],
  "chunks_retrieved": 0,
  "relevance_scores": []
}
```

#### Response - ESCALATE Intent

```json
{
  "intent": "ESCALATE",
  "answer": "⚠️ **This sounds like it could be a medical emergency.**\n\nPlease take immediate action:\n- **Call emergency services:** 911 (US), 999 (UK), 112 (EU)\n- Go to your nearest emergency room\n- If someone is with you, ask them to help while you call\n\nDo not wait — getting professional help quickly is critical.",
  "sources": [],
  "chunks_retrieved": 0,
  "relevance_scores": []
}
```

| Field | Type | Description |
|-------|------|-------------|
| intent | string | Agent decision: `ANSWER`, `CLARIFY`, or `ESCALATE` |
| answer | string | The generated response (may contain markdown) |
| sources | array | Cited source documents |
| sources[].document | string | Source PDF filename |
| sources[].page | integer | Page number (1-indexed) |
| sources[].relevance | float | Cosine similarity score (0-1) |
| chunks_retrieved | integer | Number of chunks retrieved from vector store |
| relevance_scores | array[float] | Relevance scores for all retrieved chunks |

#### Error Responses

| Status | Description |
|--------|-------------|
| 400 | `{"detail": "Question cannot be empty"}` |
| 500 | `{"detail": "Error processing query: ..."}` |
| 503 | `{"detail": "Service not initialized"}` |

---

### 3. Ingest Documents

Trigger ingestion of all PDF files in the `knowledge_base/` directory.

**Endpoint:** `POST /ingest`
**Gateway:** `POST /api/ingest`

#### Request

No request body required.

#### Response

```json
{
  "status": "success",
  "message": "Documents ingested successfully",
  "files_processed": 5,
  "total_pages": 15,
  "total_chunks": 40
}
```

| Field | Type | Description |
|-------|------|-------------|
| status | string | `"success"` or `"error"` |
| message | string | Human-readable status message |
| files_processed | integer | Number of PDF files ingested |
| total_pages | integer | Total pages extracted |
| total_chunks | integer | Total chunks stored in ChromaDB |

---

### 4. Upload Document

Upload a single PDF file and ingest it into the knowledge base.

**Endpoint:** `POST /upload`
**Content-Type:** `multipart/form-data`

#### Request

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| file | File (PDF) | Yes | The PDF file to upload and ingest |

#### cURL Example

```bash
curl -X POST http://localhost:8000/upload \
  -F "file=@/path/to/medical-guide.pdf"
```

#### Response

```json
{
  "status": "success",
  "message": "Uploaded and ingested medical-guide.pdf",
  "details": {
    "status": "success",
    "files_processed": 1,
    "total_pages": 8,
    "total_chunks": 12
  }
}
```

#### Error Responses

| Status | Description |
|--------|-------------|
| 400 | `{"detail": "Only PDF files are supported"}` |
| 500 | `{"detail": "Upload error: ..."}` |

---

### 5. Rate Limits & Timeouts

| Parameter | Value | Notes |
|-----------|-------|-------|
| Gateway timeout | 30 seconds | For LLM response generation |
| Max chat history | 6 messages | Last 6 messages sent to LLM for context |
| Max file size | Server default | No explicit limit in v1 |
| Concurrent requests | Unlimited (v1) | No rate limiting in v1 |

---

### 6. CORS Configuration

| Origin | Allowed |
|--------|---------|
| `http://localhost:5173` | Yes (Vite dev server) |
| `http://localhost:3000` | Yes (alternative dev port) |
| All other origins | No |

---

### 7. OpenAPI / Swagger

FastAPI automatically generates interactive API documentation:

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`
- **OpenAPI JSON:** `http://localhost:8000/openapi.json`
