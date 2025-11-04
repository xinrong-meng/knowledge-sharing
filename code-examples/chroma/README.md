# Chroma Vector Database - Bare Minimum Example

A minimal, runnable example demonstrating Chroma vector database operations.

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) package manager (or use pip)

### 2. Install Dependencies

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install chromadb
```

### 3. Run Example

```bash
# Using uv
uv run example.py

# Or directly
python example.py
```

## 📚 What This Demonstrates

- Creating a Chroma client with persistent storage
- Creating a collection (like a table in a database)
- Adding documents (Chroma automatically creates embeddings)
- Querying for similar documents using semantic search
- Understanding similarity scores

## 🎯 Key Concept

**Semantic Search**: The query "What's a good way to save for retirement through my employer?" finds the 401(k) document even though the query doesn't contain the exact keyword "401(k)". This is because embeddings capture meaning - the vector database understands that "retirement through employer" relates to employer-sponsored retirement plans.


## 📁 Output

The example creates a `chroma_db/` directory with persistent storage. Your documents and embeddings are saved there.

## Related Documentation

Vector Databases: [87. Vector Databases.md](../../87.%20Vector%20Databases.md)
