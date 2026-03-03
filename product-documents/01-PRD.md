# Product Requirements Document (PRD)

## MedAssist AI - Healthcare FAQ Chatbot with RAG + Voice

---

### 1. Overview

**Product Name:** MedAssist AI
**Version:** 1.0
**Author:** Ankita Dodamani
**Date:** March 2026
**Status:** In Development

**One-liner:** AI-powered patient support chatbot that answers health queries using RAG over public medical guidelines, with text and voice interaction.

---

### 2. Problem Statement

Patients frequently have health-related questions but face barriers to getting timely, reliable information:
- Long wait times for doctor consultations
- Unreliable health information from general internet searches
- Difficulty understanding complex medical jargon
- No 24/7 access to trusted medical guidance
- Language and accessibility barriers (text-only interfaces)

Healthcare support teams also struggle with:
- Repetitive FAQ queries consuming agent time
- Inconsistent answers across different support agents
- Inability to cite authoritative medical sources in responses

---

### 3. Product Vision

Build an intelligent healthcare information assistant that provides accurate, cited, and grounded answers to patient health queries by retrieving information from trusted public medical documents (WHO, NHS, CDC), with both text and voice interaction capabilities.

---

### 4. Target Users

| User Type | Description | Primary Need |
|-----------|-------------|--------------|
| Patients | Individuals seeking health information | Quick, reliable answers to health questions |
| Healthcare Support Agents | Staff handling patient queries | AI-assisted responses with citations |
| Healthcare Administrators | Oversee knowledge base content | Upload and manage medical documents |

---

### 5. Core Features

#### 5.1 Document Ingestion (P0 - Must Have)
- Upload medical PDFs (guidelines, leaflets, FAQs)
- Automatic text extraction from PDFs
- Intelligent chunking with configurable size and overlap
- Embedding generation using sentence-transformers
- Vector storage in ChromaDB

**Acceptance Criteria:**
- System can ingest PDFs up to 100 pages
- Chunks maintain contextual coherence
- Duplicate documents are handled (upsert, not duplicate)
- Ingestion status and stats are reported

#### 5.2 RAG Query Pipeline (P0 - Must Have)
- User submits a health question (text)
- Query is embedded using the same model as documents
- Top-K most relevant chunks retrieved from ChromaDB
- Retrieved context + query sent to LLM
- LLM generates grounded, cited answer

**Acceptance Criteria:**
- Responses cite source document name and page number
- Answers are grounded only in retrieved context
- Response time under 5 seconds for typical queries
- Relevance scores are returned with each response

#### 5.3 Chat Interface (P0 - Must Have)
- Clean, modern chat UI built with React + TypeScript
- Message history with conversation context
- Typing indicators during response generation
- Source citations displayed per response
- Mobile-responsive design

**Acceptance Criteria:**
- Chat history persists during session
- Up to 6 previous messages included for context
- UI is accessible and responsive on mobile devices
- Error states are handled gracefully

#### 5.4 Agentic Routing (P0 - Must Have)
The system intelligently routes each query into one of three paths:

| Path | Trigger | Behavior |
|------|---------|----------|
| ANSWER | Standard health question | Full RAG pipeline with cited response |
| CLARIFY | Ambiguous or vague query | Ask clarifying question before answering |
| ESCALATE | Emergency symptoms detected | Immediate emergency services redirect |

**Acceptance Criteria:**
- Emergency keywords (chest pain, can't breathe, etc.) trigger immediate escalation
- Vague queries (< 3 words, no context) prompt clarification
- Agent intent is visible in the UI (badge on response)

#### 5.5 Voice Input (P1 - Should Have)
- Microphone button for voice-to-text input
- Uses Web Speech API (SpeechRecognition)
- Visual feedback during recording (pulse animation)
- Auto-submits transcribed text

**Acceptance Criteria:**
- Works in Chrome and Edge browsers
- Graceful degradation if browser doesn't support Speech API
- Recording state is clearly indicated to user

#### 5.6 Voice Output (P1 - Should Have)
- Text-to-speech for assistant responses
- Speaker button on each assistant message
- Uses browser SpeechSynthesis API
- Stop button to interrupt playback

**Acceptance Criteria:**
- Markdown formatting is stripped before speaking
- Preferred natural voice selected when available
- Does not auto-play (user-initiated only)

#### 5.7 Healthcare Safety Guardrails (P0 - Must Have)
- System never diagnoses conditions
- System never prescribes medication
- All answers cite source documents
- Emergency symptom detection and escalation
- Disclaimer on every response

**Acceptance Criteria:**
- System prompt enforces all guardrails
- Emergency keywords list covers major emergencies
- Every response ends with "consult your healthcare provider" reminder

---

### 6. Out of Scope (v1.0)

- User authentication and accounts
- Multi-language support
- HIPAA-compliant data handling
- EHR (Electronic Health Record) integration
- Appointment scheduling
- Real doctor handoff / live chat
- Document OCR (scanned PDFs)
- Analytics dashboard

---

### 7. Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Response Accuracy | > 85% grounded in source docs | Manual evaluation on test queries |
| Response Time | < 5 seconds | API latency measurement |
| Emergency Detection | 100% recall | Test against emergency keyword list |
| User Satisfaction | > 4.0/5.0 | Post-interaction survey (future) |
| Knowledge Coverage | > 80% of common health FAQs | Coverage against test query set |

---

### 8. Technical Constraints

- LLM requires API key (OpenAI GPT-4o-mini or Claude)
- Embedding model runs locally (all-MiniLM-L6-v2)
- ChromaDB runs locally (no cloud dependency for v1)
- Voice features require modern browser (Chrome/Edge)
- Python 3.9+ for backend, Node.js 18+ for frontend

---

### 9. Timeline

| Phase | Duration | Deliverables |
|-------|----------|-------------- |
| Phase 1 | Week 1 | Python RAG backend + document ingestion |
| Phase 2 | Week 2 | React chat UI + NestJS gateway + integration |
| Phase 3 | Week 3 | Voice I/O + agentic routing + polish + deployment |

---

### 10. Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| LLM hallucination | High - incorrect medical info | Strict grounding in retrieved context + system prompt guardrails |
| Emergency missed | Critical - patient safety | Comprehensive emergency keyword list + conservative detection |
| API rate limits | Medium - degraded experience | Rate limiting on frontend + queue on backend |
| Outdated medical info | Medium - incorrect guidance | Regularly update knowledge base PDFs |
| Browser compatibility | Low - voice features | Graceful fallback to text-only mode |
