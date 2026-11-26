## Day 2 — Semantic Search & Vector Storage

- [x] Local embedding generation using Sentence Transformers
- [x] 384-dimensional normalized embeddings
- [x] Cosine similarity and dot product
- [x] In-memory semantic search
- [x] PostgreSQL and pgvector integration
- [x] Persistent vector storage
- [x] Upsert-based duplicate prevention
- [x] Database connection timeouts
- [x] HNSW index configuration
- [x] Persistent semantic search engine
- [x] Command-line interface
- [x] Automated embedding and similarity tests

### Technology Stack

- Python
- Sentence Transformers (all-MiniLM-L6-v2)
- PostgreSQL 16
- pgvector
- Docker Compose
- Psycopg
- NumPy
- Pytest

### Usage

```bash
docker compose up -d

python cli.py index --path .

python cli.py count

python cli.py search --query "How does authentication work?" --top-k 3
```

All embedding generation and vector storage operate locally without paid API dependencies.