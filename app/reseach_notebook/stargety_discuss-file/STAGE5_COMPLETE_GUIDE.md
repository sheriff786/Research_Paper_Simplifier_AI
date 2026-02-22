# 🚀 STAGE 5: FastAPI Backend + Production Deployment
## Complete REST API & Deployment Guide

---

## 📋 Table of Contents
1. [Overview](#overview)
2. [Architecture](#architecture)
3. [API Endpoints](#api-endpoints)
4. [Implementation](#implementation)
5. [Deployment](#deployment)
6. [Testing](#testing)
7. [Monitoring](#monitoring)

---

## 🎯 Overview

**Goal:** Transform Stage 4 notebook into production-ready REST API

**What You Get:**
- ✅ Professional REST API (FastAPI)
- ✅ Multi-user session management
- ✅ File upload/processing pipeline
- ✅ Auto-generated API documentation
- ✅ Docker containerization
- ✅ Production deployment configs
- ✅ Rate limiting & security
- ✅ Error handling & logging

**Time to Build:** 1-2 days  
**Difficulty:** Intermediate  
**Cost:** $0-10/month (depending on hosting)

---

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│         CLIENT LAYER                │
│  • Gradio UI                        │
│  • React App                        │
│  • Mobile App                       │
│  • CLI Tool                         │
└──────────────┬──────────────────────┘
               │ HTTP/REST
               ↓
┌─────────────────────────────────────┐
│       FASTAPI APPLICATION           │
├─────────────────────────────────────┤
│  API Routes:                        │
│  ├─ /api/v1/upload                  │
│  ├─ /api/v1/process/{paper_id}      │
│  ├─ /api/v1/chat                    │
│  ├─ /api/v1/papers/{paper_id}       │
│  ├─ /api/v1/papers                  │
│  └─ /api/v1/health                  │
│                                     │
│  Middleware:                        │
│  ├─ CORS                            │
│  ├─ Rate Limiting                   │
│  ├─ Error Handling                  │
│  └─ Request Logging                 │
└──────────────┬──────────────────────┘
               │
               ↓
┌─────────────────────────────────────┐
│       BUSINESS LOGIC LAYER          │
├─────────────────────────────────────┤
│  Services:                          │
│  ├─ PaperProcessor                  │
│  ├─ ChatbotManager                  │
│  ├─ SessionManager                  │
│  └─ FileHandler                     │
└──────────────┬──────────────────────┘
               │
               ↓
┌─────────────────────────────────────┐
│         DATA LAYER                  │
├─────────────────────────────────────┤
│  Storage:                           │
│  ├─ FAISS Vector Store              │
│  ├─ JSON Files (Stages 1-3)         │
│  ├─ Uploaded PDFs                   │
│  └─ Session Data                    │
└─────────────────────────────────────┘
```

---

## 🔌 API Endpoints Specification

### **1. Health Check**

```http
GET /api/v1/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-02-22T12:00:00Z",
  "version": "1.0.0",
  "services": {
    "vectorstore": "available",
    "llm": "available"
  }
}
```

---

### **2. Upload PDF**

```http
POST /api/v1/upload
Content-Type: multipart/form-data
```

**Request:**
```
file: PDF file (max 10MB)
```

**Response:**
```json
{
  "paper_id": "550e8400-e29b-41d4-a716-446655440000",
  "filename": "research_paper.pdf",
  "size_bytes": 1234567,
  "status": "uploaded",
  "message": "File uploaded successfully. Use paper_id to process.",
  "uploaded_at": "2024-02-22T12:00:00Z"
}
```

**Error Response:**
```json
{
  "detail": "File too large. Maximum size is 10MB"
}
```

---

### **3. Process Paper**

```http
POST /api/v1/process/{paper_id}
```

**Response:**
```json
{
  "paper_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "processing",
  "stages": {
    "stage1_extraction": "pending",
    "stage2_vectorization": "pending",
    "stage3_simplification": "pending"
  },
  "estimated_time_seconds": 180,
  "message": "Processing started. Check status with GET /api/v1/papers/{paper_id}"
}
```

**Background Processing:**
- Runs Stages 1, 2, 3 automatically
- Updates status in real-time
- Stores results in `processed/{paper_id}/`

---

### **4. Get Paper Info**

```http
GET /api/v1/papers/{paper_id}
```

**Response:**
```json
{
  "paper_id": "550e8400-e29b-41d4-a716-446655440000",
  "filename": "research_paper.pdf",
  "status": "completed",
  "metadata": {
    "title": "Generative AI in Architecture...",
    "authors": "Memon et al.",
    "pages": 19,
    "uploaded_at": "2024-02-22T12:00:00Z",
    "processed_at": "2024-02-22T12:03:15Z"
  },
  "simplified": {
    "tldr": "This paper reviews how AI is being used in construction...",
    "key_findings": [
      "7 main themes identified",
      "Construction most studied",
      "Limited empirical studies"
    ]
  },
  "statistics": {
    "text_chunks": 45,
    "tables": 9,
    "figures": 9,
    "total_searchable_items": 63
  }
}
```

---

### **5. Chat with Paper**

```http
POST /api/v1/chat
Content-Type: application/json
```

**Request:**
```json
{
  "paper_id": "550e8400-e29b-41d4-a716-446655440000",
  "question": "What are the main themes identified in this paper?",
  "session_id": "optional-session-id"
}
```

**Response:**
```json
{
  "answer": "The paper identifies 7 main themes through thematic analysis:\n\n1. Strategic Definition & Brief\n2. Architectural Design\n3. Structural Design\n4. BIM (Building Information Modeling)\n5. Construction & Demolition\n6. Operations\n7. Urban Governance & Smart Cities\n\nConstruction & Demolition is the most studied theme with 15 out of 28 papers focusing on it. [Source: Results, Page 6; Figure 2]",
  "sources": [
    {
      "type": "text",
      "section": "results",
      "page": 6,
      "content": "A total of seven themes were identified...",
      "relevance_score": 0.92
    },
    {
      "type": "figure",
      "figure_id": "fig_0002",
      "page": 6,
      "content": "Thematic hierarchy chart showing 7 main themes"
    }
  ],
  "session_id": "550e8400-e29b-41d4-a716-446655440001",
  "timestamp": "2024-02-22T12:05:30Z"
}
```

---

### **6. List All Papers**

```http
GET /api/v1/papers?limit=10&offset=0&status=completed
```

**Response:**
```json
{
  "papers": [
    {
      "paper_id": "550e8400-e29b-41d4-a716-446655440000",
      "filename": "research_paper.pdf",
      "title": "GenAI in Architecture...",
      "status": "completed",
      "uploaded_at": "2024-02-22T12:00:00Z"
    }
  ],
  "total": 25,
  "limit": 10,
  "offset": 0
}
```

---

### **7. Get Summary**

```http
GET /api/v1/papers/{paper_id}/summary
```

**Response:**
```json
{
  "paper_id": "550e8400-e29b-41d4-a716-446655440000",
  "tldr": "This paper reviews how Generative AI is being used...",
  "sections": {
    "abstract": "Simplified abstract...",
    "introduction": "Simplified intro...",
    "methodology": "They used systematic review of 28 papers..."
  },
  "key_findings": [
    "7 themes identified",
    "Construction most studied (15/28 papers)",
    "Limited real-world applications"
  ],
  "strengths": [
    "Comprehensive review methodology",
    "Clear thematic analysis",
    "Identifies research gaps"
  ],
  "limitations": [
    "Most papers are reviews, not empirical",
    "Limited to Australian context",
    "Recent papers only (2023-2025)"
  ]
}
```

---

## 💻 Implementation

### **Project Structure**

```
stage5_backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app
│   ├── config.py              # Configuration
│   ├── models.py              # Pydantic models
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── health.py          # Health check
│   │   ├── papers.py          # Paper endpoints
│   │   └── chat.py            # Chat endpoint
│   ├── services/
│   │   ├── __init__.py
│   │   ├── paper_processor.py # Processing pipeline
│   │   ├── chatbot.py         # Chat logic
│   │   └── session_manager.py # Session handling
│   └── utils/
│       ├── __init__.py
│       ├── file_handler.py    # File operations
│       └── logger.py          # Logging setup
├── uploads/                   # Uploaded PDFs
├── processed/                 # Processed outputs
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

---

### **Core Files**

#### **1. requirements.txt**

```txt
# FastAPI
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6

# Pydantic
pydantic==2.5.0
pydantic-settings==2.1.0

# LangChain & AI
langchain==0.3.0
langchain-openai==0.2.0
langchain-community==0.3.0
openai==1.54.0

# Vector DB
faiss-cpu==1.9.0

# Embeddings
sentence-transformers==3.3.1
tiktoken==0.8.0

# CrewAI (for processing)
crewai==0.86.0

# PDF Processing
PyMuPDF==1.24.0
pdfplumber==0.11.0
camelot-py[cv]==0.11.0
Pillow==10.4.0

# Utilities
python-dotenv==1.0.0
aiofiles==23.2.1

# Rate Limiting
slowapi==0.1.9

# CORS
python-jose[cryptography]==3.3.0

# Monitoring
prometheus-client==0.19.0
```

---

#### **2. .env.example**

```env
# API Keys
OPENAI_API_KEY=sk-your-key-here

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=false
ENVIRONMENT=production

# CORS Settings
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,https://yourdomain.com

# File Upload Settings
MAX_FILE_SIZE_MB=10
UPLOAD_DIR=uploads
PROCESSED_DIR=processed

# Session Settings
SESSION_TIMEOUT_HOURS=24
MAX_CONCURRENT_SESSIONS=100

# Rate Limiting
RATE_LIMIT_PER_MINUTE=10
RATE_LIMIT_PER_HOUR=100

# Processing
MAX_CONCURRENT_PROCESSING=3
PROCESSING_TIMEOUT_SECONDS=300

# Logging
LOG_LEVEL=INFO
LOG_FILE=api.log
```

---

#### **3. Dockerfile**

```dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ghostscript \
    python3-tk \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create necessary directories
RUN mkdir -p uploads processed logs

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/api/v1/health || exit 1

# Run FastAPI with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
```

---

#### **4. docker-compose.yml**

```yaml
version: '3.8'

services:
  api:
    build: .
    container_name: research_paper_api
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - HOST=0.0.0.0
      - PORT=8000
      - DEBUG=false
    volumes:
      - ./uploads:/app/uploads
      - ./processed:/app/processed
      - ./logs:/app/logs
    restart: unless-stopped
    networks:
      - app-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/v1/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Optional: Redis for caching (future use)
  # redis:
  #   image: redis:7-alpine
  #   container_name: research_paper_redis
  #   ports:
  #     - "6379:6379"
  #   networks:
  #     - app-network

networks:
  app-network:
    driver: bridge
```

---

## 🚀 Deployment Options

### **Option 1: Docker (Local/VPS)** ⭐

**Steps:**

1. **Build and run:**
```bash
# Clone/navigate to project
cd stage5_backend

# Create .env file
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# Build and start
docker-compose up -d

# Check logs
docker-compose logs -f

# Access API
curl http://localhost:8000/api/v1/health
```

2. **Access:**
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

3. **Stop:**
```bash
docker-compose down
```

**Cost:** $5-10/month (DigitalOcean, Linode, Hetzner)

---

### **Option 2: Railway** ⭐ (Easiest)

**Steps:**

1. **Push to GitHub:**
```bash
git init
git add .
git commit -m "Stage 5 FastAPI backend"
git push origin main
```

2. **Deploy on Railway:**
- Go to [railway.app](https://railway.app)
- Connect GitHub repo
- Add environment variables (OPENAI_API_KEY)
- Deploy automatically

3. **Get URL:**
```
https://your-app.railway.app
```

**Cost:** Free tier (500 hours/month), then $5/month

---

### **Option 3: Render**

**Steps:**

1. **Create `render.yaml`:**
```yaml
services:
  - type: web
    name: research-paper-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: OPENAI_API_KEY
        sync: false
      - key: PYTHON_VERSION
        value: 3.11.0
```

2. **Deploy:**
- Connect GitHub to Render
- Add environment variables
- Deploy

**Cost:** Free tier (750 hours), then $7/month

---

### **Option 4: AWS (Production)**

**Using EC2 + Docker:**

```bash
# SSH into EC2 instance
ssh -i key.pem ubuntu@your-ec2-ip

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Clone repo
git clone your-repo
cd your-repo

# Run with docker-compose
docker-compose up -d
```

**Cost:** $10-50/month depending on instance size

---

### **Option 5: Local + ngrok** (Testing)

**For public access to local server:**

```bash
# Start API locally
uvicorn app.main:app --reload

# In another terminal, expose with ngrok
ngrok http 8000

# Get public URL
https://abc123.ngrok.io
```

**Cost:** Free (with ngrok limits)

---

## 🧪 Testing

### **Manual Testing**

```bash
# Health check
curl http://localhost:8000/api/v1/health

# Upload PDF
curl -X POST http://localhost:8000/api/v1/upload \
  -F "file=@research_paper.pdf"

# Get paper info (use paper_id from upload response)
curl http://localhost:8000/api/v1/papers/{paper_id}

# Chat
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "paper_id": "your-paper-id",
    "question": "What is this paper about?"
  }'
```

### **Automated Testing**

Create `tests/test_api.py`:

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_upload():
    with open("test.pdf", "rb") as f:
        response = client.post(
            "/api/v1/upload",
            files={"file": ("test.pdf", f, "application/pdf")}
        )
    assert response.status_code == 200
    assert "paper_id" in response.json()

# Run with: pytest tests/
```

---

## 📊 Monitoring

### **Logging**

```python
# app/utils/logger.py
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/api.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

### **Request Logging**

```python
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = datetime.now()
    logger.info(f"Request: {request.method} {request.url}")
    
    response = await call_next(request)
    
    duration = (datetime.now() - start_time).total_seconds()
    logger.info(f"Response: {response.status_code} ({duration:.2f}s)")
    
    return response
```

### **Health Metrics**

```python
from prometheus_client import Counter, Histogram

request_count = Counter('http_requests_total', 'Total HTTP requests')
request_duration = Histogram('http_request_duration_seconds', 'HTTP request duration')
```

---

## 📈 Performance

### **Optimization Tips**

1. **Caching:**
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_paper_data(paper_id: str):
    # Cache frequent requests
    pass
```

2. **Background Tasks:**
```python
from fastapi import BackgroundTasks

@app.post("/process")
async def process(paper_id: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(process_paper, paper_id)
    return {"status": "processing"}
```

3. **Connection Pooling:**
```python
# Reuse vector stores
class VectorStorePool:
    def __init__(self):
        self.stores = {}
```

---

## 🎯 Next Steps

After Stage 5:
1. ✅ Your API is production-ready
2. ✅ Can handle multiple users
3. ✅ Deployed and accessible
4. ✅ Ready for Stage 6 (Advanced features)

**Success Metrics:**
- API responds in <2 seconds
- Handles 10+ concurrent users
- 99%+ uptime
- Auto-restarts on failure

---

## 💡 Troubleshooting

**Issue:** Port already in use
```bash
# Find process on port 8000
lsof -i :8000
# Kill it
kill -9 <PID>
```

**Issue:** Docker build fails
```bash
# Clear cache and rebuild
docker-compose build --no-cache
```

**Issue:** Vector store not found
```bash
# Ensure vectorstore_multimodal exists
ls -la vectorstore_multimodal/
```

---

## ✅ Checklist

Before deploying:
- [ ] Environment variables set
- [ ] OPENAI_API_KEY configured
- [ ] Docker working
- [ ] Health endpoint responding
- [ ] Upload tested
- [ ] Chat tested
- [ ] Logs accessible
- [ ] Backups configured

---

**🎉 Stage 5 Complete!**

You now have a production-ready REST API that can:
- Handle multiple users
- Process papers automatically
- Chat with papers
- Scale horizontally
- Deploy anywhere

**Ready for Stage 6?** Advanced features await! 🚀
