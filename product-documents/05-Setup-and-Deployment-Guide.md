# Setup & Deployment Guide

## MedAssist AI - Installation and Deployment

---

### 1. Prerequisites

| Requirement | Version | Check Command |
|-------------|---------|---------------|
| Python | 3.9+ | `python3 --version` |
| Node.js | 18+ | `node --version` |
| npm | 9+ | `npm --version` |
| Git | 2.x | `git --version` |
| OpenAI API Key | - | [platform.openai.com](https://platform.openai.com) |

**Hardware:**
- RAM: 4GB minimum (8GB recommended for embedding model)
- Disk: 2GB free space (for dependencies + ChromaDB)
- CPU: Any modern processor (embedding model runs on CPU)

---

### 2. Project Structure

```
medassist-ai/
├── frontend/                  # React + TypeScript + Vite
├── backend/
│   ├── ai-service/            # Python FastAPI (RAG + LLM)
│   └── gateway/               # NestJS API gateway
├── knowledge_base/            # Medical PDF documents
├── scripts/                   # Utility scripts
└── product-documents/         # Project documentation
```

---

### 3. Local Development Setup

#### Step 1: Clone the Repository

```bash
git clone <your-repo-url>
cd medassist-ai
```

#### Step 2: Set Up the Python AI Service

```bash
# Navigate to the AI service
cd backend/ai-service

# Create virtual environment
python3 -m venv venv
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate          # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
```

Edit `.env` and add your API key:
```env
OPENAI_API_KEY=sk-your-openai-api-key-here
```

#### Step 3: Prepare the Knowledge Base

Option A - Use sample PDFs (for testing):
```bash
cd ../../
python3 scripts/create_sample_pdfs.py
```

Option B - Add your own PDFs:
```bash
# Copy medical PDF documents into the knowledge_base/ folder
cp /path/to/your-medical-docs/*.pdf knowledge_base/
```

#### Step 4: Ingest Documents

```bash
cd backend/ai-service
source venv/bin/activate
python ingest.py
```

Expected output:
```
🏥 MedAssist AI - Document Ingestion Pipeline
📂 Found 5 PDF file(s)
📄 Loading PDF: ...
🔪 Split into 40 chunks
🧠 Loading embedding model: all-MiniLM-L6-v2
💾 Storing in ChromaDB
✅ Ingestion complete!
```

#### Step 5: Start the AI Service

```bash
# Still in backend/ai-service with venv activated
python main.py
```

The FastAPI server starts at `http://localhost:8000`

Verify: `curl http://localhost:8000/health`

#### Step 6: Set Up the Frontend

```bash
# Open a new terminal
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

The frontend starts at `http://localhost:5173`

#### Step 7: Set Up the NestJS Gateway (Optional)

```bash
# Open a new terminal
cd backend/gateway

# Install dependencies
npm install

# Start dev server
npm run start:dev
```

The gateway starts at `http://localhost:3001`

---

### 4. Environment Variables

#### AI Service (`backend/ai-service/.env`)

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| OPENAI_API_KEY | Yes | - | OpenAI API key for LLM calls |
| ANTHROPIC_API_KEY | No | - | Alternative: Anthropic API key |
| EMBEDDING_MODEL | No | `all-MiniLM-L6-v2` | HuggingFace embedding model name |
| CHROMA_PERSIST_DIR | No | `./chroma_db` | ChromaDB storage directory |
| CHROMA_COLLECTION_NAME | No | `medassist_docs` | ChromaDB collection name |
| CHUNK_SIZE | No | `600` | Document chunk size in characters |
| CHUNK_OVERLAP | No | `100` | Overlap between chunks |
| TOP_K_RESULTS | No | `5` | Number of chunks to retrieve per query |
| HOST | No | `0.0.0.0` | Server host |
| PORT | No | `8000` | Server port |

#### Frontend (`frontend/.env`)

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| VITE_API_URL | No | `http://localhost:8000` | AI service URL |

#### Gateway (`backend/gateway/.env`)

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| GATEWAY_PORT | No | `3001` | Gateway server port |
| AI_SERVICE_URL | No | `http://localhost:8000` | Python AI service URL |

---

### 5. Running All Services

#### Using Multiple Terminals

```bash
# Terminal 1: AI Service
cd backend/ai-service && source venv/bin/activate && python main.py

# Terminal 2: Frontend
cd frontend && npm run dev

# Terminal 3: Gateway (optional)
cd backend/gateway && npm run start:dev
```

#### Quick Start Script

Create a `start.sh` in the project root:

```bash
#!/bin/bash
echo "🏥 Starting MedAssist AI..."

# Start AI Service
cd backend/ai-service
source venv/bin/activate
python main.py &
AI_PID=$!
echo "✅ AI Service started (PID: $AI_PID)"

# Start Frontend
cd ../../frontend
npm run dev &
FE_PID=$!
echo "✅ Frontend started (PID: $FE_PID)"

echo ""
echo "🌐 Frontend: http://localhost:5173"
echo "🔧 AI Service: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"

trap "kill $AI_PID $FE_PID 2>/dev/null" EXIT
wait
```

---

### 6. Production Deployment

#### 6.1 Frontend - Vercel

```bash
cd frontend

# Build for production
npm run build

# Deploy to Vercel
npx vercel --prod
```

Set environment variable in Vercel dashboard:
- `VITE_API_URL` = your deployed backend URL

#### 6.2 AI Service - Railway / Render

**Railway:**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

**Render:**
1. Connect your GitHub repository
2. Create a new Web Service pointing to `backend/ai-service`
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables (OPENAI_API_KEY, etc.)

#### 6.3 Docker (Alternative)

**AI Service Dockerfile** (`backend/ai-service/Dockerfile`):
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Build and run:**
```bash
docker build -t medassist-ai ./backend/ai-service
docker run -p 8000:8000 --env-file ./backend/ai-service/.env medassist-ai
```

---

### 7. Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| `OpenAIError: api_key must be set` | Missing API key | Add `OPENAI_API_KEY` to `.env` file |
| `No PDF files found` | Empty knowledge_base/ | Add PDFs or run `create_sample_pdfs.py` |
| `ModuleNotFoundError` | venv not activated | Run `source venv/bin/activate` |
| Frontend shows "Disconnected" | Backend not running | Start the AI service first |
| Voice input not working | Unsupported browser | Use Chrome or Edge |
| Slow first query | Embedding model loading | First query loads model into memory; subsequent queries are fast |
| `urllib3 NotOpenSSLWarning` | Old Python SSL | Safe to ignore; doesn't affect functionality |
| Port already in use | Another process on port | Kill the process or change port in `.env` |

---

### 8. Updating the Knowledge Base

To add new documents after initial setup:

```bash
# Option 1: Add PDFs and re-ingest all
cp new-guide.pdf knowledge_base/
cd backend/ai-service
source venv/bin/activate
python ingest.py

# Option 2: Upload via API
curl -X POST http://localhost:8000/upload -F "file=@new-guide.pdf"
```

To reset the knowledge base:
```bash
# Remove the ChromaDB database and re-ingest
rm -rf backend/ai-service/chroma_db
cd backend/ai-service && python ingest.py
```
