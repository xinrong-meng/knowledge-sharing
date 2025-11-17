# Function Calling

## What

Built-in API feature that lets you pass function schemas to LLM APIs. The LLM can return function call requests (instead of text), your code executes them, sends results back, and the LLM generates a final answer.

## Why

LLMs only generate text. They can't:
- Access current data (weather, stock prices, today's date)
- Run code or calculations
- Query databases
- Make API calls

**Solution:** Define functions in your code, pass their schemas to the LLM API. When LLM needs to call one, it returns a function call object, you execute it, send the result back.

## How It Works

### Basic Flow

```
User: "What's the weather in NYC?"

┌─────────────┐
│ Your Code   │
└──────┬──────┘
       │ 1. Send to LLM API:
       │    - User message
       │    - Function schemas
       ▼
┌──────────────────┐
│  LLM API         │
│  (Anthropic/     │
│   OpenAI)        │
└──────┬───────────┘
       │ 2. LLM decides: "I need to call get_weather(location='NYC')"
       │ 3. Returns function call request
       ▼
┌─────────────┐
│ Your Code   │
│             │ 4. Execute function:
│ get_weather │    result = get_weather("NYC") → "72°F, sunny"
└──────┬──────┘
       │ 5. Send result back to LLM API
       ▼
┌──────────────────┐
│  LLM API         │
│                  │ 6. LLM generates final answer:
│                  │    "The weather in NYC is 72°F and sunny"
└──────┬───────────┘
       │
       ▼
    User gets answer
```

## Data Format

**In Python code:** You write Python dicts/objects

**Over network:** SDK automatically converts Python dicts → JSON strings for HTTP requests

**HTTP request format:**
```
POST https://api.anthropic.com/v1/messages
Content-Type: application/json
Body: {"model": "...", "messages": [...], "tools": [...]}
```

**HTTP response format:**
```
{"content": [{"type": "tool_use", "name": "...", "input": {...}}], "stop_reason": "tool_use"}
```

## Function Calling vs MCP

### Architecture Comparison

**Function Calling (Direct API):**

```
Your Code
    │
    │ HTTP: POST /v1/messages
    │ Body: {messages, tools}
    ▼
LLM API (Cloud)
```

**MCP Protocol:**

```
MCP Server (Local)
    │
    │ JSON-RPC: tools/list, tools/call
    ▼
MCP Client (Claude Desktop)
    │
    │ HTTP: POST /v1/messages (Function Calling)
    ▼
LLM API (Cloud)
```

**Summary:**

MCP is a wrapper around Function Calling. MCP Servers provide tools via JSON-RPC, MCP Client converts to Function Calling format and calls the LLM API.

## How LLM Decides What to Call

### Function Selection

```
User Query + Available Tools
        ↓
┌───────────────────────┐
│  LLM reads            │
│  function.description │ ← Decides which function to call
└───────────┬───────────┘
            │
            ▼
    Call function?
        │
        ├─ Yes → Returns function call request
        │
        └─ No → Returns text answer
```

### Parameter Extraction

```
User: "What's the weather in NYC?"

LLM reads parameter.description: "City name"
        ↓
Extracts: "NYC" → {"location": "NYC"}
```

### Multiple Calls

LLM can request multiple functions in one response (parallel execution).

## Implementation Options

**1. Direct API (Anthropic/OpenAI)**
- Pass `tools` parameter directly to LLM APIs
- Simplest approach
- Use for custom apps, scripts

**2. LangChain @tool decorator**
- Python decorator that auto-creates schemas
- Uses Function Calling APIs under the hood
- Convenient for Python apps

**3. MCP Protocol**
- Standardized protocol for tool servers
- Used by Claude Desktop, IDEs
- Uses Function Calling internally

## When to Use

✅ Need real-time data (weather, prices, search)  
✅ Need calculations or code execution  
✅ Need database/API access  
❌ Just generating text → no function calling needed

## Resources

- Cursor with Claude Model
- Related: [84. MCP.md](84.%20MCP.md) - Standardized protocol built on Function Calling
