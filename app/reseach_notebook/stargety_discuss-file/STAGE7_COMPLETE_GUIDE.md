# 🌐 STAGE 7: Production Web App + Full Deployment
## Enterprise-Ready Application with User Management & Monitoring

---

## 📋 Table of Contents
1. [Overview](#overview)
2. [Web Application](#web-application)
3. [User Management](#user-management)
4. [Database Architecture](#database-architecture)
5. [Authentication & Security](#authentication-security)
6. [Payment Integration](#payment-integration)
7. [Production Infrastructure](#production-infrastructure)
8. [Monitoring & Observability](#monitoring-observability)
9. [CI/CD Pipeline](#cicd-pipeline)

---

## 🎯 Overview

**What Stage 7 Delivers:**
- 🌐 Professional web application (React/Vue/Streamlit)
- 👥 Multi-user accounts & authentication
- 💾 PostgreSQL database for data persistence
- 💳 Payment system (optional)
- 🚀 Production infrastructure (auto-scaling)
- 📈 Full monitoring & observability
- 🔄 Automated CI/CD pipeline
- 🔐 Enterprise security features

**Time to Build:** 4-6 weeks  
**Difficulty:** Expert  
**Prerequisites:** Stages 1-6 complete

---

## 🌐 1. Web Application

### **Architecture:**

```
┌─────────────────────────────────────────┐
│         FRONTEND APPLICATION            │
│                                         │
│  ┌──────────────────────────────────┐  │
│  │     React/Next.js (Primary)      │  │
│  │  or Vue/Nuxt (Alternative)       │  │
│  │  or Streamlit (Quick Deploy)     │  │
│  └──────────────────────────────────┘  │
│                                         │
│  Components:                            │
│  ├─ Dashboard (Paper library)           │
│  ├─ Upload Interface                    │
│  ├─ Chat Interface                      │
│  ├─ Search & Filters                    │
│  ├─ Analytics Dashboard                 │
│  ├─ Settings                            │
│  └─ Admin Panel                         │
└──────────────┬──────────────────────────┘
               │ REST API (HTTPS)
               ↓
┌─────────────────────────────────────────┐
│         BACKEND (FastAPI)               │
└─────────────────────────────────────────┘
```

---

### **Option A: React + Next.js** ⭐ (Recommended)

**Tech Stack:**
- **Framework:** Next.js 14 (App Router)
- **UI:** Tailwind CSS + shadcn/ui
- **State:** Zustand or Redux Toolkit
- **Forms:** React Hook Form + Zod
- **Charts:** Recharts or Chart.js
- **File Upload:** react-dropzone

**Project Structure:**
```
frontend/
├── app/
│   ├── (auth)/
│   │   ├── login/page.tsx
│   │   └── signup/page.tsx
│   ├── (dashboard)/
│   │   ├── layout.tsx
│   │   ├── page.tsx              # Dashboard
│   │   ├── papers/
│   │   │   ├── page.tsx          # Paper list
│   │   │   └── [id]/
│   │   │       ├── page.tsx      # Paper detail
│   │   │       └── chat/page.tsx # Chat interface
│   │   ├── upload/page.tsx
│   │   ├── analytics/page.tsx
│   │   └── settings/page.tsx
│   ├── api/                      # API routes (if needed)
│   └── layout.tsx
├── components/
│   ├── ui/                       # shadcn components
│   ├── chat/
│   │   ├── ChatInterface.tsx
│   │   ├── MessageBubble.tsx
│   │   └── SourceCard.tsx
│   ├── papers/
│   │   ├── PaperCard.tsx
│   │   ├── PaperGrid.tsx
│   │   └── UploadZone.tsx
│   └── analytics/
│       └── ChartsContainer.tsx
├── lib/
│   ├── api.ts                    # API client
│   ├── auth.ts                   # Auth helpers
│   └── utils.ts
├── hooks/
│   ├── usePapers.ts
│   ├── useChat.ts
│   └── useAuth.ts
└── types/
    └── index.ts
```

**Key Pages:**

**1. Dashboard:**
```typescript
// app/(dashboard)/page.tsx
export default function Dashboard() {
  return (
    <div className="space-y-6">
      <Stats />  {/* Paper count, active chats, etc. */}
      <RecentPapers />
      <QuickActions />
    </div>
  )
}
```

**2. Paper Library:**
```typescript
// app/(dashboard)/papers/page.tsx
export default function Papers() {
  const { papers, loading } = usePapers()
  
  return (
    <div>
      <SearchBar />
      <Filters />
      <PaperGrid papers={papers} />
      <Pagination />
    </div>
  )
}
```

**3. Chat Interface:**
```typescript
// app/(dashboard)/papers/[id]/chat/page.tsx
export default function Chat({ params }: { params: { id: string } }) {
  const { messages, sendMessage, loading } = useChat(params.id)
  
  return (
    <div className="flex flex-col h-screen">
      <PaperHeader paperId={params.id} />
      <MessageList messages={messages} />
      <ChatInput onSend={sendMessage} loading={loading} />
    </div>
  )
}
```

---

### **Option B: Vue.js + Nuxt 3**

**Similar structure, Vue syntax:**
```vue
<!-- pages/papers/[id]/chat.vue -->
<template>
  <div class="chat-container">
    <MessageList :messages="messages" />
    <ChatInput @send="handleSend" />
  </div>
</template>

<script setup lang="ts">
const route = useRoute()
const { messages, sendMessage } = useChat(route.params.id)
</script>
```

---

### **Option C: Streamlit (Quickest)**

```python
import streamlit as st
from api_client import ResearchPaperAPI

# Sidebar
st.sidebar.title("📚 Research Papers")
papers = api.get_papers()
selected_paper = st.sidebar.selectbox("Select Paper", papers)

# Main area
st.title(f"Chat with {selected_paper['title']}")

# Chat interface
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input
if prompt := st.chat_input("Ask a question"):
    response = api.chat(selected_paper['id'], prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})
```

---

## 👥 2. User Management

### **Features:**

#### **2.1 User Accounts**

**Database Schema:**
```sql
CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    avatar_url TEXT,
    role VARCHAR(50) DEFAULT 'user', -- 'user', 'admin', 'team_admin'
    plan VARCHAR(50) DEFAULT 'free', -- 'free', 'pro', 'team', 'enterprise'
    
    -- Limits
    papers_uploaded INTEGER DEFAULT 0,
    papers_limit INTEGER DEFAULT 5,
    api_calls_count INTEGER DEFAULT 0,
    api_calls_limit INTEGER DEFAULT 1000,
    
    -- Status
    email_verified BOOLEAN DEFAULT false,
    is_active BOOLEAN DEFAULT true,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP
);

CREATE TABLE teams (
    team_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    owner_id UUID REFERENCES users(user_id),
    plan VARCHAR(50) DEFAULT 'team',
    seats INTEGER DEFAULT 5,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE team_members (
    id SERIAL PRIMARY KEY,
    team_id UUID REFERENCES teams(team_id),
    user_id UUID REFERENCES users(user_id),
    role VARCHAR(50) DEFAULT 'member', -- 'owner', 'admin', 'member'
    joined_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(team_id, user_id)
);
```

---

#### **2.2 Registration Flow**

**API Endpoints:**

```python
# Register
POST /api/v1/auth/register
Body: {
  "email": "user@example.com",
  "password": "secure_password",
  "full_name": "John Doe"
}

Response: {
  "user_id": "uuid",
  "email": "user@example.com",
  "message": "Verification email sent"
}

# Verify email
GET /api/v1/auth/verify?token=verification_token

# Login
POST /api/v1/auth/login
Body: {
  "email": "user@example.com",
  "password": "secure_password"
}

Response: {
  "access_token": "jwt_token",
  "refresh_token": "refresh_jwt",
  "user": {
    "user_id": "uuid",
    "email": "user@example.com",
    "plan": "pro"
  }
}
```

**Implementation:**
```python
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)
    
    def verify_password(self, plain: str, hashed: str) -> bool:
        return pwd_context.verify(plain, hashed)
    
    def create_access_token(self, user_id: str) -> str:
        expires = datetime.utcnow() + timedelta(hours=24)
        to_encode = {"sub": user_id, "exp": expires}
        return jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    
    async def register(self, email: str, password: str, full_name: str):
        # 1. Check if user exists
        if await self.get_user_by_email(email):
            raise ValueError("Email already registered")
        
        # 2. Hash password
        password_hash = self.hash_password(password)
        
        # 3. Create user
        user = await db.users.create({
            "email": email,
            "password_hash": password_hash,
            "full_name": full_name
        })
        
        # 4. Send verification email
        await send_verification_email(user.email, user.user_id)
        
        return user
```

---

#### **2.3 OAuth Integration**

**Google OAuth:**
```python
from authlib.integrations.starlette_client import OAuth

oauth = OAuth()
oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

@app.get('/auth/google')
async def google_login(request: Request):
    redirect_uri = request.url_for('google_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@app.get('/auth/google/callback')
async def google_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user_info = token['userinfo']
    
    # Create or get user
    user = await get_or_create_user(user_info['email'], user_info['name'])
    
    # Create session
    access_token = create_access_token(user.user_id)
    return {"access_token": access_token}
```

---

## 💾 3. Database Architecture

### **Complete Schema:**

```sql
-- Users (already shown above)

-- Papers
CREATE TABLE papers (
    paper_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id),
    team_id UUID REFERENCES teams(team_id),
    
    -- File info
    filename VARCHAR(255) NOT NULL,
    file_path TEXT NOT NULL,
    file_size_bytes BIGINT,
    
    -- Metadata
    title TEXT,
    authors TEXT[],
    publication_date DATE,
    pages INTEGER,
    
    -- Processing
    processing_status VARCHAR(50) DEFAULT 'pending',
    stage1_completed BOOLEAN DEFAULT false,
    stage2_completed BOOLEAN DEFAULT false,
    stage3_completed BOOLEAN DEFAULT false,
    
    -- Content
    tldr TEXT,
    simplified_content JSONB,
    
    -- Organization
    tags TEXT[],
    collection_id UUID,
    
    -- Timestamps
    uploaded_at TIMESTAMP DEFAULT NOW(),
    processed_at TIMESTAMP,
    
    -- Access control
    is_public BOOLEAN DEFAULT false,
    shared_with UUID[]
);

-- Chat Sessions
CREATE TABLE chat_sessions (
    session_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    paper_id UUID REFERENCES papers(paper_id),
    user_id UUID REFERENCES users(user_id),
    created_at TIMESTAMP DEFAULT NOW(),
    last_message_at TIMESTAMP,
    message_count INTEGER DEFAULT 0
);

-- Chat Messages
CREATE TABLE chat_messages (
    message_id SERIAL PRIMARY KEY,
    session_id UUID REFERENCES chat_sessions(session_id),
    role VARCHAR(50) NOT NULL, -- 'user' or 'assistant'
    content TEXT NOT NULL,
    sources JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Collections
CREATE TABLE collections (
    collection_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id),
    team_id UUID REFERENCES teams(team_id),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Usage Tracking
CREATE TABLE usage_logs (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(user_id),
    action VARCHAR(100) NOT NULL, -- 'paper_upload', 'chat_message', 'export'
    paper_id UUID,
    cost_credits DECIMAL(10, 4),
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- API Keys (for programmatic access)
CREATE TABLE api_keys (
    key_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id),
    key_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    last_used_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP,
    is_active BOOLEAN DEFAULT true
);
```

**Indexes:**
```sql
CREATE INDEX idx_papers_user_id ON papers(user_id);
CREATE INDEX idx_papers_status ON papers(processing_status);
CREATE INDEX idx_chat_sessions_paper ON chat_sessions(paper_id);
CREATE INDEX idx_chat_messages_session ON chat_messages(session_id);
CREATE INDEX idx_usage_logs_user_date ON usage_logs(user_id, created_at);
```

---

## 🔐 4. Authentication & Security

### **4.1 JWT-based Authentication**

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    token = credentials.credentials
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("sub")
        
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        user = await get_user(user_id)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        
        return user
        
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Protected route
@app.get("/api/v1/papers")
async def get_papers(user: User = Depends(get_current_user)):
    return await db.papers.find({"user_id": user.user_id})
```

---

### **4.2 Rate Limiting**

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Different limits for different plans
@app.post("/api/v1/chat")
@limiter.limit("10/minute")  # Free tier
async def chat_free(request: Request, user: User = Depends(get_current_user)):
    if user.plan == "pro":
        # Pro users get higher limit
        pass
    return await process_chat(request)

# Custom rate limit based on user plan
def get_rate_limit(user: User) -> str:
    limits = {
        "free": "10/minute",
        "pro": "100/minute",
        "team": "500/minute",
        "enterprise": "unlimited"
    }
    return limits.get(user.plan, "10/minute")
```

---

### **4.3 Input Validation**

```python
from pydantic import BaseModel, validator, Field

class ChatRequest(BaseModel):
    paper_id: UUID
    question: str = Field(..., min_length=1, max_length=1000)
    session_id: Optional[UUID] = None
    
    @validator('question')
    def sanitize_question(cls, v):
        # Remove potentially harmful characters
        import re
        v = re.sub(r'[<>{}]', '', v)
        return v.strip()
    
    @validator('paper_id')
    def validate_paper_access(cls, v, values):
        # Check if user has access to this paper
        # (done in endpoint with current_user)
        return v
```

---

### **4.4 CORS Configuration**

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Local dev
        "https://app.yourdomain.com"  # Production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 💳 5. Payment Integration (Optional)

### **5.1 Stripe Integration**

**Plans:**
```python
PLANS = {
    "free": {
        "price": 0,
        "papers_limit": 5,
        "api_calls_limit": 1000,
        "features": ["Basic chat", "5 papers"]
    },
    "pro": {
        "price": 9,  # per month
        "stripe_price_id": "price_xxx",
        "papers_limit": 100,
        "api_calls_limit": 50000,
        "features": ["Advanced chat", "100 papers", "Export", "Priority support"]
    },
    "team": {
        "price": 29,
        "stripe_price_id": "price_yyy",
        "papers_limit": -1,  # unlimited
        "api_calls_limit": 500000,
        "seats": 5,
        "features": ["Everything in Pro", "Team workspace", "Shared papers"]
    }
}
```

**Endpoints:**
```python
import stripe

stripe.api_key = STRIPE_SECRET_KEY

@app.post("/api/v1/billing/create-checkout")
async def create_checkout(
    plan: str,
    user: User = Depends(get_current_user)
):
    session = stripe.checkout.Session.create(
        customer_email=user.email,
        payment_method_types=['card'],
        line_items=[{
            'price': PLANS[plan]['stripe_price_id'],
            'quantity': 1,
        }],
        mode='subscription',
        success_url='https://app.yourdomain.com/success',
        cancel_url='https://app.yourdomain.com/cancel',
        metadata={'user_id': str(user.user_id), 'plan': plan}
    )
    return {"checkout_url": session.url}

@app.post("/api/v1/webhooks/stripe")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')
    
    event = stripe.Webhook.construct_event(
        payload, sig_header, STRIPE_WEBHOOK_SECRET
    )
    
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        user_id = session['metadata']['user_id']
        plan = session['metadata']['plan']
        
        # Upgrade user
        await upgrade_user_plan(user_id, plan)
    
    return {"status": "success"}
```

---

## 🚀 6. Production Infrastructure

### **6.1 Architecture Diagram**

```
Internet
    ↓
┌─────────────────────────────────────────┐
│    CDN (Cloudflare/CloudFront)          │
│    • Static assets                      │
│    • DDoS protection                    │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│    Load Balancer (ALB/nginx)            │
│    • SSL termination                    │
│    • Request routing                    │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│    Frontend (Vercel/Netlify)            │
│    ├─ Next.js app                       │
│    └─ Auto-scaling                      │
└─────────────────────────────────────────┘
               ↓ API calls
┌─────────────────────────────────────────┐
│    API Gateway                          │
│    • Rate limiting                      │
│    • Authentication                     │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│    Backend Servers (Auto-scaling)       │
│    ├─ FastAPI instances (2-10)          │
│    ├─ Docker containers                 │
│    └─ Health checks                     │
└──────────────┬──────────────────────────┘
               ↓
┌──────────────────────────┬──────────────┐
│   Database Layer         │ Cache Layer  │
├──────────────────────────┼──────────────┤
│ PostgreSQL (Primary)     │ Redis        │
│ PostgreSQL (Replica)     │ • Sessions   │
│ • User data              │ • Rate limit │
│ • Papers                 │ • Cache      │
│ • Chat history           │              │
└──────────────────────────┴──────────────┘
               ↓
┌─────────────────────────────────────────┐
│    Storage Layer                        │
├─────────────────────────────────────────┤
│ S3/R2 (Object Storage)                  │
│ ├─ PDF files                            │
│ ├─ Vector stores                        │
│ └─ Exports                              │
└─────────────────────────────────────────┘
```

---

### **6.2 Docker Configuration**

**Production Dockerfile:**
```dockerfile
# Multi-stage build
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    ghostscript \
    && rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy application
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:8000/api/v1/health || exit 1

# Run
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

**docker-compose.prod.yml:**
```yaml
version: '3.8'

services:
  api:
    build:
      context: .
      dockerfile: Dockerfile
    image: research-paper-api:latest
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '2'
          memory: 4G
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/research
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
    networks:
      - app-network

  db:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    networks:
      - app-network

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    networks:
      - app-network

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - api
    networks:
      - app-network

volumes:
  postgres_data:
  redis_data:

networks:
  app-network:
    driver: bridge
```

---

### **6.3 Kubernetes Deployment (Optional)**

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: research-paper-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: research-paper-api
  template:
    metadata:
      labels:
        app: research-paper-api
    spec:
      containers:
      - name: api
        image: your-registry/research-paper-api:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
        livenessProbe:
          httpGet:
            path: /api/v1/health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: research-paper-api
spec:
  selector:
    app: research-paper-api
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
```

---

## 📈 7. Monitoring & Observability

### **7.1 Metrics Collection**

**Prometheus Integration:**
```python
from prometheus_client import Counter, Histogram, Gauge, make_asgi_app

# Metrics
request_count = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

request_duration = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint']
)

active_users = Gauge(
    'active_users_total',
    'Number of active users'
)

# Middleware
@app.middleware("http")
async def track_metrics(request: Request, call_next):
    start_time = time.time()
    
    response = await call_next(request)
    
    duration = time.time() - start_time
    
    request_count.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()
    
    request_duration.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(duration)
    
    return response

# Expose metrics
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)
```

---

### **7.2 Logging**

**Structured Logging:**
```python
import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
        }
        
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_data)

# Setup
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())

logger = logging.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.INFO)
```

---

### **7.3 Error Tracking (Sentry)**

```python
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FastApiIntegration()],
    environment="production",
    traces_sample_rate=0.1,  # 10% of transactions
)

# Errors automatically captured
# Manual capture:
try:
    process_paper(paper_id)
except Exception as e:
    sentry_sdk.capture_exception(e)
    raise
```

---

### **7.4 Grafana Dashboards**

**Example Dashboard Queries:**
```promql
# Request rate
rate(http_requests_total[5m])

# Error rate
rate(http_requests_total{status=~"5.."}[5m])

# Response time (95th percentile)
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# Active users
active_users_total

# Papers processed per hour
rate(papers_processed_total[1h])
```

---

## 🔄 8. CI/CD Pipeline

### **8.1 GitHub Actions**

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest
      
      - name: Run tests
        run: pytest tests/
  
  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build Docker image
        run: |
          docker build -t research-paper-api:${{ github.sha }} .
          docker tag research-paper-api:${{ github.sha }} research-paper-api:latest
      
      - name: Push to registry
        run: |
          echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
          docker push research-paper-api:latest
  
  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.PROD_HOST }}
          username: ${{ secrets.PROD_USER }}
          key: ${{ secrets.SSH_KEY }}
          script: |
            cd /app
            docker-compose pull
            docker-compose up -d
            docker system prune -f
```

---

## 💰 9. Cost Breakdown

**Monthly Costs (Estimated):**

| Service | Tier | Cost |
|---------|------|------|
| **Hosting** |
| Frontend (Vercel) | Pro | $20 |
| Backend (Railway/Render) | Pro | $25 |
| Database (PostgreSQL) | 4GB | $15 |
| Redis | 1GB | $10 |
| **Storage** |
| S3/R2 (100GB) | Standard | $5 |
| **CDN** |
| Cloudflare | Pro | $20 |
| **Monitoring** |
| Sentry | Team | $26 |
| Grafana Cloud | Free | $0 |
| **Email** |
| SendGrid | Essentials | $15 |
| **Payment** |
| Stripe | % of revenue | Variable |
| **TOTAL** | | **~$136/month** |

**Revenue Breakeven:**
- 15 Pro users ($9/mo) = $135
- 5 Team users ($29/mo) = $145

---

## ✅ Stage 7 Checklist

**Infrastructure:**
- [ ] Frontend deployed (Vercel/Netlify)
- [ ] Backend deployed (Railway/Render/AWS)
- [ ] Database setup (PostgreSQL)
- [ ] Redis cache configured
- [ ] S3/R2 storage setup
- [ ] SSL certificates installed
- [ ] Custom domain configured

**Features:**
- [ ] User registration/login
- [ ] OAuth (Google/GitHub)
- [ ] Paper upload & processing
- [ ] Chat interface
- [ ] Search & filters
- [ ] Analytics dashboard
- [ ] Admin panel

**Security:**
- [ ] Rate limiting enabled
- [ ] CORS configured
- [ ] Input validation
- [ ] SQL injection protection
- [ ] XSS protection
- [ ] CSRF tokens
- [ ] Security headers

**Monitoring:**
- [ ] Prometheus metrics
- [ ] Grafana dashboards
- [ ] Sentry error tracking
- [ ] Log aggregation
- [ ] Uptime monitoring
- [ ] Alerts configured

**Performance:**
- [ ] CDN enabled
- [ ] Database indexes
- [ ] Redis caching
- [ ] Image optimization
- [ ] Lazy loading
- [ ] Code splitting

**Payment (if applicable):**
- [ ] Stripe integration
- [ ] Subscription plans
- [ ] Webhook handling
- [ ] Invoice generation

---

## 🎉 Success!

**With Stage 7 complete, you have:**
- ✅ Production-ready web application
- ✅ Multi-user support
- ✅ Payment processing
- ✅ Full monitoring
- ✅ Auto-scaling infrastructure
- ✅ Enterprise-grade security

**Your Research Paper Simplifier is now a complete SaaS product!** 🚀

**Next Steps:**
- Launch to beta users
- Gather feedback
- Iterate on features
- Scale as needed

**Congratulations on building an amazing product!** 🎊
