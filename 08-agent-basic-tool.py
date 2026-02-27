from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

from dotenv import load_dotenv

load_dotenv()

model =init_chat_model(
    # model="ollama:deepseek-r1:8b",
    model="ollama:gpt-oss:20b",
    base_url="http://192.168.10.93:11434"
)

def get_weather(city: str):
    """Get weather fro given city"""
    return f"It's alway sunny in {city}!"

agent = create_agent(
    model="deepseek:deepseek-chat",
    # model=model,
    tools=[get_weather],
)

# {'__start__': <langgraph.pregel._read.PregelNode object at 0x10be99bd0>, 
# 'model': <langgraph.pregel._read.PregelNode object at 0x10be99e50>, 
# 'tools': <langgraph.pregel._read.PregelNode object at 0x10bebf150>}
print(agent.nodes)
print("=======================================")
result = agent.invoke({"messages": [{"role": "user", "content": "What's the weather in SF?"}]})
messages = result["messages"]
for message in messages:
    message.pretty_print()