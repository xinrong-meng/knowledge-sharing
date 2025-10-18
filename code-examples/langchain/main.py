"""
Bare minimum LangChain example - Essential Components
Prerequisites: pip install langchain-anthropic
Set environment variable: ANTHROPIC_API_KEY
"""

from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. Initialize the chat model
llm = ChatAnthropic(
    model="claude-3-5-haiku-latest",
    temperature=0.7
)

# 2. Create a prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that specializes in {topic}."),
    ("user", "{question}")
])

# 3. Create an output parser
output_parser = StrOutputParser()

# 4. Chain them together using LCEL (LangChain Expression Language)
chain = prompt | llm | output_parser

# 5. Invoke the chain
response = chain.invoke({
    "topic": "programming jokes",
    "question": "Tell me a funny joke about Python programming."
})

# 6. Print the response
print("Response:", response)

# Example 2: Simple question answering
print("\n" + "="*50 + "\n")

qa_prompt = ChatPromptTemplate.from_template(
    "Answer this question concisely: {question}"
)

qa_chain = qa_prompt | llm | output_parser

answer = qa_chain.invoke({"question": "What is LangChain?"})
print("Answer:", answer)
