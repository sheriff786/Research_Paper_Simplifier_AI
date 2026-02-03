import os

PROJECT_STRUCTURE = {
    "app": {
        "__init__.py": "",
        "main.py": "",
        "api": {
            "__init__.py": "",
            "v1": {
                "__init__.py": "",
                "router.py": "",
                "endpoints": {
                    "__init__.py": "",
                    "papers.py": "",
                    "chat.py": "",
                    "health.py": "",
                },
            },
        },
        "core": {
            "__init__.py": "",
            "config.py": "",
            "logging.py": "",
            "constants.py": "",
        },
        "ingestion": {
            "__init__.py": "",
            "pdf_loader.py": "",
            "section_extractor.py": "",
            "metadata_extractor.py": "",
        },
        "processing": {
            "__init__.py": "",
            "normalizer.py": "",
            "chunker.py": "",
            "equation_parser.py": "",
        },
        "rag": {
            "__init__.py": "",
            "embeddings.py": "",
            "vector_store.py": "",
            "retriever.py": "",
        },
        "agents": {
            "__init__.py": "",
            "base_agent.py": "",
            "paper_understanding.py": "",
            "simplifier.py": "",
            "math_explainer.py": "",
            "critic.py": "",
            "citation_agent.py": "",
        },
        "crew": {
            "__init__.py": "",
            "crew_manager.py": "",
            "tasks.py": "",
        },
        "tools": {
            "__init__.py": "",
            "mcp_tools.py": "",
            "search_tools.py": "",
        },
        "services": {
            "__init__.py": "",
            "paper_service.py": "",
            "chat_service.py": "",
            "citation_service.py": "",
        },
        "schemas": {
            "__init__.py": "",
            "paper.py": "",
            "chat.py": "",
            "citation.py": "",
        },
        "storage": {
            "__init__.py": "",
            "local_fs.py": "",
            "cache.py": "",
        },
    },
    "tests": {
        "__init__.py": "",
        "test_ingestion.py": "",
        "test_rag.py": "",
        "test_agents.py": "",
    },
}


def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)

        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            if not os.path.exists(path):
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)


if __name__ == "__main__":
    project_root = os.getcwd()
    create_structure(project_root, PROJECT_STRUCTURE)
    print("\n✅ Backend folder structure created successfully.\n")
