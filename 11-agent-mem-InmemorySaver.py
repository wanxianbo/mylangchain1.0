## 消息列表的内存管理
## 通过congig 实现多会话管理
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver

from dotenv import load_dotenv

load_dotenv()

checkpointer = InMemorySaver()

model =init_chat_model(
    model="ollama:deepseek-r1:8b",
    # model="ollama:gpt-oss:20b",
    base_url="http://192.168.10.93:11434"
)

agent = create_agent(
    model="deepseek:deepseek-chat",
    # model=model,
    checkpointer=checkpointer
)

# 设置会话id
config = {"configurable": {"thread_id": "1"}}

# 第一段问答
result = agent.invoke(
    {"messages": [{"role": "user", "content": "来段宋词"}]},
    config=config
    )
messages = result["messages"]
for message in messages:
    message.pretty_print()

# 第二段问答
result = agent.invoke(
    {"messages": [{"role": "user", "content": "再来"}]},
    config=config
    )
messages = result["messages"]
for message in messages:
    message.pretty_print()