from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

embedding = OllamaEmbeddings(
    model="nomic-embed-text",
    base_url="http://192.168.10.93:11434"
)

vector_store = Chroma(
    collection_name="example_collection",
    embedding_function=embedding,
    persist_directory="./chroma_langchain_db",
)

# 1.向量库进行相似度查询
# 相似度查询
results = vector_store.similarity_search(
    "How many distribution centers does Nike have in the US?"
)

for index, result in enumerate(results):
    print(index)
    print(result.page_content[:100])

# 带分数的相似度的查询
print("使用向量带分数进行相似度查询============================")
results = vector_store.similarity_search_with_score(
    "How many distribution centers does Nike have in the US?")

for doc, score in results:
    print(score)
    print(doc.page_content[:100])

# 使用向量进行相似度查询
print("使用向量进行相似度查询=================================")
embedding_vector = embedding.embed_query(
    "How many distribution centers does Nike have in the US?")

results = vector_store.similarity_search_by_vector(embedding=embedding_vector)

for index, result in enumerate(results):
    print(index)
    print(result.page_content[:100])


print("使用检索器进行相似度查询=================================")
# chain:-langchain: 大模型，提示词模版，tools， output，外部 API接口-Runable
from typing import List

from langchain_core.documents import Document
from langchain_core.runnables import chain

@chain
def retriever(query: str) -> List[Document]:
    return vector_store.similarity_search(query, k=1)

results = retriever.invoke("How many distribution centers does Nike have in the US?")
for index, result in enumerate(results):
    print(index)
    print(result.page_content[:100])

batch_results = retriever.batch(["How many distribution centers does Nike have in the US?", 
                 "What is the name of the CEO of Nike?"])
for result in batch_results:
    print(result)