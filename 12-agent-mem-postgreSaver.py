## 消息列表的内存管理
## 通过congig 实现多会话管理
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.postgres import PostgresSaver

from dotenv import load_dotenv

load_dotenv()

model =init_chat_model(
    model="ollama:deepseek-r1:8b",
    # model="ollama:gpt-oss:20b",
    base_url="http://192.168.10.93:11434"
)

# 上下文管理
DB_URL = "postgresql://postgres:postgres@192.168.10.5:5432/langchain?sslmode=disable"
with PostgresSaver.from_conn_string(DB_URL) as checkpointer:
# with PostgresSaver.from_conn_string(
#     host="192.168.10.5",
#     port=5432,
#     database="langchain",
#     user="postgres",
#     password="postgres",
#     args={"sslmode": "disable"}
# ) as checkpointer:
    # 创建表，只运行一次，或者直接创建好
    # checkpointer.setup()

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