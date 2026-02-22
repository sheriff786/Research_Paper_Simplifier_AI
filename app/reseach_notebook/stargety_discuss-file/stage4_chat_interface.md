# 💬 STAGE 4: Interactive Chat Interface
## RAG-Based Q&A System for Research Papers

---

# 💬 STAGE 4: Interactive Chat Interface
## RAG-Based Q&A System for Research Papers

**Goal:** Build an interactive chat system where users can ask questions about the paper

**What we'll build:**
1. RAG-based chat system with memory
2. Citation tracking
3. Multi-turn conversations
4. Gradio chat interface
5. FastAPI backend (optional)

**Output:** Beautiful chat interface where anyone can talk to the research paper!

---

## 📦 Step 1: Imports and Setup

```python
# Core imports
import os
import json
from typing import List, Dict, Tuple, Optional
from datetime import datetime

# LangChain - RAG components
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

# Vector store
from langchain.embeddings import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Gradio for UI
import gradio as gr

# Environment
from dotenv import load_dotenv

load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("❌ OPENAI_API_KEY required for Stage 4")

print("✅ All imports successful!")
print("✅ OpenAI API Key loaded")
```

## 📂 Step 2: Load Previous Stage Outputs

```python
# File paths
STAGE1_OUTPUT = "stage1_output.json"
STAGE2_OUTPUT = "stage2_enhanced_output.json"
STAGE3_OUTPUT = "stage3_simplified_output.json"
VECTORSTORE_PATH = "vectorstore_multimodal"

# Load Stage 1
with open(STAGE1_OUTPUT, 'r', encoding='utf-8') as f:
    stage1_data = json.load(f)

# Load Stage 2
with open(STAGE2_OUTPUT, 'r', encoding='utf-8') as f:
    stage2_data = json.load(f)

# Load Stage 3
with open(STAGE3_OUTPUT, 'r', encoding='utf-8') as f:
    stage3_data = json.load(f)

print("✅ All stage data loaded")
print(f"\n📄 Paper: {stage1_data['metadata']['title'][:60]}...")
print(f"📊 Vector DB items: {stage2_data['extraction_stats']['total_documents']}")
print(f"📝 Simplification ready: Yes")
```

## 🔍 Step 3: Load Vector Store

```python
# Load embeddings (same as Stage 2)
USE_OPENAI = True

if USE_OPENAI:
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
else:
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Load vector store
vectorstore = FAISS.load_local(
    VECTORSTORE_PATH,
    embeddings,
    allow_dangerous_deserialization=True
)

print("✅ Vector store loaded")
print(f"   Ready for semantic search!")
```

## 🤖 Step 4: Create Custom Prompt Template

```python
# Custom prompt for better responses
CUSTOM_PROMPT_TEMPLATE = """You are an expert at explaining research papers in simple terms.

Your role:
1. Answer questions about the research paper accurately
2. Use simple, everyday language (8th grade level)
3. Provide examples and analogies when helpful
4. Always cite your sources (mention section and page)
5. If information isn't in the context, say so honestly

Paper Title: {paper_title}

Simplified Summary (for context):
{simplified_summary}

Relevant Context from Paper:
{context}

Conversation History:
{chat_history}

User Question: {question}

Instructions:
- Keep answers concise (2-3 paragraphs max)
- Start with a direct answer
- Add "In simple terms:" for complex concepts
- End with source citations in [brackets]

Answer:"""

# Get simplified summary from Stage 3
simplified_summary = stage3_data.get('simplification', {}).get('full_output', '')[:500]
paper_title = stage1_data['metadata']['title']

print("✅ Custom prompt template created")
```

## 🧠 Step 5: Create Paper Chatbot Class

