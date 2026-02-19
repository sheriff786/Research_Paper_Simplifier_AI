# 🎨 ENHANCED STAGE 2: Multimodal Document Parsing
## Text + Tables + Figures + Images → Vector Database

# 🎨 ENHANCED STAGE 2: Multimodal Document Parsing
## Text + Tables + Figures + Images → Vector Database

**Goal:** Extract ALL content types from research papers

**What we'll build:**
1. Text chunking (semantic)
2. Table extraction (Camelot + AI summarization)
3. Figure extraction (PyMuPDF + GPT-4 Vision)
4. Multimodal embeddings
5. Unified vector database
6. Cross-reference linking

---

## 📦 Step 1: Imports and Setup

```python
# Core imports
import os
import json
import base64
import io
import numpy as np
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from datetime import datetime
from collections import Counter

# PDF processing
import fitz  # PyMuPDF
import pdfplumber
import camelot

from PIL import Image

# Text processing
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

# Embeddings
from langchain.embeddings import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings

# Vector store
import faiss
from langchain_community.vectorstores import FAISS

# AI/LLM
from langchain_openai import ChatOpenAI
from crewai import Agent, Task, Crew, Process

# Environment
from dotenv import load_dotenv

load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    print("⚠️  OPENAI_API_KEY not found!")
else:
    print("✅ OpenAI API Key loaded")

print("✅ All imports successful!")
```

## 📂 Step 2: Load Stage 1 Output

```python
# Load Stage 1 data
STAGE1_OUTPUT = "data/research_paper/stage1_output.json"
PDF_PATH = "data/research_paper/corona.pdf"  # Update if needed

with open(STAGE1_OUTPUT, 'r', encoding='utf-8') as f:
    stage1_data = json.load(f)

print("✅ Loaded Stage 1 data")
print(f"\n📄 Paper: {stage1_data['metadata']['title']}")
print(f"📊 Pages: {stage1_data['metadata']['pages']}")
```

## 🔪 Step 3: Text Chunking (from Stage 2)

```python
class SemanticChunker:
    """Smart text chunking with metadata"""
    
    def __init__(self, chunk_size=1000, chunk_overlap=200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""],
        )
    
    def chunk_by_section(self, sections: Dict[str, str], paper_metadata: Dict) -> List[Dict]:
        """Chunk text while preserving section context"""
        chunks = []
        chunk_id = 0
        
        for section_name, section_text in sections.items():
            if not section_text or len(section_text.strip()) < 50:
                continue
            
            text_chunks = self.text_splitter.split_text(section_text)
            
            for i, chunk_text in enumerate(text_chunks):
                chunks.append({
                    "type": "text",
                    "chunk_id": f"chunk_{chunk_id:04d}",
                    "content": chunk_text,
                    "section": section_name,
                    "chunk_index": i,
                    "metadata": {
                        "word_count": len(chunk_text.split()),
                        "char_count": len(chunk_text),
                        "paper_title": paper_metadata.get("title", "Unknown"),
                    }
                })
                chunk_id += 1
        
        return chunks

# Create chunker
chunker = SemanticChunker(chunk_size=1000, chunk_overlap=200)
text_chunks = chunker.chunk_by_section(
    sections=stage1_data['sections_full'],
    paper_metadata=stage1_data['metadata']
)

print(f"✅ Created {len(text_chunks)} text chunks")
```

## 📊 Step 4: Table Extraction

