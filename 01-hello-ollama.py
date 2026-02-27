# model class
from langchain_ollama import ChatOllama
from langchain.chat_models import init_chat_model

model = ChatOllama(
    model="deepseek-r1:1.5b",
    base_url="http://localhost:11434",
    temperature=0.1,
    max_tokens=1000,
    timeout=30
)

# model = init_chat_model(
#     model="ollama:deepseek-r1:1.5b",
#     base_url="http://localhost:11434",
#     temperature=0.1,
#     timeout=30,
#     max_tokens=1000
# )

# for chunk in model.stream("再来一段1949年毛泽东的诗词"):
#     print(chunk.content, end="", flush=True)

response = model.invoke("请介绍下自己？")
print(response.content)