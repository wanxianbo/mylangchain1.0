### 更复杂一点的智能体 create_agent
## 大模型 model
## 系统提示词：system_prompt 
## 工具：tools 用户消息传递参数
# => 工具运行时上下文传递参数：context_schema 
## 记忆管理 checkpointer
## 机构化输出：response_format 

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

If a user asks you for the weather, make sure you know the location. If you can tell from the question that they mean wherever they are, use the get_user_location tool to find their location."""

@tool
class Context:
    """Custom runtime contenxt schema"""
    user_id: str

@tool
def get_user_location(runtime: ToolRuntime[Context]) -> str:
    """Retrieve user information based on user ID."""
    user_id = runtime.context.user_id
    return "Florida" if user_id == "1" else "SF"

model = init_chat_model(
    model="deepseek:deepseek-chat",
    temperature=0.5,
    timeout=10,
    max_token=1000
)