from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

from dotenv import load_dotenv

load_dotenv()

llm = init_chat_model(
    model="ollama:gpt-oss:20b",
    base_url="http://192.168.10.93:11434"
)

def get_weather(city: str):
    """Get weather fro given city"""
    return f"It's alway sunny in {city}!"

agent = create_agent(
    model="deepseek:deepseek-chat",
    tools=[get_weather]
)

# for event in agent.stream(
#     {"messages": [{"role": "user", "content": "What's the weather in SF?"}]}, 
#     stream_mode="values" # message by message
# ):
    # messages = event["messages"]
    # print(f"历史消息：{len(messages)}条")
    # messages[-1].pretty_print() # 打印最后一条消息
    # for message in messages:
    #     message.pretty_print()

for chunk in agent.stream(
    {"messages": [{"role": "user", "content": "What's the weather in SF?"}]}, 
    stream_mode="messages" # token by token
):
    print(chunk[0].content, end="")
    # print(chunk)
    # (AIMessageChunk(
    #   content='I', 
    #   additional_kwargs={}, 
    #   response_metadata={'model_provider': 'deepseek'}, 
    #   id='lc_run--019c8fdd-0b25-7c30-81e8-912c53e25a2e', 
    #   tool_calls=[], invalid_tool_calls=[], tool_call_chunks=[]
    #  ), 
    #  {
    #   'langgraph_step': 1, 
    #   'langgraph_node': 'model', 
    #   'langgraph_triggers': ('branch:to:model',), 
    #   'langgraph_path': ('__pregel_pull', 'model'), 
    #   'langgraph_checkpoint_ns': 'model:9ec46a8a-3b11-863d-3b64-ec0cbd6f0fac', 
    #   'checkpoint_ns': 'model:9ec46a8a-3b11-863d-3b64-ec0cbd6f0fac', 
    #   'ls_provider': 'deepseek', 
    #   'ls_model_name': 'deepseek-chat', 
    #   'ls_model_type': 'chat', 
    #   'ls_temperature': None
    #   }
    # )
