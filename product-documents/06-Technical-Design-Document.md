# Technical Design Document

## MedAssist AI - Detailed Technical Design

---

### 1. RAG Pipeline Design

#### 1.1 Embedding Strategy

**Model:** `all-MiniLM-L6-v2` (sentence-transformers)

| Property | Value |
|----------|-------|
| Dimensions | 384 |
| Max Sequence Length | 256 tokens |
| Model Size | ~80MB |
| Inference | CPU (no GPU required) |
| Normalization | L2 normalized (cosine-ready) |

**Why this model:**
- Small and fast enough to run locally on CPU
- Good semantic understanding for medical text
- Same model used for both document embeddings and query embeddings (critical for consistency)
- Free and open-source (no API costs for embeddings)

#### 1.2 Chunking Strategy

**Algorithm:** `RecursiveCharacterTextSplitter` (LangChain)

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| chunk_size | 600 chars | Fits within embedding model's context window while maintaining coherent meaning |
| chunk_overlap | 100 chars | Prevents information loss at chunk boundaries |
| separators | `\n\n`, `\n`, `. `, ` `, `""` | Prioritizes natural text boundaries |

**Chunking flow:**
1. Split on double newlines (paragraph boundaries) first
2. If chunks are still too large, split on single newlines
3. Then on sentence boundaries (`. `)
4. Finally on word boundaries as last resort

#### 1.3 Vector Store Design

**Database:** ChromaDB (PersistentClient)

| Setting | Value |
|---------|-------|
| Distance metric | Cosine similarity |
| HNSW index | Default parameters |
| Persistence | Local filesystem (`./chroma_db`) |
| Collection | `medassist_docs` |

**Document structure per chunk:**
```
{
  id: "doc_0",              // Unique identifier
  document: "chunk text...", // Raw text content
  embedding: [0.12, ...],   // 384-dim float vector
  metadata: {
    source: "/path/to/file.pdf",  // Source file path
    page: 0                        // Page number (0-indexed)
  }
}
```

**Upsert strategy:** IDs are deterministic (`doc_{index}`), so re-ingesting the same documents updates rather than duplicates.

#### 1.4 Retrieval Strategy

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Top-K | 5 | Balances context richness vs. noise |
| Similarity metric | Cosine (via HNSW) | Standard for normalized embeddings |
| Re-ranking | None (v1) | Future: cross-encoder re-ranking |

**Retrieval flow:**
1. Embed user query using same model as documents
2. Query ChromaDB for top-5 nearest neighbors
3. Return chunks with metadata and distance scores
4. Convert cosine distance to similarity: `score = 1 - distance`

---

### 2. Prompt Engineering Design

#### 2.1 System Prompt Structure

```
[ROLE DEFINITION]
  - Who the AI is (MedAssist, healthcare info assistant)

[BEHAVIORAL RULES]
  - Only answer from provided context
  - Never diagnose or prescribe
  - Always cite sources
  - Detect and escalate emergencies
  - Patient-friendly language

[CONTEXT INJECTION]
  - Retrieved chunks formatted with source labels
  - "{context}" placeholder

[CONVERSATION HISTORY]
  - Last 6 messages for continuity
  - "{chat_history}" placeholder

[USER QUERY]
  - Current question
  - "{question}" placeholder
```

#### 2.2 Guardrail Design

| Guardrail | Implementation | Purpose |
|-----------|---------------|---------|
| Context grounding | System prompt instruction | Prevent hallucination |
| No diagnosis | System prompt instruction | Medical safety |
| No prescription | System prompt instruction | Medical safety |
| Source citation | System prompt instruction | Traceability |
| Emergency escalation | Agent-level keyword matching | Patient safety |
| Disclaimer | System prompt instruction | Legal protection |
| Temperature = 0.3 | LLM parameter | Reduce creative/hallucinated responses |

#### 2.3 Context Window Management

| Component | Approximate Tokens |
|-----------|-------------------|
| System prompt (template) | ~200 |
| Retrieved context (5 chunks x 600 chars) | ~750 |
| Chat history (6 messages) | ~300 |
| User question | ~50 |
| **Total input** | **~1,300** |
| Max output | 1,024 |

Well within GPT-4o-mini's 128K context window, leaving room for expansion.

---

### 3. Agentic Routing Design

#### 3.1 Intent Classification Logic