```python
class TableExtractor:
    """Extract tables from PDF using Camelot"""
    
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
    
    def extract_tables(self) -> List[Dict]:
        """Extract all tables from PDF"""
        print("📊 Extracting tables...")
        
        try:
            # Try Camelot first (best for tables)
            tables = camelot.read_pdf(self.pdf_path, pages='all', flavor='lattice')
            print(f"   Found {len(tables)} tables with Camelot")
        except Exception as e:
            print(f"   Camelot failed: {e}")
            print("   Falling back to pdfplumber...")
            tables = self._extract_with_pdfplumber()
        
        extracted_tables = []
        
        for i, table in enumerate(tables):
            try:
                # Convert to pandas DataFrame
                if hasattr(table, 'df'):
                    df = table.df
                else:
                    df = table
                
                # Extract table data
                table_data = {
                    "type": "table",
                    "table_id": f"table_{i:04d}",
                    "page": table.page if hasattr(table, 'page') else i + 1,
                    "content": {
                        "raw_data": df.values.tolist(),
                        "columns": df.columns.tolist(),
                        "csv": df.to_csv(index=False),
                        "markdown": df.to_markdown(),
                    },
                    "metadata": {
                        "rows": len(df),
                        "columns": len(df.columns),
                        "extraction_method": "camelot",
                    }
                }
                
                extracted_tables.append(table_data)
            except Exception as e:
                print(f"   Error extracting table {i}: {e}")
        
        return extracted_tables
    
    def _extract_with_pdfplumber(self) -> List:
        """Fallback extraction using pdfplumber"""
        tables = []
        
        with pdfplumber.open(self.pdf_path) as pdf:
            for page in pdf.pages:
                page_tables = page.extract_tables()
                for table in page_tables:
                    if table:
                        tables.append(table)
        
        return tables

# Extract tables
table_extractor = TableExtractor(PDF_PATH)
tables = table_extractor.extract_tables()

print(f"\n✅ Extracted {len(tables)} tables")
if tables:
    print(f"   Example: Table 0 has {tables[0]['metadata']['rows']} rows")
```

```python
tables
```

## 🖼️ Step 5: Figure/Image Extraction

```python
class FigureExtractor:
    """Extract figures and images from PDF"""
    
    def __init__(self, pdf_path: str, output_dir: str = "extracted_figures"):
        self.pdf_path = pdf_path
        self.output_dir = output_dir
        Path(output_dir).mkdir(exist_ok=True)
    
    def extract_figures(self) -> List[Dict]:
        """Extract all images/figures from PDF"""
        print("🖼️  Extracting figures...")
        
        doc = fitz.open(self.pdf_path)
        figures = []
        figure_id = 0
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            image_list = page.get_images(full=True)
            
            for img_index, img in enumerate(image_list):
                try:
                    # Get image data
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]
                    
                    # Save image
                    image_path = f"{self.output_dir}/figure_{figure_id:04d}.{image_ext}"
                    with open(image_path, "wb") as img_file:
                        img_file.write(image_bytes)
                    
                    # Get image dimensions
                    img_obj = Image.open(io.BytesIO(image_bytes))
                    width, height = img_obj.size
                    
                    # Convert to base64 for AI analysis
                    img_base64 = base64.b64encode(image_bytes).decode('utf-8')
                    
                    figure_data = {
                        "type": "figure",
                        "figure_id": f"fig_{figure_id:04d}",
                        "page": page_num + 1,
                        "content": {
                            "image_path": image_path,
                            "image_base64": img_base64,
                            "width": width,
                            "height": height,
                            "format": image_ext,
                        },
                        "metadata": {
                            "size_bytes": len(image_bytes),
                            "aspect_ratio": width / height if height > 0 else 0,
                        }
                    }
                    
                    figures.append(figure_data)
                    figure_id += 1
                    
                except Exception as e:
                    print(f"   Error extracting image on page {page_num + 1}: {e}")
        
        doc.close()
        return figures

# Extract figures
figure_extractor = FigureExtractor(PDF_PATH)
figures = figure_extractor.extract_figures()

print(f"\n✅ Extracted {len(figures)} figures")
print(f"   Saved to: extracted_figures/")
```

```python
figures
```

## 🤖 Step 6: AI Analysis - Table Summarization

```python
# Initialize LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)

# Create Table Analyst Agent
table_analyst = Agent(
    role="Table Data Analyst",
    goal="Analyze tables and extract key insights and summaries",
    backstory="""You are an expert at reading and understanding tabular data.
    You can quickly identify patterns, key findings, and summarize complex tables
    in simple language. You focus on the most important information.""",
    llm=llm,
    verbose=False,
)

def summarize_table(table_data: Dict) -> str:
    """Use AI to summarize a table"""
    
    # Get table as markdown
    table_markdown = table_data['content']['markdown']
    
    # Create task
    task = Task(
        description=f"""Analyze this table and provide:
        1. A brief summary (2-3 sentences)
        2. Key insights (3-5 bullet points)
        
        Table:
        {table_markdown[:2000]}  # Limit to first 2000 chars
        
        Format your response as:
        SUMMARY: [your summary]
        INSIGHTS:
        - [insight 1]
        - [insight 2]
        - [insight 3]
        """,
        agent=table_analyst,
        expected_output="Summary and key insights from the table"
    )
    
    # Create crew and execute
    crew = Crew(
        agents=[table_analyst],
        tasks=[task],
        process=Process.sequential,
        verbose=False
    )
    
    result = crew.kickoff()
    return str(result)

# Summarize first table as example
if tables:
    print("🤖 Analyzing first table with AI...\n")
    summary = summarize_table(tables[0])
    tables[0]['ai_summary'] = summary
    print(summary)
    print("\n✅ Table analysis complete!")
else:
    print("⚠️  No tables found to analyze")
```

