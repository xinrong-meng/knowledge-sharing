# LangChain Project - Bare Minimum Examples

A minimal, practical introduction to LangChain with Claude (Anthropic). This project demonstrates core LangChain concepts with clean, simple examples.

## 📁 Project Structure

```
langchain_proj/
├── main.py              # Basic LangChain chat with Claude
├── demo_concepts.py     # LCEL and ChatPromptTemplate demos
├── rag_example.py       # RAG (Retrieval-Augmented Generation)
├── pyproject.toml       # Project dependencies
└── README.md           # This file
```

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) package manager
- Anthropic API key

### 2. Install Dependencies

```bash
# Install all dependencies
uv sync
```

### 3. Set Up API Key

Get your API key from [Anthropic Console](https://console.anthropic.com/) and set it:

```bash
# Option A: Export in terminal (temporary)
export ANTHROPIC_API_KEY='your-api-key-here'

# Option B: Add to ~/.zshrc (permanent)
echo 'export ANTHROPIC_API_KEY="your-api-key-here"' >> ~/.zshrc
source ~/.zshrc
```

### 4. Run Examples

```bash
# Basic chat example
uv run main.py

# LCEL and prompt template concepts
uv run demo_concepts.py

# RAG (Retrieval-Augmented Generation)
uv run rag_example.py
```

## 📚 What's Included

### `main.py` - Basic LangChain Example

Demonstrates:
- ✅ Setting up ChatAnthropic (Claude)
- ✅ Using ChatPromptTemplate with system/user roles
- ✅ Output parsing with StrOutputParser
- ✅ LCEL (LangChain Expression Language) chains

**Key concepts:** Prompts → LLM → Parser pipeline

### `demo_concepts.py` - Core Concepts

Demonstrates:
- ✅ Reusable prompt templates with variables
- ✅ LCEL chain composition (`|` operator)
- ✅ Different prompt patterns (from_messages vs from_template)

**Key concepts:** Building modular, composable chains

### `rag_example.py` - RAG Implementation

Demonstrates:
- ✅ Vector stores (FAISS) for document storage
- ✅ Semantic embeddings (HuggingFace)
- ✅ Document retrieval based on similarity
- ✅ Combining retrieval with generation

## Related Documentation
LangChain introduction: [85. LangChain.md](https://github.com/xinrong-meng/knowledge-sharing/blob/master/85.%20LangChain.md)