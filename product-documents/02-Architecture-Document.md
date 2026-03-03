# Architecture Document

## MedAssist AI - System Architecture

---

### 1. Architecture Overview

MedAssist AI follows a **three-tier architecture** with a React frontend, NestJS API gateway, and Python AI service handling RAG and LLM orchestration.

```
+--------------------------------------------------+
|                   CLIENT TIER                     |
|                                                   |
|  React + TypeScript + Tailwind CSS (Vite)         |
|  - Chat UI (ChatWindow, MessageBubble)            |
|  - Voice Input (Web Speech API)                   |
|  - Voice Output (SpeechSynthesis API)             |
|  - API Client (fetch → /api/*)                    |
|                                                   |
+-------------------------+------------------------+
                          |
                    HTTP REST API
                          |
+-------------------------v------------------------+
|                  GATEWAY TIER                     |
|                                                   |
|  NestJS (Node.js) - Port 3001                     |
|  - Request routing & validation                   |
|  - Session management                             |
|  - Auth middleware (future)                        |
|  - Proxy to Python AI service                     |
|                                                   |
+-------------------------+------------------------+
                          |
                    HTTP REST API
                          |
+-------------------------v------------------------+
|                 AI SERVICE TIER                   |
|                                                   |
|  FastAPI (Python) - Port 8000                     |
|  - Agent Router (ANSWER/CLARIFY/ESCALATE)         |
|  - RAG Chain (prompt construction + LLM call)     |
|  - Retriever (query embedding + similarity search)|
|  - Ingestion Pipeline (PDF → chunks → embeddings) |
|                                                   |
+-------------------------+------------------------+
                          |
              +-----------+-----------+
              |                       |
   +----------v---------+  +---------v----------+
   |     ChromaDB        |  |    LLM API          |
   |  (Vector Store)     |  |  (OpenAI/Claude)    |
   |  - Document chunks  |  |  - GPT-4o-mini      |
   |  - Embeddings       |  |  - Response gen      |
   |  - Metadata         |  |                      |
   +--------------------+  +---------------------+
```

---

### 2. Component Details

#### 2.1 Frontend (React + TypeScript)

**Purpose:** User-facing chat interface with voice capabilities

| Component | File | Responsibility |
|-----------|------|----------------|
| App | `App.tsx` | Layout, header, health status indicator |
| ChatWindow | `ChatWindow.tsx` | Message list, input area, send logic |
| MessageBubble | `MessageBubble.tsx` | Individual message display, TTS button, source citations |
| VoiceInput | `VoiceInput.tsx` | Microphone button, speech-to-text |
| useSpeechToText | `hooks/useSpeechToText.ts` | Web Speech API wrapper for STT |
| useTextToSpeech | `hooks/useTextToSpeech.ts` | SpeechSynthesis API wrapper for TTS |
| api | `services/api.ts` | HTTP client for backend communication |

**Key Decisions:**
- Vite for fast development builds
- Tailwind CSS v4 for utility-first styling
- No state management library (React state sufficient for v1)
- Direct API calls via fetch (no axios dependency)

#### 2.2 API Gateway (NestJS)

**Purpose:** API routing, request validation, proxy to AI service

| File | Responsibility |
|------|----------------|
| `main.ts` | Bootstrap NestJS app, CORS config |
| `app.module.ts` | Module registration |
| `chat.controller.ts` | REST endpoints (`/api/query`, `/api/health`, `/api/ingest`) |
| `ai-service.proxy.ts` | HTTP proxy to Python FastAPI service |

**Key Decisions:**
- Thin proxy layer (business logic lives in Python service)
- 30-second timeout for LLM calls
- CORS configured for localhost dev

#### 2.3 AI Service (Python FastAPI)

**Purpose:** Core AI/ML logic - RAG pipeline, agentic routing, LLM orchestration

| Module | File | Responsibility |
|--------|------|----------------|
| Config | `config.py` | Environment variables, paths, settings |
| Ingestion | `ingest.py` | PDF loading, chunking, embedding, ChromaDB storage |
| Retriever | `retriever.py` | Query embedding, similarity search, context formatting |
| Chain | `chain.py` | Prompt construction, LLM invocation, response parsing |
| Agent | `agent.py` | Intent classification, routing (ANSWER/CLARIFY/ESCALATE) |
| API | `main.py` | FastAPI endpoints, request/response models |

