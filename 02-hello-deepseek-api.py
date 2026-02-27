from langchain_deepseek import ChatDeepSeek
from langchain.chat_models import init_chat_model

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
    temperature=0.1,
    timeout=30,
    max_tokens=1000,
    max_retries=2
)

for chunk in model.stream("来一段宋词"):
    print(chunk.content, end="", flush=True)

