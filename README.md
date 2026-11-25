# CodePilot

An open-source, repository-aware AI coding assistant
inspired by modern AI-native IDE architectures.

## Objective

Build a privacy-conscious coding assistant using
local LLMs and open-source infrastructure.

## Planned Features

- AST-based semantic code chunking
- Code embeddings and vector search
- Repository-aware RAG
- Incremental indexing using Merkle trees
- AI-powered code completion
- VS Code extension
- Agentic coding workflows
- Caching and model routing
- Automated evaluation and testing

## Technology Stack

Python, FastAPI, TypeScript, PostgreSQL, pgvector,
Ollama, Sentence Transformers, Redis, Docker.

## Development Progress

- [x] Project initialization
- [x] Repository scanning
- [x] AST-based code chunking
- [ ] Embedding generation
- [ ] Vector search
- [ ] Repository-aware chat
- [ ] Incremental indexing
- [ ] VS Code integration
- [ ] Code completion
- [ ] Agentic workflows

## Design Principles

- Local-first development
- No paid API dependencies
- Privacy-conscious architecture
- Modular and maintainable code
- Incremental development with automated tests

## Testing

Install development dependencies:

    pip install -r backend/requirements-dev.txt

Run the test suite:

    python -m pytest backend/tests -v
