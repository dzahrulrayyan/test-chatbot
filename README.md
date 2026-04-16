# PT Chatbot — Pendakwah Teknologi AI Assistant

AI-powered chatbot for **Pendakwah Teknologi Solutions**, a digital transformation and training company specializing in AI, cybersecurity, content creation, and media solutions.

Built by [Pendakwah Teknologi](https://pendakwah.tech). Runs on NVIDIA GX10 Grace Blackwell.

---

## What It Does

PT Chatbot answers questions about Pendakwah Teknologi's services — AI training, cybersecurity workshops, video production, digital transformation consulting, brand endorsements, and more — grounded in the company's knowledge base.

Users can ask in Bahasa Melayu or English. The system retrieves relevant document sections, searches the web for current information when needed, and generates answers with source references.

---

## Architecture

```
User Query
    |
    v
[1] Query Classification (internal / external / hybrid)
    |
    v
[2] Query Expansion (LLM generates 3 search variants)
    |
    v
[3] Hybrid Retrieval (Vector + BM25 + Reciprocal Rank Fusion)
    |               \
    v                v
[4] Web Search      [5] Cross-Encoder Reranking
    (Tavily/Brave)       (GPU, top 7)
    |               /
    v              v
[6] LLM Generation (GPT-4o, streaming SSE)
    |
    v
[7] Self-Evaluation (3-dimension quality scoring)
    |
    v
[8] Follow-up Suggestions (3 contextual next questions)
```

### Components

| Component | Technology | Details |
|-----------|-----------|---------|
| **Main LLM** | GPT-4o | Via OpenAI API, key round-robin, streaming |
| **Fast LLM** | GPT-4o-mini | Query expansion, self-eval, follow-ups |
| **Embeddings** | Mesolitica Mistral 191M | Malay-optimized, 1024-dim, GPU-accelerated |
| **Reranker** | ms-marco-MiniLM-L-6-v2 | Cross-encoder on GPU |
| **Vector DB** | ChromaDB | HNSW index (M=32, ef=200), persistent |
| **Web Search** | Tavily + Brave | Dual-provider fallback |
| **STT** | Whisper large-v3 | Faster-Whisper, float16 on GPU |
| **TTS** | MMS-TTS Malay | Meta's multilingual speech, GPU |
| **Cache** | Redis | Shared across workers, 10min TTL |
| **Backend** | FastAPI + Uvicorn | 4 workers, uvloop, async |
| **Gateway** | Nginx | SSL, rate limiting, SSE proxy, gzip |

---

## Project Structure

```
pt-chatbot/
  backend/
    app.py              # FastAPI application (endpoints, streaming, voice, admin)
    providers.py         # RAG pipeline (retrieval, reranking, generation, web search)
    agency_config.py     # System prompt, keywords, company metadata
  frontend/
    index.html           # Chat interface (single-page app)
    architecture.html    # System architecture documentation page
    admin.html           # Log & audit trail dashboard
    pt.jpg               # Company logo
  configs/
    backend.env.template # Environment variables template (copy to backend.env)
    pt-chatbot.service   # systemd service unit
    pt-chatbot.conf      # Nginx site configuration
  knowledge/             # Place knowledge base documents here (PDF, DOCX, TXT, MD)
  logo/
    pt.jpg               # Company logo
  scripts/
    setup.sh             # Automated setup (venv, deps, models, systemd, nginx)
    ingest.sh            # Document ingestion into ChromaDB
  requirements.txt       # Python dependencies
```

---

## Setup

### Prerequisites

- Ubuntu 22.04+ (tested on 24.04 aarch64)
- Python 3.11+
- NVIDIA GPU with CUDA 12+ (optional, falls back to CPU)
- Redis server
- Nginx (for production deployment)

### Installation

```bash
# Clone the repository
git clone https://github.com/pendakwahteknologi/pt-chatbot.git
cd pt-chatbot

# Run automated setup
bash scripts/setup.sh
```

The setup script will:
1. Detect GPU and platform capabilities
2. Create `/opt/pt-chatbot/` directory structure
3. Copy backend, frontend, and knowledge files
4. Create Python virtual environment with all dependencies
5. Install GPU-accelerated PyTorch (if GPU detected)
6. Pre-download embedding and reranker models
7. Install systemd service and nginx config

### Configuration

```bash
# Edit the environment file with your API keys
nano /opt/pt-chatbot/backend.env
```

Required keys:

```env
# OpenAI API (required — main LLM provider)
OPENAI_API_KEYS=sk-your-openai-api-key

# Web Search (optional — enables internet search)
TAVILY_API_KEY=tvly-your-key
BRAVE_API_KEY=your-brave-key
```

### Document Ingestion

```bash
# Ingest documents into ChromaDB (GPU-accelerated)
bash scripts/ingest.sh
```

This clears ChromaDB, extracts text from all PDFs/DOCX/TXT/MD files in `/opt/pt-chatbot/knowledge/` and `/opt/pt-chatbot/documents/`, chunks them with page tracking, embeds on GPU, and stores in ChromaDB.

### Start

```bash
# Start the service
sudo systemctl start pt-chatbot

# Enable auto-start on boot
sudo systemctl enable pt-chatbot

# Check health
curl http://localhost:8003/api/health
```

---

## API Endpoints

### Chat

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/chat` | Synchronous chat (returns full response) |
| `POST` | `/api/chat/stream` | Streaming chat (SSE events: sources, chunks, done) |

**Request body:**
```json
{
  "messages": [
    {"role": "user", "content": "Apakah perkhidmatan Pendakwah Teknologi?"}
  ]
}
```

**Response includes:** reply, retrieval sources (with page numbers), query type, self-evaluation scores, follow-up suggestions.

### Voice

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/voice/transcribe/local` | Speech-to-text (base64 audio) |
| `POST` | `/api/voice/synthesize/local` | Text-to-speech (returns WAV) |

### System

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/health` | Service health + document count |
| `GET` | `/api/mode` | Current mode, features, model info |
| `GET` | `/api/cache/stats` | Redis cache statistics |
| `POST` | `/api/cache/clear` | Clear response cache |

### Feedback

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/feedback` | Submit rating (1-5) and comment |
| `GET` | `/api/feedback/stats` | Rating distribution and average |

### Admin

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/admin/conversations` | Full conversation audit log |
| `GET` | `/api/admin/feedback` | All feedback with IP tracking |
| `GET` | `/api/admin/summary` | Aggregate stats (IPs, response times, cache hits) |

---

## Frontend Pages

| Page | URL | Description |
|------|-----|-------------|
| **Chat** | `/` | Main chat interface with voice input, markdown rendering, source references |
| **Architecture** | `/architecture.html` | Full system documentation with pipeline flow and component details |
| **Admin** | `/admin.html` | Audit trail dashboard — conversations, feedback, IP tracking, stats |

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_BASE_URL` | `https://api.openai.com/v1` | LLM API base URL |
| `OPENAI_API_KEYS` | *(required)* | Comma-separated API keys |
| `OPENAI_MODEL` | `gpt-4o` | Main LLM model |
| `OPENAI_MODEL_FAST` | `gpt-4o-mini` | Fast LLM for utilities |
| `EMBEDDING_DEVICE` | `cuda` | Embedding compute device |
| `CROSS_ENCODER_DEVICE` | `cuda` | Reranker compute device |
| `RETRIEVAL_TOP_K` | `15` | Vector search results per query |
| `EMBEDDING_BATCH_SIZE` | `256` | GPU embedding batch size |
| `CACHE_TTL_SECONDS` | `600` | Redis cache TTL |
| `TAVILY_API_KEY` | *(optional)* | Tavily web search API key |
| `BRAVE_API_KEY` | *(optional)* | Brave Search API key |
| `CHROMA_PERSIST_DIR` | `/opt/pt-chatbot/chroma_db` | ChromaDB storage path |

---

## Adding Documents

Place PDF, DOCX, TXT, or MD files in `/opt/pt-chatbot/knowledge/` or `/opt/pt-chatbot/documents/`, then re-ingest:

```bash
bash scripts/ingest.sh
sudo systemctl restart pt-chatbot
```

PDF files are extracted with page markers — each chunk in ChromaDB stores which page(s) it came from, enabling precise page references in answers.

---

## License

Proprietary. Copyright Pendakwah Teknologi.
