# Testing Strategy Document

## MedAssist AI - Test Plan & QA Strategy

---

### 1. Testing Overview

| Test Level | Scope | Tools |
|------------|-------|-------|
| Unit Tests | Individual functions and modules | pytest, Jest/Vitest |
| Integration Tests | API endpoints, service communication | pytest + httpx, supertest |
| RAG Evaluation | Retrieval quality, answer accuracy | Manual evaluation + metrics |
| UI Testing | Component rendering, interactions | Vitest + React Testing Library |
| E2E Testing | Full user workflows | Playwright / Cypress |
| Manual QA | Voice features, edge cases | Browser testing |

---

### 2. Unit Tests

#### 2.1 Python Backend Unit Tests

**Framework:** pytest

**Test files structure:**
```
backend/ai-service/tests/
├── test_config.py
├── test_ingest.py
├── test_retriever.py
├── test_chain.py
├── test_agent.py
└── conftest.py
```

**Key test cases:**

##### `test_ingest.py`
| Test Case | Description | Expected Result |
|-----------|-------------|-----------------|
| test_load_pdf_valid | Load a valid PDF file | Returns list of Document objects |
| test_load_pdf_invalid | Load a non-existent file | Raises FileNotFoundError |
| test_chunk_documents | Chunk a list of documents | Returns list of chunks within size limits |
| test_chunk_overlap | Verify overlap between consecutive chunks | Last N chars of chunk[i] match first N chars of chunk[i+1] |
| test_chunk_size_config | Chunks respect configured size | All chunks <= CHUNK_SIZE |
| test_ingest_no_pdfs | Ingest with empty directory | Returns error status |

##### `test_retriever.py`
| Test Case | Description | Expected Result |
|-----------|-------------|-----------------|
| test_retrieve_relevant | Query matching ingested content | Returns chunks with relevance > 0.5 |
| test_retrieve_irrelevant | Query with no matching content | Returns chunks with low relevance scores |
| test_retrieve_top_k | Verify top-K parameter | Returns exactly K results |
| test_format_context | Format chunks into context string | Contains source labels and content |
| test_document_count | Check indexed document count | Returns correct count |

##### `test_agent.py`
| Test Case | Description | Expected Result |
|-----------|-------------|-----------------|
| test_classify_escalate_chest_pain | "I have chest pain" | Returns "ESCALATE" |
| test_classify_escalate_cant_breathe | "I can't breathe" | Returns "ESCALATE" |
| test_classify_escalate_suicide | "I'm thinking about suicide" | Returns "ESCALATE" |
| test_classify_clarify_short | "diabetes" | Returns "CLARIFY" |
| test_classify_clarify_vague | "it hurts" | Returns "CLARIFY" |
| test_classify_answer_normal | "What are symptoms of Type 2 diabetes?" | Returns "ANSWER" |
| test_clarify_with_history | Short query but has chat_history | Returns "ANSWER" (skips clarification) |
| test_escalation_response | Emergency query processing | Returns emergency response with phone numbers |
| test_all_emergency_keywords | Test every keyword in list | Each returns "ESCALATE" |

##### `test_chain.py`
| Test Case | Description | Expected Result |
|-----------|-------------|-----------------|
| test_build_prompt_no_history | Build prompt without chat history | Contains system message + user message |
| test_build_prompt_with_history | Build prompt with chat history | Contains formatted history in system message |
| test_prompt_contains_context | Verify context injection | System message contains retrieved context |
| test_extract_sources | Extract unique sources from chunks | Returns deduplicated source list |

#### 2.2 Frontend Unit Tests

**Framework:** Vitest + React Testing Library

**Test files structure:**
```
frontend/src/__tests__/
├── components/
│   ├── MessageBubble.test.tsx
│   ├── ChatWindow.test.tsx
│   └── VoiceInput.test.tsx
├── hooks/
│   ├── useSpeechToText.test.ts
│   └── useTextToSpeech.test.ts
└── services/
    └── api.test.ts
```

