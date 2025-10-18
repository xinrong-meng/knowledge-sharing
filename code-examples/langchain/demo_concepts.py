"""
Practical demonstration of LCEL and ChatPromptTemplate
"""

from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatAnthropic(model="claude-3-5-haiku-latest", temperature=0.7)

# ============================================
# ChatPromptTemplate: Reusable prompt structure
# ============================================

# Define once, reuse many times
translator_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a translator. Translate from {source_lang} to {target_lang}."),
    ("user", "{text}")
])

# Use it multiple times with different inputs
print("Example 1: English to Spanish")
chain = translator_prompt | llm | StrOutputParser()
result1 = chain.invoke({
    "source_lang": "English",
    "target_lang": "Spanish", 
    "text": "Hello, how are you?"
})
print(f"Result: {result1}\n")

print("Example 2: English to French")
result2 = chain.invoke({
    "source_lang": "English",
    "target_lang": "French",
    "text": "Good morning!"
})
print(f"Result: {result2}\n")

# ============================================
# LCEL: Composable chains
# ============================================

print("="*50)
print("LCEL: Building modular chains\n")

# You can break it down:
step1 = translator_prompt
step2 = llm
step3 = StrOutputParser()

# Then compose them:
my_chain = step1 | step2 | step3

# Or add more steps:
summary_prompt = ChatPromptTemplate.from_template(
    "Summarize this in 5 words: {text}"
)

# Chain multiple operations
multi_step_chain = summary_prompt | llm | StrOutputParser()

print("Multi-step example:")
summary = multi_step_chain.invoke({
    "text": "LangChain is a framework for developing applications powered by language models. It enables applications that are context-aware and reason."
})
print(f"Summary: {summary}")