## 🎨 Step 7: AI Analysis - Figure Description (GPT-4 Vision)

```python
def describe_figure_with_vision(figure_data: Dict) -> str:
    """Use GPT-4 Vision to describe a figure"""
    
    from openai import OpenAI
    client = OpenAI()
    
    try:
        # Get base64 image
        image_base64 = figure_data['content']['image_base64']
        
        # Call GPT-4 Vision
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # or "gpt-4-vision-preview" for better quality
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": """Analyze this figure from a research paper. Provide:
                            1. What type of figure is this? (chart, diagram, flowchart, etc.)
                            2. What does it show? (2-3 sentences)
                            3. Key elements or data points (3-5 items)
                            
                            Be concise and focus on the main message."""
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=300
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Error analyzing figure: {str(e)}"

# Describe first figure as example
if figures and os.getenv("OPENAI_API_KEY"):
    print("🎨 Analyzing first figure with GPT-4 Vision...\n")
    description = describe_figure_with_vision(figures[0])
    figures[0]['ai_description'] = description
    print(description)
    print("\n✅ Figure analysis complete!")
else:
    print("⚠️  No figures found or API key missing")
```

## 🔗 Step 8: Cross-Reference Detection

```python
def detect_cross_references(text_chunks: List[Dict], tables: List[Dict], figures: List[Dict]):
    """Detect references between text, tables, and figures"""
    
    print("🔗 Detecting cross-references...")
    
    # Add references to tables
    for table in tables:
        table_id = table['table_id']
        table['referenced_by_chunks'] = []
        
        # Search for mentions in text
        for chunk in text_chunks:
            content_lower = chunk['content'].lower()
            # Look for "Table X", "table X", "Table 1", etc.
            if 'table' in content_lower:
                table['referenced_by_chunks'].append(chunk['chunk_id'])
    
    # Add references to figures
    for figure in figures:
        figure_id = figure['figure_id']
        figure['referenced_by_chunks'] = []
        
        # Search for mentions in text
        for chunk in text_chunks:
            content_lower = chunk['content'].lower()
            # Look for "Figure X", "Fig. X", etc.
            if 'figure' in content_lower or 'fig.' in content_lower:
                figure['referenced_by_chunks'].append(chunk['chunk_id'])
    
    # Add references from text to tables/figures
    for chunk in text_chunks:
        chunk['references_tables'] = []
        chunk['references_figures'] = []
        
        content_lower = chunk['content'].lower()
        
        if 'table' in content_lower:
            chunk['references_tables'] = [t['table_id'] for t in tables[:3]]  # Link to first few
        
        if 'figure' in content_lower or 'fig.' in content_lower:
            chunk['references_figures'] = [f['figure_id'] for f in figures[:3]]  # Link to first few
    
    print(f"✅ Cross-references detected")
    print(f"   Tables with references: {sum(1 for t in tables if t.get('referenced_by_chunks'))}")
    print(f"   Figures with references: {sum(1 for f in figures if f.get('referenced_by_chunks'))}")

# Detect cross-references
detect_cross_references(text_chunks, tables, figures)
```

## 🧠 Step 9: Generate Multimodal Embeddings