**Key test cases:**

| Component | Test Case | Expected Result |
|-----------|-----------|-----------------|
| MessageBubble | Render user message | Blue bubble, right-aligned |
| MessageBubble | Render assistant message | White bubble, left-aligned, with timestamp |
| MessageBubble | Render with sources | Source badges displayed |
| MessageBubble | Render ESCALATE intent | Red emergency badge shown |
| MessageBubble | Render loading state | Typing dots animation |
| ChatWindow | Send message on Enter | Message added to list, API called |
| ChatWindow | Shift+Enter does not send | Newline added instead |
| ChatWindow | Disable input while loading | Input and send button disabled |
| VoiceInput | Hidden when unsupported | Component returns null |
| api.ts | sendQuery success | Returns parsed response |
| api.ts | sendQuery failure | Throws error with detail message |

---

### 3. Integration Tests

#### 3.1 API Integration Tests

**Framework:** pytest + httpx (TestClient)

| Test Case | Method | Endpoint | Expected |
|-----------|--------|----------|----------|
| test_health_check | GET | `/health` | 200, contains `documents_indexed` |
| test_query_valid | POST | `/query` | 200, contains `answer` and `intent` |
| test_query_empty | POST | `/query` | 400, error message |
| test_query_emergency | POST | `/query` | 200, intent = "ESCALATE" |
| test_ingest_endpoint | POST | `/ingest` | 200, contains chunk count |
| test_upload_pdf | POST | `/upload` | 200, file ingested |
| test_upload_non_pdf | POST | `/upload` | 400, "Only PDF files" error |

#### 3.2 Gateway Integration Tests

| Test Case | Description | Expected |
|-----------|-------------|----------|
| test_gateway_proxy_query | Gateway proxies to AI service | Same response as direct API call |
| test_gateway_timeout | AI service slow response | 504 or timeout error |
| test_gateway_service_down | AI service not running | 503 error |

---

### 4. RAG Evaluation

#### 4.1 Retrieval Quality Metrics

| Metric | Formula | Target |
|--------|---------|--------|
| Precision@K | Relevant chunks in top-K / K | > 0.6 |
| Recall@K | Relevant chunks in top-K / total relevant | > 0.8 |
| MRR (Mean Reciprocal Rank) | 1/rank of first relevant chunk | > 0.7 |

#### 4.2 Answer Quality Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| Groundedness | Answer is supported by retrieved context | > 90% |
| Faithfulness | No information fabricated beyond context | > 95% |
| Relevance | Answer addresses the user's question | > 85% |
| Completeness | Answer covers all relevant aspects from context | > 75% |

#### 4.3 Evaluation Test Set

| # | Query | Expected Source | Expected Key Content |
|---|-------|-----------------|---------------------|
| 1 | "What are symptoms of Type 2 diabetes?" | Diabetes-Overview.pdf | Thirst, urination, weight loss, fatigue |
| 2 | "How is blood pressure measured?" | Hypertension-Guide.pdf | Sphygmomanometer, two readings |
| 3 | "What is the DASH diet?" | Hypertension-Guide.pdf | Dietary approaches, sodium reduction |
| 4 | "How to treat a common cold?" | Cold-and-Flu-Guide.pdf | Rest, fluids, OTC medications |
| 5 | "What is CBT?" | Mental-Health-Basics.pdf | Cognitive Behavioral Therapy |
| 6 | "How to perform CPR?" | First-Aid-Basics.pdf | 30 compressions, 2 breaths, rate 100-120 |
| 7 | "What is a normal blood pressure?" | Hypertension-Guide.pdf | Less than 120/80 mmHg |
| 8 | "When should I get the flu vaccine?" | Cold-and-Flu-Guide.pdf | Annual, everyone 6 months+ |
| 9 | "What are signs of depression?" | Mental-Health-Basics.pdf | Sadness, loss of interest, sleep changes |
| 10 | "How to treat a burn?" | First-Aid-Basics.pdf | Cool water, don't pop blisters |

