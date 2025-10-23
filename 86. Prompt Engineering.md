# Prompt Engineering

## What

Crafting effective instructions to get desired outputs from LLMs.

**Core idea:** How you ask = what you get.

```
❌ "Write code"
✅ "Write a Python function that validates email addresses using regex. Include docstring."
```

## Why

- Better accuracy (40% → 95%)
- Reduces hallucinations  
- Saves tokens/money
- Consistent outputs

LLMs don't "understand" - they predict the most likely next words based on patterns in training data.
Good prompts work because they:
- Activate relevant training examples
- Narrow the probability space
- Establish clear patterns to follow
- Reduce ambiguity
That's why "Let's think step by step" works - those exact words (or similar) appeared in reasoning examples during training, so saying them activates that reasoning behavior!

## How Tokens Work

**Tokens = Words/subwords that LLMs process**

```
Text: "Hello world"
Tokens: ["Hello", " world"] = 2 tokens

Text: "I'm coding"
Tokens: ["I", "'m", " coding"] = 3 tokens
```

**Rough estimates:**
- 1 token ≈ 0.75 words (English)
- 1,000 tokens ≈ 750 words
- 1,000 tokens ≈ $0.01-0.03 (depending on model)

**Why it matters:** Every token costs money, so shorter prompts = cheaper!

## Core Techniques

### 1. Zero-Shot
Ask directly without examples.

```
You are a Python expert. Write a function to calculate fibonacci numbers.
```

### 2. Few-Shot
Provide examples.

```
Classify sentiment:

"This product is amazing!" → positive
"Terrible quality." → negative
"It's okay." → neutral
"Best purchase ever!" → ?
```

### 3. Chain-of-Thought (CoT)
Ask for reasoning.

```
Q: Roger has 5 tennis balls. He buys 2 cans of 3 balls each. How many total?
Let's think step by step:

A: Start: 5 balls
   Bought: 2 cans × 3 = 6 balls
   Total: 5 + 6 = 11 balls
```

**Trigger:** "Let's think step by step"

### 4. Structured Output
Request specific format.

```
Extract as JSON:

Text: "John Smith, age 30, Seattle, engineer"

Output:
{"name": "John Smith", "age": 30, "city": "Seattle", "job": "engineer"}
```

## Basic Template

```
[Role] (optional)
You are a senior Python developer.

[Task] (required)
Write a function that...

[Constraints] (optional)
- Use type hints
- Handle errors
- Keep under 20 lines

[Format] (optional)
Return as JSON/code/markdown
```

## Best Practices

**Be specific:**
```
❌ "Make it better"
✅ "Add comments and extract magic numbers into constants"
```

**Give context:**
```
❌ "Fix this"
✅ "This Python function throws TypeError with list input"
```

**Use delimiters:**
```
Translate text between ###:
###
Hello world
###
```

**Specify format:**
```
List in numbered format, one per line
```

**Prevent errors:**
```
If you don't know, say "I don't know" instead of guessing.
```

## Token Efficiency

**Save money with shorter prompts:**

**Be concise:**
```
❌ "Please provide a comprehensive analysis of the following data..."
✅ "Analyze this data and provide 3 key insights:"
```

**Remove filler words:**
```
❌ "I would like you to please help me with..."
✅ "Help me with:"
```

**Use abbreviations:**
```
❌ "Please provide a detailed explanation"
✅ "Explain:"
```

**Combine instructions:**
```
❌ "First, analyze the code. Then, identify bugs. Finally, suggest fixes."
✅ "Analyze code, identify bugs, suggest fixes:"
```

**Result:** 50-70% fewer tokens = significant cost savings!

## When to Use What

| Use Case | Solution |
|----------|----------|
| Simple task | Zero-shot |
| Pattern matching | Few-shot |
| Math/logic | Chain-of-Thought |
| Need knowledge | RAG |
| Custom style | Fine-tuning |

## Common Patterns

**Multi-step:**
```
Complete in 3 steps:
1. Analyze requirements
2. Design solution  
3. Provide code
```

**Conditional:**
```
If code has bugs, flag with "🚨"
If secure, respond "✅ Secure"
```

**System prompt (chat apps):**
```
System: You are a helpful coding assistant that provides concise answers with examples.

User: How do I reverse a string?
```

## Example: Data Extraction

```
Extract information as JSON. If field missing, use null.

Fields: date (YYYY-MM-DD), amount (number), description (string)

Text: "Bought groceries on 10/15/2024 for $127.50"

Output:
```

## Resources

- Cursor with Claude Model
- Anthropic Prompt Library: https://docs.anthropic.com/en/prompt-library/library
- OpenAI Guide: https://platform.openai.com/docs/guides/prompt-engineering

