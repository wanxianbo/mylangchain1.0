### 更复杂一点的智能体 create_agent
## 大模型 model
## 系统提示词：system_prompt 
## 工具：tools 用户消息传递参数
# => 工具运行时上下文传递参数：context_schema 
## 记忆管理 checkpointer
## 结构化输出：response_format 

from socket import timeout
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain.tools import tool, ToolRuntime
from langchain.chat_models import init_chat_model

from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

# 系统提示词
SYSTEM_PROMPT = """You are an expert weather forecaster, who speaks in puns.

You have access to two tools:

- get_weather_for_location: use this to get the weather for a specific location
- get_user_location: use this to get the user's location

If a user asks you for the weather, make sure you know the location. If you can tell from the question that they mean wherever they are, use the get_user_location tool to find their location.
用中文回答
"""

@tool
def get_weather_for_location(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

# 数据类注解；可以使用set、get函数
@dataclass
class Context:
    """Custom runtime contenxt schema"""
    user_id: str

@tool
def get_user_location(runtime: ToolRuntime[Context]) -> str:
    """Retrieve user information based on user ID."""
    user_id = runtime.context.user_id
    return "Florida" if user_id == "1" else "SF"

# 结构化输出
@dataclass
class ResponseFormat:
    """Response schema for the agent."""
    # A punny response (always required)
    punny_response: str
    # Any interesting information about the weather if available
    weather_conditions: str | None = None

# 记忆管理
checkpointer = InMemorySaver()

# 定义模型
model = init_chat_model(
    model="deepseek:deepseek-chat",
    temperature=0.5,
    timeout=10,
    max_token=1000
)

# 创建智能体
agent = create_agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
    tolls=[get_weather_for_location, get_user_location],
    context_schema=Context,
    response_format=ResponseFormat,
    checkpointer=checkpointer
)

# 配置 thread_id
config = {"configurable": {"thread_id": "1"}}

# 运行智能体
# 第一轮回答
response = agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather outside?"}]},
    config=config,
    context=Context(user_id="1")
)

print(response["structured_response"])

# 第二轮回答
response = agent.invoke(
    {"messages": [{"role": "user", "content": "thank you!"}]},
    config=config,
    context=Context(user_id="1")
)

print(response["structured_response"])