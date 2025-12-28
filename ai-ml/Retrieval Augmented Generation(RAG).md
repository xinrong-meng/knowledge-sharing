# Retrieval Augmented Generation(RAG)

## What

The RAG model combines a language model with an information retrieval system to improve performance on 
knowledge-intensive tasks. It uses a **retriever** to find relevant information and a **generator** to produce accurate and 
detailed responses. This approach enhances the accuracy and flexibility of language models by allowing them to 
**access** and use **up-to-date** external information.

## Why

Traditional language models like GPT store knowledge in their _parameters*_ but struggle to update knowledge and 
sometimes produce incorrect information (hallucinations).

Solution: By adding a retrieval component, the model can look up relevant information from a large database (like 
Wikipedia) to generate more accurate and up-to-date responses.

_*parameters_: Parameters in machine learning models are the internal variables that the model learns from the 
training data. These parameters help the model make predictions or generate outputs based on new inputs. 	In the 
context of language models, these parameters capture patterns, relationships, and knowledge from the text data they 
are trained on.

## How RAG works
- Two Main Parts
  - Retriever: Finds relevant documents based on the input question.
  - Generator: Uses these documents to help generate a detailed and accurate response.
- Viz (in paper)
  - Query Encoder: Turns the input question into a format the retriever can use.
  - Retriever: Searches a large database for relevant documents.
  - Document Index: The database of documents (e.g., Wikipedia).
  - Generator: Uses the input question and retrieved documents to generate the final answer.
  
![image](https://github.com/xinrong-meng/knowledge-sharing/assets/3375461/15691472-33eb-49df-8daa-ca8394c6e1bd)

_*Parametric Memory_: Knowledge stored within the model’s parameters.

_*Non-Parametric Memory_: External knowledge sources, like databases or documents, that the model can look up.

## Types of RAG Models

- RAG-Sequence
  - The entire response is generated based on each of the top-K retrieved documents.
  - The final probability is a weighted sum of the likelihoods from each document, taking into account their 
	relevance to the query.
- RAG-Token
  - Each token in the response can be influenced by different retrieved documents.
  - The final probability is a product of summed likelihoods for each token, considering the top-K documents’ 
	relevance to the query for each token individually.

Use cases:
- RAG-Sequence:
  - Best For: Simple, direct questions with answers typically found in a single document.
  - Stength: Coherent context from a single source.
  - Use Cases: Simple factual questions, clear source of truth scenarios.
- RAG-Token:
  - Best For: Complex questions needing comprehensive answers from multiple sources. 
  - Stength: High precision by combining information from various documents.
  - Use Cases: Detailed explanations, multi-faceted questions, high-precision tasks.

## Example RAG Application

![image](https://github.com/xinrong-meng/knowledge-sharing/assets/3375461/5bb0bf9b-8aef-42f2-b8cc-7a59ccc5352a)

RAG applications require a pipeline and a chain component to perform the following:

- Indexing: A pipeline that ingests data from a source and indexes it. This data can be structured or unstructured.
- Retrieval and generation: This is the actual RAG chain. It takes the user query and retrieves similar data from the 
index, then passes the data, along with the query, to the LLM model.

The following describes the details of the RAG chain in the context of an unstructured data RAG example.


![image](https://github.com/xinrong-meng/knowledge-sharing/assets/3375461/45e851ee-f80b-4b06-aa7a-7ad331878fe6)


1. Embed the request using the same _embedding model*_ that was used to embed the data in the knowledge base.
2. Query the _vector database*_ to do a similarity search between the embedded request and the embedded data chunks in 
the vector database.
3. Retrieve the data chunks that are most relevant to the request.
4. Feed the relevant data chunks and the request to a customized LLM. The data chunks provide context that helps the 
LLM generate an appropriate response. Often, the LLM has a template for how to format the response.
5. Generate a response.

_*Vector Database_: A vector database indexes and stores vector embeddings for fast retrieval and similarity search.

![image](https://github.com/xinrong-meng/knowledge-sharing/assets/3375461/1c42e7b1-fa0f-4598-a854-ecbcf9a7de9b)

![image](https://github.com/xinrong-meng/knowledge-sharing/assets/3375461/95704f74-58ed-439b-acc2-31ccf83ad848)

_*embedding model_:
When both the question and the documentation are embedded using the same model, they are represented in the same 
vector space. This means their embeddings (vector representations) can be directly compared.

## Challenges in RAG Models

| Challenge                          | Description                                                                                                         |
|------------------------------------|---------------------------------------------------------------------------------------------------------------------|
| Computational Complexity           | The process of retrieving relevant documents and generating responses requires significant computational resources. |
| Quality of Retrieved Documents     | The relevance and quality of retrieved documents significantly impact the accuracy of the generated response.        |
| Integration of Components          | Effective integration of the retrieval and generation components is crucial for optimal performance.                 |
| Handling Ambiguity and Noise       | Dealing with ambiguous queries and noisy data complicates the retrieval and generation processes.                    |
| Scalability                        | Scaling the model to handle large volumes of data and queries efficiently is challenging.                            |
| Bias and Fairness                  | The model can inherit biases from the training data and retrieved documents, leading to biased responses.            |
| Updating Non-Parametric Memory     | Keeping the document corpus up to date with the latest information is resource-intensive and challenging.            |


## References

https://arxiv.org/pdf/2005.11401

https://docs.databricks.com/en/generative-ai/retrieval-augmented-generation.html

What is Retrieval-Augmented Generation (RAG)?
https://www.youtube.com/watch?v=T-D1OfcDW1M

Vector Databases simply explained! (Embeddings & Indexes)
https://www.youtube.com/watch?v=dN0lsF2cvm4

GPT-4o