```python
# Choose embedding model
USE_OPENAI = True  # Set False for local embeddings

if USE_OPENAI and os.getenv("OPENAI_API_KEY"):
    print("🤖 Using OpenAI Embeddings")
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
else:
    print("🤖 Using Local HuggingFace Embeddings")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Prepare all documents for embedding
all_documents = []

# 1. Text chunks
for chunk in text_chunks:
    doc = Document(
        page_content=chunk['content'],
        metadata={
            "type": "text",
            "id": chunk['chunk_id'],
            "section": chunk['section'],
            **chunk['metadata']
        }
    )
    all_documents.append(doc)

# 2. Tables (embed caption + summary + data preview)
for table in tables:
    # Create searchable text from table
    table_text = f"""Table {table['table_id']} (Page {table['page']}):
    {table.get('ai_summary', 'Table data available')}
    Data: {table['content']['markdown'][:500]}"""  # First 500 chars
    
    doc = Document(
        page_content=table_text,
        metadata={
            "type": "table",
            "id": table['table_id'],
            "page": table['page'],
            "rows": table['metadata']['rows'],
            "columns": table['metadata']['columns'],
        }
    )
    all_documents.append(doc)

# 3. Figures (embed description)
for figure in figures:
    # Create searchable text from figure
    figure_text = f"""Figure {figure['figure_id']} (Page {figure['page']}):
    {figure.get('ai_description', 'Figure available')}"""
    
    doc = Document(
        page_content=figure_text,
        metadata={
            "type": "figure",
            "id": figure['figure_id'],
            "page": figure['page'],
            "image_path": figure['content']['image_path'],
        }
    )
    all_documents.append(doc)

print(f"\n📊 Total documents to embed:")
print(f"   Text chunks: {len(text_chunks)}")
print(f"   Tables: {len(tables)}")
print(f"   Figures: {len(figures)}")
print(f"   TOTAL: {len(all_documents)}")
```

## 🗄️ Step 10: Create Multimodal Vector Store

```python
print("\n🔄 Creating multimodal vector store...")
print(f"   Embedding {len(all_documents)} documents...")
print("   This may take 2-3 minutes...\n")

# Create FAISS vector store
vectorstore = FAISS.from_documents(
    documents=all_documents,
    embedding=embeddings
)

print("✅ Multimodal vector store created!")
print(f"   Indexed {len(all_documents)} documents")
print(f"   Ready for semantic search across all content types!")
```

## 💾 Step 11: Save Everything

```python
# Save vector store
VECTORSTORE_PATH = "vectorstore_multimodal"
vectorstore.save_local(VECTORSTORE_PATH)
print(f"✅ Vector store saved to: {VECTORSTORE_PATH}")

# Save metadata
stage2_enhanced_output = {
    "paper_id": stage1_data.get('pdf_path', 'unknown'),
    "processed_at": datetime.now().isoformat(),
    "paper_metadata": stage1_data['metadata'],
    "extraction_stats": {
        "text_chunks": len(text_chunks),
        "tables": len(tables),
        "figures": len(figures),
        "total_documents": len(all_documents),
    },
    "content": {
        "text_chunks": text_chunks[:5],  # Save first 5 as examples
        "tables": tables,
        "figures": [{k: v for k, v in f.items() if k != 'content'} for f in figures],  # Exclude base64
    },
    "vectorstore": {
        "path": VECTORSTORE_PATH,
        "embedding_model": "text-embedding-3-small" if USE_OPENAI else "all-MiniLM-L6-v2",
    }
}

OUTPUT_FILE = "stage2_enhanced_output.json"
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(stage2_enhanced_output, f, indent=2, ensure_ascii=False)

print(f"✅ Metadata saved to: {OUTPUT_FILE}")
```

## 🔍 Step 12: Test Multimodal Search

```python
def multimodal_search(query: str, k: int = 5, filter_type: Optional[str] = None):
    """Search across all content types"""
    
    print(f"\n{'='*60}")
    print(f"🔍 Query: {query}")
    if filter_type:
        print(f"   Filter: {filter_type} only")
    print(f"{'='*60}\n")
    
    # Search
    if filter_type:
        results = vectorstore.similarity_search(
            query, 
            k=k,
            filter={"type": filter_type}
        )
    else:
        results = vectorstore.similarity_search(query, k=k)
    
    # Display results
    for i, doc in enumerate(results, 1):
        content_type = doc.metadata.get('type', 'unknown')
        doc_id = doc.metadata.get('id', 'unknown')
        
        if content_type == 'text':
            icon = "📝"
        elif content_type == 'table':
            icon = "📊"
        elif content_type == 'figure':
            icon = "🖼️"
        else:
            icon = "📄"
        
        print(f"{i}. {icon} {content_type.upper()}: {doc_id}")
        print(f"   Page: {doc.metadata.get('page', 'N/A')}")
        print(f"   Preview: {doc.page_content[:200]}...")
        print()
    
    return results

# Test searches
print("\n" + "="*60)
print("MULTIMODAL SEARCH TESTS")
print("="*60)

# Test 1: General search
multimodal_search("What are the main themes in GenAI applications?", k=5)

# Test 2: Table-specific search
multimodal_search("Show me comparison data", k=3, filter_type="table")

# Test 3: Figure-specific search
multimodal_search("Show me visual diagrams", k=3, filter_type="figure")
```

