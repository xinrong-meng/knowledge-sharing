# LangChain

## What is LangChain

Framework for building LLM applications where components 
work together seamlessly and can be easily swapped.

> LangChain is basically just a collection of utility scripts for working with LLMs and external tools like semantic similarity stores and such. There is nothing in Langchain that wouldn't be trivially easy to just do yourself if you're a mildly competent python programmer that knows what they're doing.
> 
> — Reddit user

## Components

- Model: The language model engine (like Claude, GPT)
- Message: Structured ways to send information to/from the AI
- Tool: Functions LLMs can call (@tool decorator)
- Agent: An AI-powered decison makers about which tools to use and when
- Chain: A pre-built component that combines multiple LangChain pieces into a reusable workflow

## LangChain Expression Language (LCEL)

What it is: A simple way to chain components together using the | (pipe) operator.

```
chain = prompt | llm | output_parser
result = chain.invoke({"topic": "jokes", "question": "Tell me a joke"})

prompt formats your input into a proper message
llm sends it to e.g. Claude and gets response
output_parser extracts just the text string
```

## Role

The three roles ("system", "user", "assistant") are a universal standard used throughout LangChain and all chat-based AI models. These roles appear everywhere: in ChatPromptTemplate for creating prompt templates, in direct message objects like SystemMessage/HumanMessage/AIMessage, in chat history/memory systems, and in the actual API calls to Claude, GPT, and other models. They represent who is speaking in a conversation: 
- "system" sets instructions for the AI's behavior
-  "user" is the human's input
- "assistant" is the AI's previous responses (useful for conversation context)


## LangChain = The RAG Assembly Kit

### RAG (Retrieval Augmented Generation)

Simple idea: Look up relevant information, then give it to the LLM

#### How RAG Works (3 Steps):

1. Index Your Documents (Do Once)

```
Your Documents → Split into Chunks → Convert to Numbers (Embeddings) → Store in Database
```

2. Search for Relevant Info (Every Query)

```
User Question → Convert to Numbers → Find Similar Chunks → Retrieve Top Results
```

3. Generate Answer (Every Query)

```
Question + Retrieved Chunks → Send to LLM → Get Answer
```

#### With Langchain

LangChain is a toolkit that makes building RAG systems 10x easier by providing:
- Document loaders
- Text splitters
- Vector store integrations
- Retrievers
- Chain builders (LCEL)

```
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

# Create RAG chain with LCEL
prompt = ChatPromptTemplate.from_template("""
Answer based on context: {context}
Question: {question}
""")

rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
)

# Use it
answer = rag_chain.invoke("What is RAG?")
```

### Example Usage

[`code-examples/langchain/`](code-examples/langchain/)

## References
- Cursor with Claude Model