---

### 3. Data Flow

#### 3.1 Document Ingestion Flow

```
PDF File
  │
  ▼
PyPDFLoader (load pages)
  │
  ▼
RecursiveCharacterTextSplitter
  ├── chunk_size: 600 tokens
  └── chunk_overlap: 100 tokens
  │
  ▼
HuggingFaceEmbeddings (all-MiniLM-L6-v2)
  │  384-dimension vectors
  ▼
ChromaDB (PersistentClient)
  ├── documents: chunk text
  ├── embeddings: vector representation
  └── metadata: source file, page number
```

#### 3.2 Query Processing Flow

```
User Question (text or voice)
  │
  ▼
Agent: classify_intent(query)
  │
  ├─── ESCALATE → Emergency response (no LLM call)
  │
  ├─── CLARIFY → Clarification question (no LLM call)
  │
  └─── ANSWER
         │
         ▼
       Retriever: embed query → ChromaDB similarity search
         │  Returns top-5 chunks with relevance scores
         ▼
       Chain: build prompt (system + context + history + question)
         │
         ▼
       LLM API call (GPT-4o-mini, temp=0.3)
         │
         ▼
       Response with answer + source citations
```

---

### 4. Database Schema

#### ChromaDB Collection: `medassist_docs`

| Field | Type | Description |
|-------|------|-------------|
| id | string | Unique chunk ID (e.g., `doc_0`, `doc_1`) |
| document | string | Raw text content of the chunk |
| embedding | float[384] | Vector embedding (all-MiniLM-L6-v2) |
| metadata.source | string | Source PDF file path |
| metadata.page | int | Page number in source PDF |

**Index:** HNSW with cosine similarity

---

### 5. API Architecture

| Method | Endpoint | Service | Description |
|--------|----------|---------|-------------|
| GET | `/health` | FastAPI | Health check + document count |
| POST | `/query` | FastAPI | Process user query through agent |
| POST | `/ingest` | FastAPI | Ingest all PDFs from knowledge_base/ |
| POST | `/upload` | FastAPI | Upload and ingest a single PDF |
| GET | `/api/health` | NestJS | Proxied health check |
| POST | `/api/query` | NestJS | Proxied query |
| POST | `/api/ingest` | NestJS | Proxied ingestion |

---

### 6. Security Considerations

| Area | Approach |
|------|----------|
| API Keys | Stored in `.env`, never committed to git |
| CORS | Restricted to localhost origins in development |
| Input Validation | Pydantic models for all request/response schemas |
| Medical Safety | System prompt guardrails prevent diagnosis/prescription |
| Data Privacy | No patient data stored; only public medical docs |
| Emergency Handling | Conservative keyword matching for safety escalation |

---

### 7. Scalability Considerations (Future)

| Current | Future |
|---------|--------|
| ChromaDB local | Pinecone / Weaviate cloud |
| In-memory chat history | Redis / PostgreSQL |
| Single FastAPI instance | Kubernetes with horizontal scaling |
| File-based PDF upload | S3 + async processing queue |
| No auth | JWT + OAuth2 |
| No caching | Redis cache for frequent queries |

---

### 8. Technology Stack Summary

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| Frontend | React | 19.x | UI framework |
| Frontend | TypeScript | 5.x | Type safety |
| Frontend | Vite | 7.x | Build tool |
| Frontend | Tailwind CSS | 4.x | Styling |
| Gateway | NestJS | 10.x | API routing |
| Gateway | Axios | 1.x | HTTP proxy |
| AI Service | Python | 3.9+ | Runtime |
| AI Service | FastAPI | 0.115 | API framework |
| AI Service | LangChain | 0.3 | RAG orchestration |
| AI Service | ChromaDB | 0.5 | Vector database |
| AI Service | sentence-transformers | 3.3 | Embeddings |
| LLM | OpenAI GPT-4o-mini | - | Response generation |
| Voice | Web Speech API | - | STT |
| Voice | SpeechSynthesis API | - | TTS |
