from typing import List
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

# 嵌入模型初始化
embedding = OllamaEmbeddings(
    model="qwen3-embedding:8b",
    base_url="http://192.168.10.93:11434"
    )

score_measures= [
    "default",    # dfault -> l2
    "cosine",     # 用两个向量的夹角度量相似度
    "l2",         # 用两个向量的欧氏距离度量相似度
    "ip"          # 用两个向量的内积（点积）度量相似度
]

# 创建向量库和4个collection
persist_dir = "./chroma_score_db"
vector_stores=[]
for score_measure in score_measures:
    collection_metadata = {"hnsw:space": score_measure}
    if score_measure == "default":
        collection_metadata = None
    
    collection_name = f"my_collection_{score_measure}"
    vector_stores.append(Chroma(
        collection_name=collection_name,
        embedding_function=embedding,
        persist_directory=persist_dir,
        collection_metadata=collection_metadata,
    ))

def indexing(docs: List[Document]):
    print("\n加入文档")
    for vector_store in vector_stores:
        ids = vector_store.add_documents(docs)
        print(f"\n集合：{vector_store._collection.name}")
        print(f"ids: {ids}")

def query_with_score(query: str):
    for i in range(len(vector_stores)):
        print(f"\n搜索:{query}")
        results = vector_stores[i].similarity_search_with_score(query)
        for doc, score in results:
            print(f"doc: {doc.page_content}", end="")
            print(f"{score_measures[i]}的score:{score}")

print("======================开始索引========================")
docs = [
    Document(page_content="这个小米手机很好用"),
    Document(page_content="我国陕西地区盛产小米")
]
# indexing(docs)

# query_with_score("我刚和朋友通完话")
# query_with_score("what is you name?")
# query_with_score("I just called my friend")
# query_with_score("我国幅员辽阔，物产丰富")
query_with_score("雷军有点烦")