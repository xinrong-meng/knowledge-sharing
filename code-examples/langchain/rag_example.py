"""
Bare minimum RAG (Retrieval-Augmented Generation) example
Prerequisites: uv add langchain-anthropic langchain-community faiss-cpu langchain-huggingface sentence-transformers
Set environment variable: ANTHROPIC_API_KEY
"""

from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

# 1. Create some documents (your knowledge base)
documents = [
    "TechCorp's vacation policy: Full-time employees receive 15 days of paid vacation per year. Part-time employees receive pro-rated vacation based on hours worked. Unused vacation can be carried over up to 5 days into the next year.",
    "TechCorp's remote work policy: Employees in engineering and design departments can work remotely up to 3 days per week. Sales and customer support must be in office 4 days per week. All employees must attend Monday morning standups in person.",
    "TechCorp's parental leave: New parents receive 12 weeks of paid parental leave. This applies to both biological and adoptive parents. Leave must be taken within the first year of the child's birth or adoption.",
    "TechCorp's health benefits: All full-time employees are eligible for health, dental, and vision insurance starting on their first day. The company covers 80% of premium costs. Part-time employees (20+ hours/week) are eligible after 90 days.",
    "TechCorp's professional development: Each employee has an annual budget of $2,000 for courses, conferences, or certifications. Engineering staff have an additional $1,000 for technical conferences. Budgets reset on January 1st and do not roll over.",
    "TechCorp's work hours: Standard work hours are 9 AM to 5 PM, Monday through Friday. Engineering teams have flexible hours and can start anytime between 7 AM and 11 AM. Overtime is paid at 1.5x rate for non-exempt employees.",
    "TechCorp's equipment policy: All employees receive a laptop on day one. Engineers can choose between Mac or PC. Equipment must be returned upon termination. Personal use of company equipment is allowed for reasonable personal activities.",
]

# 2. Create a vector store with real embeddings (understands meaning!)
print("Loading embeddings model (first time may take a moment)...")
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

print("Creating vector store...")
vectorstore = FAISS.from_texts(
    documents,
    embedding=embeddings
)

# 3. Create a retriever
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

# 4. Set up the LLM
llm = ChatAnthropic(model="claude-3-5-haiku-latest", temperature=0.7)

# 5. Create a RAG prompt
rag_prompt = ChatPromptTemplate.from_template(
    """Answer the question based on the following context:

Context: {context}

Question: {question}

Answer:"""
)

# 6. Build the RAG chain
def rag_chain(question):
    # Retrieve relevant documents
    relevant_docs = retriever.invoke(question)
    
    # Show which documents were retrieved (for debugging)
    print(f"\n📄 Retrieved documents:")
    for i, doc in enumerate(relevant_docs, 1):
        print(f"  {i}. {doc.page_content[:80]}...")
    
    context = "\n\n".join([doc.page_content for doc in relevant_docs])
    
    # Create the chain
    chain = rag_prompt | llm | StrOutputParser()
    
    # Get answer
    return chain.invoke({"context": context, "question": question})

# 7. Test it out
if __name__ == "__main__":
    questions = [
        "I'm a part-time engineer working 25 hours per week. When am I eligible for health insurance and how much vacation do I get?",
        "If I'm an engineer who just had a baby, can I take parental leave and work remotely when I return? What are my options?",
        "I want to attend a $1,500 AI conference and take a $800 Python course this year. I'm a software engineer. Can my professional development budget cover both?",
        "What's the latest I can start work if I'm on the engineering team, and what happens to my unused vacation days at the end of the year?",
        "Compare the remote work flexibility between engineering and sales departments.",
    ]
    
    for q in questions:
        print(f"\n{'='*70}")
        print(f"❓ Q: {q}")
        print(f"{'='*70}")
        answer = rag_chain(q)
        print(f"\n✅ A: {answer}")

