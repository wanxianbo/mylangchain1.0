from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

from dotenv import load_dotenv

load_dotenv()

model =init_chat_model(
    model="ollama:deepseek-r1:8b",
    # model="ollama:gpt-oss:20b",
    base_url="http://192.168.10.93:11434"
)

agent = create_agent(
    # model="deepseek:deepseek-chat"
    model=model,
)

# 第一段问答
result = agent.invoke({"messages": [{"role": "user", "content": "来段宋词"}]})
messages = result["messages"]
for message in messages:
    message.pretty_print()

his_messages = messages

# 第二段问答
his_messages.append({"role": "user", "content": "再来"})
result = agent.invoke({"messages": his_messages})
messages = result["messages"]
for message in messages:
    message.pretty_print()