---

### 5. Emergency Detection Tests

**Every emergency keyword must be tested:**

| # | Input Query | Expected Intent |
|---|-------------|-----------------|
| 1 | "I'm having chest pain" | ESCALATE |
| 2 | "My friend can't breathe" | ESCALATE |
| 3 | "She is unconscious and unresponsive" | ESCALATE |
| 4 | "I think I'm having a heart attack" | ESCALATE |
| 5 | "My child is choking" | ESCALATE |
| 6 | "There is severe bleeding" | ESCALATE |
| 7 | "I'm having a seizure" | ESCALATE |
| 8 | "I think this is a stroke" | ESCALATE |
| 9 | "I took an overdose of pills" | ESCALATE |
| 10 | "I'm thinking about suicide" | ESCALATE |
| 11 | "Having difficulty breathing at night" | ESCALATE |
| 12 | "Someone collapsed and lost consciousness" | ESCALATE |

**False positive tests (should NOT escalate):**

| # | Input Query | Expected Intent |
|---|-------------|-----------------|
| 1 | "What causes chest pain during exercise?" | ANSWER |
| 2 | "Tell me about breathing exercises" | ANSWER |
| 3 | "What is the history of heart attacks?" | ANSWER |
| 4 | "How does the brain work during a seizure?" | ANSWER |

---

### 6. Edge Case Tests

| # | Scenario | Input | Expected Behavior |
|---|----------|-------|-------------------|
| 1 | Empty query | "" | 400 error |
| 2 | Very long query | 5000 chars | Truncated, still processed |
| 3 | Non-English query | "Qu'est-ce que le diabete?" | Best-effort answer or "I don't have info" |
| 4 | SQL injection attempt | "'; DROP TABLE docs; --" | Treated as normal text |
| 5 | Code/script injection | "<script>alert('xss')</script>" | Sanitized, treated as text |
| 6 | Off-topic query | "What is the weather today?" | "I don't have information on this" |
| 7 | Multiple questions | "What is diabetes and what is hypertension?" | Attempts to answer both |
| 8 | Follow-up question | "Tell me more about that" | Uses chat history for context |
| 9 | No documents ingested | Any query | Graceful "no information" response |

---

### 7. Performance Tests

| Test | Metric | Target | Tool |
|------|--------|--------|------|
| Query response time | End-to-end latency | < 5 seconds | curl + time |
| Concurrent queries | Throughput | 5 simultaneous queries | locust / k6 |
| Ingestion speed | Pages per second | > 1 page/sec | Python time module |
| Memory usage | RAM consumption | < 2GB under load | psutil |
| Embedding model load | Startup time | < 30 seconds | Server logs |

---

### 8. Manual QA Checklist

#### Browser Compatibility

| Feature | Chrome | Edge | Firefox | Safari |
|---------|--------|------|---------|--------|
| Chat UI | Test | Test | Test | Test |
| Voice Input (STT) | Test | Test | N/A | N/A |
| Voice Output (TTS) | Test | Test | Test | Test |
| Responsive layout | Test | Test | Test | Test |

#### UI/UX Checklist

- [ ] Welcome message displays on first load
- [ ] Messages scroll to bottom automatically
- [ ] Typing indicator shows during response generation
- [ ] Source citations display correctly
- [ ] Emergency badge (red) displays for escalation
- [ ] Clarification badge (amber) displays correctly
- [ ] Microphone button shows recording state
- [ ] Speaker button toggles play/stop
- [ ] Input field auto-resizes for multiline
- [ ] Send button disabled when input is empty
- [ ] Send button disabled during loading
- [ ] Connection status indicator updates correctly
- [ ] Disconnected warning bar shows when backend is down
- [ ] Mobile layout is usable (responsive)
- [ ] Disclaimer text is visible at bottom
