research_paper_ai/
│
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── endpoints/
│   │   │   │   ├── papers.py
│   │   │   │   ├── chat.py
│   │   │   │   └── health.py
│   │   │   └── router.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── logging.py
│   │   └── constants.py
│   │
│   ├── ingestion/
│   │   ├── pdf_loader.py
│   │   ├── section_extractor.py
│   │   └── metadata_extractor.py
│   │
│   ├── processing/
│   │   ├── normalizer.py
│   │   ├── chunker.py
│   │   └── equation_parser.py
│   │
│   ├── rag/
│   │   ├── embeddings.py
│   │   ├── vector_store.py
│   │   └── retriever.py
│   │
│   ├── agents/
│   │   ├── base_agent.py
│   │   ├── paper_understanding.py
│   │   ├── simplifier.py
│   │   ├── math_explainer.py
│   │   ├── critic.py
│   │   └── citation_agent.py
│   │
│   ├── crew/
│   │   ├── crew_manager.py
│   │   └── tasks.py
│   │
│   ├── tools/
│   │   ├── mcp_tools.py
│   │   └── search_tools.py
│   │
│   ├── services/
│   │   ├── paper_service.py
│   │   ├── chat_service.py
│   │   └── citation_service.py
│   │
│   ├── schemas/
│   │   ├── paper.py
│   │   ├── chat.py
│   │   └── citation.py
│   │
│   ├── storage/
│   │   ├── local_fs.py
│   │   └── cache.py
│   │
│   └── main.py
│
├── tests/
│   ├── test_ingestion.py
│   ├── test_rag.py
│   └── test_agents.py
│
├── requirements.txt
├── setup.py
├── README.md
└── .env
