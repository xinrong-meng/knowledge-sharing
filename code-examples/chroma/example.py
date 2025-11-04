"""
Bare minimum Chroma vector database example.

Demonstrates:
- Creating a collection
- Adding documents (Chroma automatically creates embeddings)
- Querying for similar documents
- Semantic search (finds relevant docs even without exact keywords)
"""

import chromadb

# Step 1: Create a Chroma client with persistent storage
# This creates a connection to the vector database (like opening a database connection)
# The ./chroma_db directory will be automatically created if it doesn't exist
client = chromadb.PersistentClient(path="./chroma_db")

# Step 2: Create or get a collection
# A collection is like a table in a database - it groups related documents together
# You can have multiple collections (e.g., "finance_docs", "tech_docs", etc.)
collection = client.get_or_create_collection(
    name="finance_documents",
    metadata={"description": "Financial knowledge base"}
)

# Step 3: Add documents (Chroma automatically creates embeddings using default model)
print("Adding documents to vector database...")
documents = [
    "A 401(k) is a retirement savings plan sponsored by employers. Employees contribute pre-tax income, and employers often match contributions up to a certain percentage.",
    "An ETF (Exchange-Traded Fund) is a basket of securities that trades on stock exchanges like a stock. ETFs offer diversification and lower fees than mutual funds.",
    "Dollar-cost averaging involves investing a fixed amount regularly regardless of market conditions. This strategy reduces the impact of market volatility.",
    "A bond is a fixed-income investment where you lend money to a corporation or government. Bonds pay periodic interest and return the principal at maturity.",
    "Asset allocation is the strategy of dividing investments among different asset categories like stocks, bonds, and cash. It balances risk and return based on your goals and timeline.",
]

collection.add(
    documents=documents,
    ids=["doc1", "doc2", "doc3", "doc4", "doc5"]
)

print(f"✅ Added {len(documents)} documents\n")

# Step 4: Query for similar documents
print("=" * 70)
query = "What's a good way to save for retirement through my employer?"
print(f"🔍 Query: {query}\n")

results = collection.query(
    query_texts=[query],
    n_results=2  # Return top 2 most similar documents
)

# Display results
print("📄 Most similar documents:")
for i, (doc, distance) in enumerate(zip(
    results['documents'][0],
    results['distances'][0]
), 1):
    print(f"\n{i}. Distance: {distance:.3f} (lower = more similar)")
    print(f"   Content: {doc}")
