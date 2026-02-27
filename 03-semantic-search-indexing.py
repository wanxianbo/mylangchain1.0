## 语义搜索引擎
# 1.Documents and document loaders  加载文档，解析文档为Document对象
# 2.Text splitting  文本切分，将文档切分为更小的文本块 构建成Chunk对象
# 3.Embeddings  使用embedding模型将文本块转换为向量表示，构建成Vector对象
# 4.Vector stores and retrievers    使用向量存储库存储向量，并实现检索功能
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

file_path = "nke-10k-2023.pdf"

loader = PyPDFLoader(file_path)

docs = loader.load()

# print(len(docs))
# print(docs[0])
# 107
# page_content='' metadata={'producer': 'EDGRpdf Service w/ EO.Pdf 22.0.40.0', 
# 'creator': 'EDGAR Filing HTML Converter', 'creationdate': '2023-07-20T16:22:00-04:00', 
# 'title': '0000320187-23-000039', 'author': 'EDGAR Online, a division of Donnelley Financial Solutions', 
# 'subject': 'Form 10-K filed on 2023-07-20 for the period ending 2023-05-31', 
# 'keywords': '0000320187-23-000039; ; 10-K', 'moddate': '2023-07-20T16:22:08-04:00', 
# 'source': 'nke-10k-2023.pdf', 'total_pages': 107, 'page': 0, 'page_label': '1'}

# 2.文本切分 Chunks

text_spiltter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    add_start_index=True
)

all_splits = text_spiltter.split_documents(docs)

# print(len(all_splits))
# print(all_splits[0])
# 516
# page_content='' metadata={'producer': 'EDGRpdf Service w/ EO.Pdf 22.0.40.0', 'creator': 'EDGAR Filing HTML Converter', 'creationdate': '2023-07-20T16:22:00-04:00', 
# 'title': '0000320187-23-000039', 'author': 'EDGAR Online, a division of Donnelley Financial Solutions', 
# 'subject': 'Form 10-K filed on 2023-07-20 for the period ending 2023-05-31', 'keywords': '0000320187-23-000039; ; 10-K', 
# 'moddate': '2023-07-20T16:22:08-04:00', 'source': 'nke-10k-2023.pdf', 'total_pages': 107, 'page': 0, 'page_label': '1', 'start_index': 0}

# 3.向量化 Embeddings
from langchain_ollama import OllamaEmbeddings

embedding = OllamaEmbeddings(model="nomic-embed-text")
vector_0 = embedding.embed_query(all_splits[0].page_content)

# 768
print(len(vector_0))
print(vector_0)
# vector_0 其实他的索引

# 4.向量存储和检索 Vector stores and retrievers
from langchain_chroma import Chroma

vector_store = Chroma(
    collection_name="example_collection",
    embedding_function=embedding,
    persist_directory="./chroma_langchain_db",
)

ids = vector_store.add_documents(all_splits)

# 516
print(len(ids))
print(ids)