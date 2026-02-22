# 💡 STAGE 6: Advanced Features & Optimization
## Multi-Paper Management, Advanced RAG, Export & Analytics

---

## 📋 Table of Contents
1. [Overview](#overview)
2. [Multi-Paper Management](#multi-paper-management)
3. [Advanced RAG Features](#advanced-rag-features)
4. [Export & Sharing](#export-sharing)
5. [Batch Processing](#batch-processing)
6. [Analytics & Insights](#analytics-insights)
7. [Personalization](#personalization)
8. [Integrations](#integrations)

---

## 🎯 Overview

**What Stage 6 Adds:**
- 📚 Manage library of multiple papers
- 🔍 Advanced search and retrieval
- 📤 Export in multiple formats
- ⚡ Batch processing capabilities
- 📊 Analytics and visualizations
- 🎨 Personalization options
- 🔌 Third-party integrations

**Time to Build:** 2-3 weeks  
**Difficulty:** Advanced  
**Prerequisites:** Stages 1-5 complete

---

## 📚 1. Multi-Paper Management

### **Current State:**
```
One paper at a time
Manual switching
No comparison
```

### **Stage 6:**
```
Paper library
Collections/folders
Compare papers
Search across all
Recommendations
```

### **Features:**

#### **1.1 Paper Library**

**Database Schema:**
```sql
CREATE TABLE papers (
    paper_id UUID PRIMARY KEY,
    filename VARCHAR(255),
    title TEXT,
    authors TEXT[],
    publication_date DATE,
    pages INTEGER,
    upload_date TIMESTAMP,
    processing_status VARCHAR(50),
    tags TEXT[],
    collection_id UUID,
    metadata JSONB
);

CREATE TABLE collections (
    collection_id UUID PRIMARY KEY,
    name VARCHAR(255),
    description TEXT,
    created_at TIMESTAMP,
    paper_count INTEGER
);

CREATE TABLE paper_relations (
    id SERIAL PRIMARY KEY,
    paper_id_1 UUID,
    paper_id_2 UUID,
    relation_type VARCHAR(50), -- 'cites', 'related', 'compares'
    strength FLOAT
);
```

**API Endpoints:**

```python
# List all papers
GET /api/v1/papers
Query params: ?tags=AI,ML&collection=uuid&sort=date&order=desc

# Create collection
POST /api/v1/collections
Body: {"name": "AI Papers", "description": "..."}

# Add papers to collection
POST /api/v1/collections/{id}/papers
Body: {"paper_ids": ["uuid1", "uuid2"]}

# Search across library
GET /api/v1/search?q=machine learning&papers=all
```

**Example Response:**
```json
{
  "papers": [
    {
      "paper_id": "uuid-1",
      "title": "GenAI in Architecture",
      "authors": ["Memon et al."],
      "tags": ["AI", "Architecture", "Construction"],
      "upload_date": "2024-02-20",
      "similarity_score": 0.95
    }
  ],
  "total": 45,
  "collections": 3
}
```

---

#### **1.2 Paper Comparison**

**Compare 2+ papers side-by-side:**

```python
POST /api/v1/compare
Body: {
  "paper_ids": ["uuid-1", "uuid-2", "uuid-3"],
  "aspects": ["methodology", "findings", "limitations"]
}

Response: {
  "comparison": {
    "methodology": {
      "uuid-1": "Systematic literature review",
      "uuid-2": "Experimental study",
      "uuid-3": "Case study analysis"
    },
    "findings": {
      "common": ["AI improves efficiency", "Need for more research"],
      "unique": {
        "uuid-1": ["7 themes identified"],
        "uuid-2": ["30% productivity gain"]
      }
    },
    "summary": "All three papers focus on AI applications..."
  }
}
```

**Visualization:**
```
┌─────────────────────────────────────────┐
│  Paper Comparison Matrix                │
├─────────────┬──────────┬───────────────┤
│             │ Paper 1  │ Paper 2       │
├─────────────┼──────────┼───────────────┤
│ Method      │ Review   │ Experimental  │
│ Sample Size │ 28       │ 150           │
│ Findings    │ 7 themes │ 30% gain      │
│ Year        │ 2024     │ 2023          │
└─────────────┴──────────┴───────────────┘
```

---

#### **1.3 Smart Recommendations**

**Recommend related papers:**

```python
GET /api/v1/papers/{paper_id}/recommendations

Response: {
  "recommendations": [
    {
      "paper_id": "uuid-2",
      "title": "AI in Construction: A Review",
      "relevance_score": 0.89,
      "reasons": [
        "Similar topic (Construction + AI)",
        "Cites 5 common papers",
        "Same methodology (systematic review)"
      ]
    }
  ]
}
```

**Algorithm:**
```python
def recommend_papers(paper_id):
    # 1. Get paper's embeddings
    paper_embedding = get_paper_embedding(paper_id)
    
    # 2. Find similar embeddings
    similar = vectorstore.similarity_search(paper_embedding, k=10)
    
    # 3. Check citations
    shared_citations = find_shared_citations(paper_id)
    
    # 4. Topic overlap
    topic_similarity = compute_topic_overlap(paper_id)
    
    # 5. Combine scores
    return rank_recommendations([similar, shared_citations, topic_similarity])
```

---

## 🔍 2. Advanced RAG Features

### **Current State:**
```
Basic similarity search
Single retrieval strategy
No re-ranking
```

### **Stage 6:**
```
Hybrid search (keyword + semantic)
Re-ranking for relevance
Query expansion
Multi-hop reasoning
Citation-aware retrieval
```

### **Features:**

#### **2.1 Hybrid Search**

**Combine BM25 (keyword) + Vector (semantic):**

```python
from rank_bm25 import BM25Okapi

class HybridRetriever:
    def __init__(self, vectorstore, documents):
        self.vectorstore = vectorstore
        # Build BM25 index
        tokenized_docs = [doc.split() for doc in documents]
        self.bm25 = BM25Okapi(tokenized_docs)
    
    def search(self, query: str, k: int = 5):
        # 1. BM25 search (keyword matching)
        bm25_scores = self.bm25.get_scores(query.split())
        bm25_results = np.argsort(bm25_scores)[-k:]
        
        # 2. Vector search (semantic)
        vector_results = self.vectorstore.similarity_search(query, k=k)
        
        # 3. Combine with weights
        hybrid_results = self.combine_results(
            bm25_results, 
            vector_results,
            weights=[0.3, 0.7]  # 30% keyword, 70% semantic
        )
        
        return hybrid_results
```

**API:**
```python
POST /api/v1/search/hybrid
Body: {
  "query": "machine learning applications",
  "papers": ["uuid-1", "uuid-2"],
  "weights": {"keyword": 0.3, "semantic": 0.7}
}
```

---

#### **2.2 Re-Ranking**

**Use cross-encoder for better ranking:**

```python
from sentence_transformers import CrossEncoder

class ReRanker:
    def __init__(self):
        self.model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
    
    def rerank(self, query: str, documents: List[str], top_k: int = 5):
        # Score each doc against query
        pairs = [[query, doc] for doc in documents]
        scores = self.model.predict(pairs)
        
        # Sort by score
        ranked = sorted(
            zip(documents, scores),
            key=lambda x: x[1],
            reverse=True
        )
        
        return ranked[:top_k]
```

**Before vs After:**
```
Before (Vector only):
1. "AI in construction" (score: 0.75)
2. "Machine learning basics" (score: 0.73)
3. "AI applications in architecture" (score: 0.71)

After (Re-ranked):
1. "AI applications in architecture" (score: 0.91) ⬆️
2. "AI in construction" (score: 0.85)
3. "Machine learning basics" (score: 0.62) ⬇️
```

---

#### **2.3 Query Expansion**

**Understand vague questions:**

```python
class QueryExpander:
    def expand(self, query: str) -> List[str]:
        # 1. Synonyms
        synonyms = self.get_synonyms(query)
        
        # 2. Related terms (from LLM)
        related = self.llm.generate(
            f"Generate 5 related search terms for: {query}"
        )
        
        # 3. Acronym expansion
        acronyms = self.expand_acronyms(query)
        
        return [query] + synonyms + related + acronyms

# Example
query = "What is GenAI?"
expanded = [
    "What is GenAI?",
    "What is Generative AI?",
    "What is Generative Artificial Intelligence?",
    "GenAI applications",
    "GenAI definition"
]
```

---

#### **2.4 Multi-Hop Reasoning**

**Answer complex questions requiring multiple steps:**

```python
Question: "Compare the findings of papers about AI in construction vs architecture"

Step 1: Identify papers
  → Find papers tagged "construction"
  → Find papers tagged "architecture"

Step 2: Extract findings from each
  → Get "findings" section from construction papers
  → Get "findings" section from architecture papers

Step 3: Compare
  → Identify commonalities
  → Identify differences
  → Generate comparison summary

Answer: "Construction papers focus on X, while architecture papers emphasize Y..."
```

---

#### **2.5 Citation-Aware Retrieval**

**Prioritize frequently cited content:**

```python
class CitationAwareRetriever:
    def search(self, query: str, k: int = 5):
        # 1. Regular similarity search
        results = self.vectorstore.similarity_search(query, k=k*2)
        
        # 2. Boost by citation count
        for result in results:
            # Check how many times this chunk is referenced
            citations = self.count_citations(result.metadata['chunk_id'])
            result.score *= (1 + 0.1 * citations)  # Boost by 10% per citation
        
        # 3. Re-sort and return top k
        return sorted(results, key=lambda x: x.score, reverse=True)[:k]
```

---

## 📤 3. Export & Sharing

### **Features:**

#### **3.1 Export Simplified Paper**

**Generate PDF/DOCX from simplified version:**

```python
POST /api/v1/papers/{paper_id}/export
Body: {
  "format": "pdf",  # or "docx", "html", "markdown"
  "sections": ["tldr", "summary", "findings", "critique"],
  "include_sources": true
}

Response: {
  "download_url": "https://api.com/downloads/simplified_paper.pdf",
  "expires_at": "2024-02-23T12:00:00Z"
}
```

**PDF Generation:**
```python
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

def generate_pdf(paper_data, output_path):
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    story = []
    
    # Title
    story.append(Paragraph(f"<b>{paper_data['title']}</b>", title_style))
    story.append(Spacer(1, 12))
    
    # TL;DR
    story.append(Paragraph("<b>TL;DR:</b>", heading_style))
    story.append(Paragraph(paper_data['tldr'], body_style))
    
    # ... add more sections
    
    doc.build(story)
```

**DOCX Generation:**
```python
from docx import Document

def generate_docx(paper_data, output_path):
    doc = Document()
    
    # Title
    doc.add_heading(paper_data['title'], 0)
    
    # TL;DR
    doc.add_heading('TL;DR', 1)
    doc.add_paragraph(paper_data['tldr'])
    
    # Findings
    doc.add_heading('Key Findings', 1)
    for finding in paper_data['findings']:
        doc.add_paragraph(finding, style='List Bullet')
    
    doc.save(output_path)
```

---

#### **3.2 Share Chat Transcripts**

```python
GET /api/v1/chat/{session_id}/export?format=markdown

Response (Markdown):
```markdown
# Chat Transcript: GenAI in Architecture

**Date:** 2024-02-22

---

## Question 1
**You:** What are the main themes?

**AI:** The paper identifies 7 main themes through thematic analysis:
1. Strategic Definition & Brief
2. Architectural Design
...

**Sources:**
- TEXT - Results (Page 6)
- FIGURE - fig_0002 (Page 6)

---
```

---

#### **3.3 Generate Presentation Slides**

```python
POST /api/v1/papers/{paper_id}/slides
Body: {
  "template": "academic",  # or "business", "minimal"
  "slides": 10,
  "include": ["title", "problem", "method", "findings", "conclusion"]
}
```

**Using python-pptx:**
```python
from pptx import Presentation

def generate_slides(paper_data):
    prs = Presentation()
    
    # Title slide
    title_slide = prs.slides.add_slide(prs.slide_layouts[0])
    title_slide.shapes.title.text = paper_data['title']
    title_slide.placeholders[1].text = paper_data['authors']
    
    # Problem slide
    content_slide = prs.slides.add_slide(prs.slide_layouts[1])
    content_slide.shapes.title.text = "Research Problem"
    content_slide.placeholders[1].text = paper_data['problem']
    
    # ... more slides
    
    prs.save('presentation.pptx')
```

---

## ⚡ 4. Batch Processing

### **Process Multiple Papers at Once:**

```python
POST /api/v1/batch/upload
Body: multipart/form-data with multiple files

Response: {
  "batch_id": "batch-uuid",
  "files": [
    {"filename": "paper1.pdf", "status": "queued"},
    {"filename": "paper2.pdf", "status": "queued"}
  ],
  "estimated_time": "15 minutes"
}

# Check progress
GET /api/v1/batch/{batch_id}/status

Response: {
  "batch_id": "batch-uuid",
  "status": "processing",
  "progress": {
    "total": 10,
    "completed": 3,
    "failed": 0,
    "percentage": 30
  },
  "papers": [
    {"paper_id": "uuid-1", "status": "completed"},
    {"paper_id": "uuid-2", "status": "processing"},
    {"paper_id": "uuid-3", "status": "queued"}
  ]
}
```

**Implementation:**
```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

class BatchProcessor:
    def __init__(self, max_workers=3):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.batches = {}
    
    async def process_batch(self, batch_id: str, files: List):
        self.batches[batch_id] = {
            "status": "processing",
            "total": len(files),
            "completed": 0,
            "papers": []
        }
        
        # Process in parallel
        tasks = [self.process_single(file, batch_id) for file in files]
        await asyncio.gather(*tasks)
        
        self.batches[batch_id]["status"] = "completed"
    
    async def process_single(self, file, batch_id):
        # Run stages 1-3
        paper_id = await run_pipeline(file)
        
        # Update progress
        self.batches[batch_id]["completed"] += 1
        self.batches[batch_id]["papers"].append(paper_id)
```

---

## 📊 5. Analytics & Insights

### **Features:**

#### **5.1 Topic Clustering**

**Find themes across multiple papers:**

```python
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE

def cluster_papers(paper_ids: List[str], n_clusters: int = 5):
    # 1. Get embeddings for each paper
    embeddings = []
    for paper_id in paper_ids:
        paper_embedding = get_paper_embedding(paper_id)
        embeddings.append(paper_embedding)
    
    # 2. Cluster
    kmeans = KMeans(n_clusters=n_clusters)
    clusters = kmeans.fit_predict(embeddings)
    
    # 3. Generate cluster labels with LLM
    for i in range(n_clusters):
        papers_in_cluster = [paper_ids[j] for j in range(len(paper_ids)) if clusters[j] == i]
        label = generate_cluster_label(papers_in_cluster)
    
    return clusters, labels
```

**Visualization:**
```
Cluster 1: "AI in Construction" (15 papers)
Cluster 2: "Machine Learning Theory" (8 papers)
Cluster 3: "BIM Applications" (12 papers)
```

---

#### **5.2 Citation Network**

**Visualize paper relationships:**

```python
import networkx as nx

def build_citation_graph(papers: List[str]):
    G = nx.DiGraph()
    
    # Add nodes (papers)
    for paper in papers:
        G.add_node(paper['paper_id'], title=paper['title'])
    
    # Add edges (citations)
    for paper in papers:
        for cited_paper in paper['references']:
            if cited_paper in [p['paper_id'] for p in papers]:
                G.add_edge(paper['paper_id'], cited_paper)
    
    # Calculate metrics
    pagerank = nx.pagerank(G)
    centrality = nx.betweenness_centrality(G)
    
    return G, pagerank, centrality
```

**API:**
```python
GET /api/v1/analytics/citations?papers=all

Response: {
  "graph": {
    "nodes": [
      {"id": "uuid-1", "title": "...", "pagerank": 0.15, "centrality": 0.23}
    ],
    "edges": [
      {"source": "uuid-1", "target": "uuid-2", "weight": 3}
    ]
  },
  "most_cited": ["uuid-1", "uuid-3"],
  "most_influential": ["uuid-2"]
}
```

---

#### **5.3 Trend Analysis**

**Track topics over time:**

```python
GET /api/v1/analytics/trends?topic=AI&years=2020-2024

Response: {
  "topic": "AI",
  "timeline": [
    {"year": 2020, "papers": 5, "keywords": ["ML", "neural networks"]},
    {"year": 2021, "papers": 12, "keywords": ["deep learning", "transformers"]},
    {"year": 2022, "papers": 23, "keywords": ["GPT", "LLMs"]},
    {"year": 2023, "papers": 45, "keywords": ["ChatGPT", "GenAI"]},
    {"year": 2024, "papers": 67, "keywords": ["multimodal", "agents"]}
  ],
  "trend": "increasing",
  "growth_rate": "45% per year"
}
```

---

## 🎨 6. Personalization

### **Features:**

#### **6.1 Custom Reading Levels**

```python
POST /api/v1/chat
Body: {
  "paper_id": "uuid",
  "question": "Explain the methodology",
  "reading_level": "grade_5"  # or "grade_8", "college", "expert"
}

Response based on level:
- Grade 5: "They read 28 papers and found 7 main ideas..."
- Grade 8: "They used systematic review to analyze 28 papers..."
- College: "Systematic literature review with thematic analysis..."
- Expert: "Employed PRISMA methodology for systematic review..."
```

---

#### **6.2 Preferred Explanation Style**

```python
# User settings
PUT /api/v1/users/{user_id}/preferences
Body: {
  "explanation_style": "analogies",  # or "technical", "examples", "step-by-step"
  "format_preference": "bullet_points",  # or "paragraphs", "tables"
  "include_citations": true,
  "language": "en"
}

# Applied automatically to all responses
```

---

#### **6.3 Topic Highlighting**

```python
# Set interests
PUT /api/v1/users/{user_id}/interests
Body: {
  "topics": ["AI", "Construction", "BIM"],
  "keywords": ["machine learning", "neural networks"]
}

# Search results prioritize user interests
GET /api/v1/papers?personalized=true
# Returns papers matching user interests first
```

---

## 🔌 7. Integrations

### **7.1 Zotero Integration**

```python
# Import from Zotero
POST /api/v1/integrations/zotero/import
Body: {
  "api_key": "your-zotero-key",
  "library_id": "12345",
  "collection": "AI Papers"
}

Response: {
  "imported": 45,
  "failed": 2,
  "papers": ["uuid-1", "uuid-2", ...]
}
```

---

### **7.2 Google Drive Sync**

```python
# Auto-sync folder
POST /api/v1/integrations/gdrive/sync
Body: {
  "folder_id": "gdrive-folder-id",
  "auto_sync": true,
  "sync_interval": "daily"
}

# Watches folder for new PDFs and auto-processes
```

---

### **7.3 Notion Export**

```python
# Export summary to Notion
POST /api/v1/integrations/notion/export
Body: {
  "paper_id": "uuid",
  "database_id": "notion-db-id",
  "template": "paper_summary"
}

# Creates Notion page with:
# - Title
# - TL;DR
# - Key Findings
# - Link to chat
```

---

## 💰 Cost Estimate

**Stage 6 Features:**
- Database (PostgreSQL): $7-15/month (Render, Railway)
- Additional storage: $5/month (50GB)
- External APIs (Notion, Zotero): Free tiers available
- Processing costs: Same as before (~$0.07/paper)

**Total:** $12-25/month for full Stage 6

---

## 🎯 Implementation Priority

**Phase 1 (Must Have):**
1. Multi-paper management
2. Hybrid search
3. Export PDF/DOCX

**Phase 2 (Should Have):**
4. Batch processing
5. Basic analytics
6. Re-ranking

**Phase 3 (Nice to Have):**
7. Personalization
8. Integrations
9. Advanced visualizations

---

## ✅ Success Metrics

Stage 6 complete when:
- [ ] Can manage 100+ papers
- [ ] Search quality >90% relevant
- [ ] Export works in 3+ formats
- [ ] Batch process 10+ papers
- [ ] Basic analytics dashboard
- [ ] 1+ integration working

---

**🎉 With Stage 6, your system becomes a powerful research assistant!**

Next: **Stage 7** - Production web app with users, teams, and full deployment! 🚀
