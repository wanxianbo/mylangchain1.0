## 1.理解RAG （Retrieval-augmented generation）检索增强生成
# 大模型交互：问题 => 大模型 => 回答(生成式)
# 基于 RAG 的大模型交互
# 增强【问题 + （检索：根据问题找到相似的文本）】=> 大模型 => 回答(生成式)
## 从大模型的角度：没有区别，RAG 不是大模型技术，是如何更好的用大模型的技术
# RAG 可以看作是一种提示词工程技术

## 2. 大模型局限性：
# 1. 实效问题：大模型的知识截止日期是固定的，无法获取最新的信息。
# 2. 公开数据 大模型幻觉

# 3. 解决方案
#   1）大模型不断实时更新，不可能方案
#   3）微调：用私有数据，新的数据，（标注）局部的训练，垂直行业大模型
#   2）RAG：检索增强生成，结合外部知识库，提供最新的信息，解决大模型的实效问题和幻觉问题。
# https://github.com/datawhalechina/all-in-rag

from langchain_deepseek import ChatDeepSeek
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent

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
    model="ollama:deepseek-r1:8b",
    base_url="http://192.168.10.93:11434",
    temperature=0.1,
    timeout=30,
    max_tokens=1000
)

agent = create_agent(
    model=model
)

results = agent.invoke(
    {"messages": [{"role": "user", "content": "讲一下 3i/Atlas"}]}
)

messages = results["messages"]
print(f"历史消息：{len(messages)}条")
for message in messages:
    message.pretty_print()