```
classify_intent(query) → ESCALATE | CLARIFY | ANSWER

Priority order:
1. ESCALATE (highest) - emergency keyword match
2. CLARIFY - ambiguous query detection
3. ANSWER (default) - full RAG pipeline
```

#### 3.2 Emergency Detection

**Method:** Keyword substring matching (case-insensitive)

**Keywords list (30+):**
chest pain, heart attack, can't breathe, difficulty breathing, choking, severe bleeding, unconscious, seizure, stroke, anaphylaxis, overdose, poisoning, suicidal, self-harm, severe burn, head injury, loss of consciousness, etc.

**Design decision:** Conservative matching (high recall, accept some false positives). It is better to over-escalate than to miss a real emergency.

#### 3.3 Ambiguity Detection

**Triggers:**
- Query is fewer than 3 words (too vague)
- Matches ambiguous patterns (e.g., starts with pronouns "it", "this", "that")
- Contains multiple `or` statements (uncertain)

**Exception:** If `chat_history` is provided, skip clarification (user has conversational context).

#### 3.4 Clarification Generation

**Method:** Topic-based clarification templates

| Detected Topic | Clarification |
|----------------|---------------|
| diabetes | "Type 1, Type 2, or gestational?" |
| pain | "Where is the pain? How long?" |
| medication | "Which specific medication?" |
| vaccine | "Which vaccine specifically?" |
| Default | "Could you provide more details?" |

---

### 4. Frontend Technical Design

#### 4.1 State Management

```typescript
// Chat state (React useState)
messages: ChatMessage[]      // All messages in conversation
input: string                // Current text input value
isLoading: boolean           // Whether waiting for response

// Derived
chatHistory: {role, content}[]  // Formatted for API (excludes welcome/loading)
```

**No external state library** - React's built-in state is sufficient for a single-page chat application.

#### 4.2 Message Lifecycle

```
User types/speaks → setInput(text)
                         │
User submits → add UserMessage to messages[]
             → add LoadingMessage to messages[]
             → setIsLoading(true)
             → API call (sendQuery)
                         │
        ┌────────────────┴────────────────┐
    Success                           Failure
        │                                 │
  Remove loading msg              Remove loading msg
  Add AssistantMessage             Add ErrorMessage
  with answer + sources            with error text
        │                                 │
        └────────────────┬────────────────┘
                         │
               setIsLoading(false)
               Focus input field
```

#### 4.3 Voice Integration

**Speech-to-Text (STT):**
- Uses `SpeechRecognition` / `webkitSpeechRecognition` API
- Single-shot mode (`continuous: false`)
- Interim results enabled for real-time feedback
- Auto-submits after recognition ends

**Text-to-Speech (TTS):**
- Uses `SpeechSynthesis` API
- Markdown stripped before speaking
- Preferred voices: Samantha, Google, Natural
- Rate: 0.95x (slightly slower for clarity)
- User-initiated only (no auto-play)

---

### 5. Error Handling Design

#### 5.1 Backend Error Handling

| Scenario | HTTP Status | Response |
|----------|-------------|----------|
| Empty question | 400 | `{"detail": "Question cannot be empty"}` |
| Service not ready | 503 | `{"detail": "Service not initialized"}` |
| LLM API error | 500 | `{"detail": "Error processing query: ..."}` |
| Invalid file type | 400 | `{"detail": "Only PDF files are supported"}` |
| PDF load failure | (skipped) | Logged, continues with other files |

#### 5.2 Frontend Error Handling

| Scenario | Behavior |
|----------|----------|
| API call fails | Error message bubble shown in chat |
| Backend disconnected | Yellow warning bar with start command |
| Voice API unavailable | Microphone button hidden |
| TTS fails | Speaker button hidden |

---

### 6. Performance Considerations

| Operation | Expected Time | Bottleneck |
|-----------|---------------|------------|
| Document ingestion (5 PDFs) | ~30 seconds | Embedding model loading (first time) |
| Query embedding | ~50ms | CPU inference |
| ChromaDB retrieval | ~10ms | In-memory HNSW search |
| LLM response generation | 2-4 seconds | API network + token generation |
| **Total query round-trip** | **~3-5 seconds** | LLM API call dominates |

**Optimization notes:**
- Embedding model is loaded once at startup and cached in memory
- ChromaDB uses HNSW index for sub-linear search time
- Chat history is limited to 6 messages to control prompt size
- LLM temperature is low (0.3) for faster, more deterministic responses