```python
class PaperChatbot:
    """RAG-based chatbot for research papers"""
    
    def __init__(self, vectorstore, paper_title: str, simplified_summary: str):
        self.vectorstore = vectorstore
        self.paper_title = paper_title
        self.simplified_summary = simplified_summary
        
        # Initialize LLM
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.3,  # Some creativity but mostly consistent
        )
        
        # Create memory for conversation
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )
        
        # Create custom prompt
        self.prompt = PromptTemplate(
            template=CUSTOM_PROMPT_TEMPLATE,
            input_variables=["context", "question", "chat_history"],
            partial_variables={
                "paper_title": self.paper_title,
                "simplified_summary": self.simplified_summary
            }
        )
        
        # Create conversational chain
        self.chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vectorstore.as_retriever(
                search_kwargs={"k": 5}  # Retrieve top 5 chunks
            ),
            memory=self.memory,
            return_source_documents=True,
            combine_docs_chain_kwargs={"prompt": self.prompt}
        )
    
    def ask(self, question: str) -> Dict:
        """Ask a question and get answer with sources"""
        
        # Get response from chain
        result = self.chain({"question": question})
        
        # Extract sources
        sources = []
        for doc in result.get('source_documents', []):
            sources.append({
                "content": doc.page_content[:200] + "...",
                "type": doc.metadata.get('type', 'text'),
                "section": doc.metadata.get('section', 'Unknown'),
                "page": doc.metadata.get('page', 'Unknown'),
                "id": doc.metadata.get('id', 'Unknown')
            })
        
        return {
            "answer": result['answer'],
            "sources": sources
        }
    
    def reset_conversation(self):
        """Clear conversation history"""
        self.memory.clear()
        print("✅ Conversation history cleared")

print("✅ PaperChatbot class defined")
```

## 🎯 Step 6: Initialize Chatbot

```python
# Create chatbot instance
chatbot = PaperChatbot(
    vectorstore=vectorstore,
    paper_title=paper_title,
    simplified_summary=simplified_summary
)

print("✅ Chatbot initialized and ready!")
print(f"\n📚 Chat with: {paper_title[:60]}...")
```

## 🧪 Step 7: Test Chatbot (Terminal)

```python
# Test with sample questions
test_questions = [
    "What is this paper about?",
    "What are the main themes identified?",
    "What are the limitations?"
]

print("🧪 Testing chatbot with sample questions:\n")
print("="*60)

for i, question in enumerate(test_questions, 1):
    print(f"\n👤 Q{i}: {question}")
    print("-" * 60)
    
    result = chatbot.ask(question)
    
    print(f"🤖 Answer:\n{result['answer']}")
    
    if result['sources']:
        print(f"\n📎 Sources:")
        for j, source in enumerate(result['sources'][:3], 1):  # Show top 3
            print(f"   {j}. {source['type'].upper()} - {source['section']} (Page {source['page']})")
    
    print("="*60)

print("\n✅ Terminal test complete!")
```

## 🎨 Step 8: Create Gradio Chat Interface

```python
def chat_with_paper(message: str, history: List[List[str]]) -> str:
    """
    Chat function for Gradio interface
    
    Args:
        message: User's question
        history: Chat history (not used, managed by chatbot internally)
    
    Returns:
        Answer with sources
    """
    try:
        # Get answer from chatbot
        result = chatbot.ask(message)
        
        # Format response with sources
        response = result['answer']
        
        # Add sources if available
        if result['sources']:
            response += "\n\n---\n**📎 Sources:**\n"
            for i, source in enumerate(result['sources'][:3], 1):
                response += f"\n{i}. **{source['type'].upper()}** - {source['section']} (Page {source['page']})"
        
        return response
        
    except Exception as e:
        return f"❌ Error: {str(e)}\n\nPlease try rephrasing your question."

print("✅ Chat function defined")
```

## 🚀 Step 9: Build Gradio Interface

