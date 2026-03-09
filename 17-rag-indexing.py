## 索引
# 1.读取网页， Document List[Document]
# 2.分割文本，文本段（chunk）， Document， List[Document]
# 3.向量化，文本段（chunk） => 向量， Document
# 4.存储向量，向量 => 向量库（Vector Store）

import bs4
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


page_url = "https://news.cnr.cn/native/gd/kx/20260122/t20260122_527502950.shtml"

bs4_strainer = bs4.SoupStrainer()

loader = WebBaseLoader(
    web_path=page_url,
    bs_kwargs={"parse_only": bs4_strainer}
)

docs = loader.load()
print(len(docs))
print(docs[0])


# 2.文本切分 Chunks

text_spiltter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    add_start_index=True
)

all_splits = text_spiltter.split_documents(docs)

# print(len(all_splits))
# print(all_splits[0])

# 3.向量化 Embeddings
from langchain_ollama import OllamaEmbeddings

embedding = OllamaEmbeddings(model="nomic-embed-text:latest", base_url="http://192.168.10.93:11434")
# vector_0 = embedding.embed_query(all_splits[0].page_content)

# 768
# print(len(vector_0))
# print(vector_0)
# vector_0 其实他的索引

# 4.向量存储和检索 Vector stores and retrievers
from langchain_chroma import Chroma

vector_store = Chroma(
    collection_name="rag_collection",
    embedding_function=embedding,
    persist_directory="./chroma_rag_db",
)

ids = vector_store.add_documents(all_splits)

# 516
print(len(ids))
print(ids)