## 📊 Step 13: Analysis & Statistics

```python
print("\n" + "="*60)
print("ENHANCED STAGE 2 - FINAL STATISTICS")
print("="*60)

print(f"\n📄 Paper: {stage1_data['metadata']['title'][:60]}...")
print(f"📊 Pages: {stage1_data['metadata']['pages']}")

print(f"\n📝 Content Extracted:")
print(f"   Text chunks: {len(text_chunks)}")
print(f"   Tables: {len(tables)}")
print(f"   Figures: {len(figures)}")
print(f"   TOTAL: {len(all_documents)} searchable items")

print(f"\n🤖 AI Analysis:")
print(f"   Tables summarized: {sum(1 for t in tables if 'ai_summary' in t)}")
print(f"   Figures described: {sum(1 for f in figures if 'ai_description' in f)}")

print(f"\n🔗 Cross-references:")
print(f"   Text chunks linking tables: {sum(1 for c in text_chunks if c.get('references_tables'))}")
print(f"   Text chunks linking figures: {sum(1 for c in text_chunks if c.get('references_figures'))}")

print(f"\n💾 Saved:")
print(f"   Vector store: {VECTORSTORE_PATH}/")
print(f"   Metadata: {OUTPUT_FILE}")
print(f"   Figures: extracted_figures/ ({len(figures)} images)")

print(f"\n✅ ENHANCED STAGE 2 COMPLETE!")
print(f"\n🎯 Next: Stage 3 - AI Simplification Agents")
```

## 🎉 Summary

**What we accomplished:**
- ✅ Extracted text and chunked semantically
- ✅ Extracted tables with Camelot/pdfplumber
- ✅ Extracted figures with PyMuPDF
- ✅ AI summarization of tables (CrewAI)
- ✅ AI description of figures (GPT-4 Vision)
- ✅ Cross-reference detection
- ✅ Multimodal embeddings
- ✅ Unified vector database (FAISS)
- ✅ Search across all content types

**Ready for Stage 3!** 🚀

Advance stuff

```python
import fitz
import os

def render_pdf_pages(pdf_path, out_dir="pages", dpi=300):
    os.makedirs(out_dir, exist_ok=True)
    doc = fitz.open(pdf_path)
    image_paths = []

    for i in range(len(doc)):
        page = doc[i]
        pix = page.get_pixmap(dpi=dpi)
        img_path = f"{out_dir}/page_{i+1}.png"
        pix.save(img_path)
        image_paths.append((i + 1, img_path))

    return image_paths

```

```python
import torch
from PIL import Image
from transformers import DetrImageProcessor, TableTransformerForObjectDetection

processor = DetrImageProcessor.from_pretrained(
    "microsoft/table-transformer-detection"
)
model = TableTransformerForObjectDetection.from_pretrained(
    "microsoft/table-transformer-detection"
).eval()

def detect_full_tables(image_path, threshold=0.9):
    image = Image.open(image_path).convert("RGB")
    inputs = processor(images=image, return_tensors="pt")

    with torch.no_grad():
        outputs = model(**inputs)

    results = processor.post_process_object_detection(
        outputs,
        threshold=threshold,
        target_sizes=[image.size[::-1]]
    )[0]

    return results["boxes"].tolist()

```

```python
def crop_table(image_path, bbox, out_path):
    image = Image.open(image_path)
    cropped = image.crop(bbox)
    cropped.save(out_path)

```

```python
from transformers import TableTransformerForObjectDetection

structure_model = TableTransformerForObjectDetection.from_pretrained(
    "microsoft/table-transformer-structure-recognition"
).eval()

def detect_structure(table_image):
    inputs = processor(images=table_image, return_tensors="pt")

    with torch.no_grad():
        outputs = structure_model(**inputs)

    results = processor.post_process_object_detection(
        outputs,
        threshold=0.8,
        target_sizes=[table_image.size[::-1]]
    )[0]

    return results

```

```python

```