```python
# Create custom CSS
custom_css = """
.container {
    max-width: 900px;
    margin: auto;
}
.user-message {
    background-color: #e3f2fd !important;
}
.bot-message {
    background-color: #f5f5f5 !important;
}
"""

# Create example questions
example_questions = [
    "What is this paper about?",
    "What are the 7 main themes identified?",
    "What methodology did the researchers use?",
    "What are the main findings?",
    "What are the limitations of this research?",
    "Show me information about tables or figures",
    "How is GenAI used in construction?",
    "What future research is needed?"
]

# Build interface
interface = gr.ChatInterface(
    fn=chat_with_paper,
    title=f"📚 Research Paper Chat: {paper_title[:50]}...",
    description=f"""**Ask me anything about this research paper!**
    
**TL;DR:** {simplified_summary[:200]}...
    
💡 **Tips:**
- Ask about main themes, methodology, findings, or limitations
- Request explanations in simple terms
- Ask about specific tables or figures
- Follow up with "Tell me more about that"
    """,
    examples=example_questions,
    theme=gr.themes.Soft(),
    css=custom_css,
    retry_btn="🔄 Retry",
    undo_btn="↩️ Undo",
    clear_btn="🗑️ Clear Chat",
)

print("✅ Gradio interface built!")
print("\n🚀 Ready to launch!")
```

## 🌐 Step 10: Launch Chat Interface

```python
# Launch the interface
print("🚀 Launching chat interface...\n")
print("="*60)
print("📚 Research Paper Chat Interface")
print("="*60)
print(f"\n📄 Paper: {paper_title}")
print(f"💬 Chat: Ready to answer questions!")
print(f"🌐 Interface: Opening in browser...\n")

# Launch (will open in browser)
interface.launch(
    share=False,  # Set to True to create public link
    server_name="127.0.0.1",
    server_port=7860,
    show_error=True
)

# Note: In Jupyter, this will display the interface inline
# In a script, it will open in your default browser
```

## 💾 Step 11: Save Chat Session (Optional)

```python
def save_chat_session(session_name: str = "chat_session"):
    """Save current chat session to file"""
    
    # Get chat history from memory
    messages = chatbot.memory.chat_memory.messages
    
    # Convert to serializable format
    session_data = {
        "paper_title": paper_title,
        "timestamp": datetime.now().isoformat(),
        "messages": [
            {
                "role": msg.type,
                "content": msg.content
            }
            for msg in messages
        ]
    }
    
    # Save to file
    filename = f"{session_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(session_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Chat session saved to: {filename}")
    return filename

# Example usage (uncomment to save)
# save_chat_session("my_research_chat")

print("✅ Save function ready")
```

## 📊 Step 12: Chat Statistics

```python
def get_chat_stats() -> Dict:
    """Get statistics about the current chat session"""
    
    messages = chatbot.memory.chat_memory.messages
    
    stats = {
        "total_messages": len(messages),
        "user_messages": len([m for m in messages if m.type == "human"]),
        "ai_messages": len([m for m in messages if m.type == "ai"]),
        "total_chars": sum(len(m.content) for m in messages),
    }
    
    return stats

# Example usage
stats = get_chat_stats()
print("📊 Chat Session Statistics:")
print(f"   Total messages: {stats['total_messages']}")
print(f"   User questions: {stats['user_messages']}")
print(f"   AI responses: {stats['ai_messages']}")
print(f"   Total characters: {stats['total_chars']:,}")
```

## 🔧 Step 13: Advanced Features

```python
def search_by_type(query: str, content_type: str = "text", k: int = 3) -> List[Dict]:
    """Search for specific content types (text, table, figure)"""
    
    results = vectorstore.similarity_search(
        query,
        k=k,
        filter={"type": content_type}
    )
    
    return [
        {
            "content": doc.page_content[:200],
            "metadata": doc.metadata
        }
        for doc in results
    ]

def get_paper_sections() -> List[str]:
    """Get list of all sections in the paper"""
    return list(stage1_data['sections_full'].keys())

def get_section_content(section_name: str) -> str:
    """Get content of a specific section"""
    return stage1_data['sections_full'].get(section_name, "Section not found")

# Test advanced features
print("🔧 Advanced Features Available:")
print(f"   ✅ Search by content type (text, table, figure)")
print(f"   ✅ Get paper sections: {len(get_paper_sections())} sections")
print(f"   ✅ Direct section access")
print(f"   ✅ Chat session export")
```

