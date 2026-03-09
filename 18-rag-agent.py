from langchain_deepseek import ChatDeepSeek
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain_chroma import Chroma
from langchain.tools import tool


from dotenv import load_dotenv

load_dotenv()

# model = ChatDeepSeek(
#     model="deepseek-chat", # deepseek-reasoner
#     temperature=0.1,
#     max_tokens=1000,
#     timeout=30,
#     max_retries=2
# )

model = init_chat_model(
    model="deepseek:deepseek-chat",
    base_url="http://192.168.10.93:11434",
    temperature=0.8,
    timeout=30,
    max_tokens=1000
)

from langchain_ollama import OllamaEmbeddings

embedding = OllamaEmbeddings(model="nomic-embed-text:latest", base_url="http://192.168.10.93:11434")
# vector_0 = embedding.embed_query(all_splits[0].page_content)

vector_store = Chroma(
    collection_name="rag_collection",
    embedding_function=embedding,
    persist_directory="./chroma_rag_db",
)

@tool(response_format="content_and_artifact")
def retrieve_context(query: str):
    """Retrieve information to help answer the question."""
    retrieve_docs = vector_store.similarity_search(query, k=2)
    context = "\n".join([(f"Source:{doc.metadata}\nContent:{doc.page_content}") for doc in retrieve_docs])
    return context, retrieve_docs

system_prompt = """
    你可以使用信息检索工具，回答用的问题
"""

agent = create_agent(
    model=model,
    tools=[retrieve_context],
    system_prompt=system_prompt
)

results = agent.invoke(
    {"messages": [{"role": "user", "content": "讲一下 3i/Atlas"}]}
)

messages = results["messages"]
print(f"历史消息：{len(messages)}条")
for message in messages:
    message.pretty_print()