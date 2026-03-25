## deepagent: planning file system(agent) subagent
## demo: research agent: research report

## pip install deepagents

### 过程：
# write_tools, todo list
# internet_search -> update todo list
# write_file

from langchain.chat_models import init_chat_model
# from langchain.agents import create_agent
from deepagents import create_deep_agent


from dotenv import load_dotenv

from tavily import TavilyClient
from typing import Literal

load_dotenv()

tavilyClient = TavilyClient()

def internet_search(
    query: str,
    max_results: int = 5,
    topic: Literal["general", "news", "finance"] = "general",
    include_raw_content: bool = False
):
    """RUN A WEB SEARCH"""
    return tavilyClient.search(
        query=query,
        max_results=max_results,
        topic=topic,
        include_raw_content=include_raw_content
    )

# 系统提示词
research_instructions = """
你是一个专业的研究院，你的任务是进行彻底的研究院并撰写一份完整的报告。

你可以使用一下工具：
- internet_search：用户搜索互联网信息

请确保：
1.进行全面的搜索来收集信息
2.验证信息的准确性
3.组织信息并撰写结构化报告
4.最多调用3次 internet_search，避免无限检索
"""

# 定义模型
model = init_chat_model(
    model="deepseek:deepseek-chat",
    temperature=0.5,
    timeout=60,
    max_tokens=1000
)

agent = create_deep_agent(
    model=model,
    tools=[internet_search],
    system_prompt=research_instructions
)

for step in agent.stream(
        {"messages": [{"role": "user", "content": "什么是LangGraph？详细介绍它的功能、用途和主要特点。"}]},
        stream_mode="values"
    ):
        if "files" in step:
              print("*"*50)
              print(step["files"])
        step["messages"][-1].pretty_print()