## 📝 Step 14: Export Chat Transcript

```python
def export_chat_markdown(filename: str = "chat_transcript.md"):
    """Export chat as readable markdown"""
    
    messages = chatbot.memory.chat_memory.messages
    
    # Create markdown content
    md_content = []
    md_content.append(f"# Chat Transcript: {paper_title}\n")
    md_content.append(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    md_content.append("---\n\n")
    
    for i, msg in enumerate(messages):
        if msg.type == "human":
            md_content.append(f"## 👤 Question {(i//2)+1}\n")
            md_content.append(f"{msg.content}\n\n")
        else:
            md_content.append(f"### 🤖 Answer\n")
            md_content.append(f"{msg.content}\n\n---\n\n")
    
    # Write to file
    with open(filename, 'w', encoding='utf-8') as f:
        f.writelines(md_content)
    
    print(f"✅ Chat transcript exported to: {filename}")

# Example usage (uncomment to export)
# export_chat_markdown("my_chat_transcript.md")

print("✅ Export function ready")
```

## 🎉 Step 15: Summary & Next Steps

```python
print("\n" + "="*60)
print("🎉 STAGE 4 COMPLETE - CHAT INTERFACE READY")
print("="*60)

print(f"\n📄 Paper: {paper_title[:60]}...")
print(f"💬 Chat System: Active")
print(f"🔍 Vector Search: {stage2_data['extraction_stats']['total_documents']} items")

print(f"\n✨ Features Available:")
print(f"   ✅ Interactive chat with memory")
print(f"   ✅ Citation tracking (sources included)")
print(f"   ✅ Multi-turn conversations")
print(f"   ✅ Simplified explanations")
print(f"   ✅ Beautiful Gradio interface")
print(f"   ✅ Search by content type")
print(f"   ✅ Export chat transcripts")

print(f"\n🌐 Access:")
print(f"   Local: http://127.0.0.1:7860")
print(f"   (Set share=True to create public link)")

print(f"\n💰 Cost per chat session (~10 messages):")
print(f"   ~$0.015 with gpt-4o-mini")
print(f"   Your $120 = ~8,000 sessions!")

print(f"\n🎯 What You Can Do:")
print(f"   1. Ask questions about the paper")
print(f"   2. Get simple explanations")
print(f"   3. Find specific information")
print(f"   4. Explore tables and figures")
print(f"   5. Save chat sessions")
print(f"   6. Export transcripts")

print(f"\n🚀 Next: Stage 5 - FastAPI Backend + Web Deployment!")

print("\n" + "="*60)
print("✅ SUCCESS! Your research paper is now interactive!")
print("="*60)
```

## 🎉 Stage 4 Complete!

**What we accomplished:**
- ✅ Built RAG-based chat system
- ✅ Added conversation memory
- ✅ Implemented citation tracking
- ✅ Created beautiful Gradio UI
- ✅ Added advanced search features
- ✅ Export and save functionality

**Your research paper is now:**
- 💬 Conversational
- 🔍 Searchable
- 📚 Educational
- 🎨 Beautiful
- 🚀 Interactive

---

### 🎁 Bonus: Quick Commands

```python
# Reset conversation
chatbot.reset_conversation()

# Search for tables only
results = search_by_type("comparison data", "table")

# Get all sections
sections = get_paper_sections()

# Save chat session
save_chat_session("my_session")

# Export transcript
export_chat_markdown("transcript.md")

# Get statistics
stats = get_chat_stats()
```

**Enjoy chatting with your research paper!** 🎉

