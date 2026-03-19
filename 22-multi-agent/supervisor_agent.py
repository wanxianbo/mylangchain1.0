### 说明
## agent: model tools system_prompt checkpointer middleware
### 多 agent langchain1.0 推荐两种方式
## 1. supervisor agent  集中式
#     user => supervisor agent => worker agents
## 2. handoff agent  轮换式
#。   user => agent1 => user => agent2 => user => agent3

### 这个例子关于supervisor agent
### 步骤：
# 1.创建2个worker agent，有各自的tools
# 2.把这两个agent 封装成2个新的tools
# 3.创建 supervisor agent， 配置tools 为上面封装的2个agent工具

### 内容：
# 1. supervisor agent：个人助理
# 2. worker agent：calendar agent， email agent

from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langchain.tools import tool
from langchain.agents import create_agent
from langgraph.types import Command

from calendar_agent import calendar_agent
from email_agent import email_agent

load_dotenv()

model = init_chat_model(
    model="deepseek:deepseek-chat",
    temperature=0.5,
    timeout=10,
    max_tokens=1000
)

@tool
def schedule_event(request: str) -> str:
    """Schedule calendar events using natural language.

    Use this when the user wants to create, modify, or check calendar appointments.
    Handles date/time parsing, availability checking, and event creation.

    Input: Natural language scheduling request (e.g., 'meeting with design team
    next Tuesday at 2pm')
    """
    result = calendar_agent.invoke({
        "messages": [{"role": "user", "content": request}]
    })
    return result["messages"][-1].text


@tool
def manage_email(request: str) -> str:
    """Send emails using natural language.

    Use this when the user wants to send notifications, reminders, or any email
    communication. Handles recipient extraction, subject generation, and email
    composition.

    Input: Natural language email request (e.g., 'send them a reminder about
    the meeting')
    """
    result = email_agent.invoke({
        "messages": [{"role": "user", "content": request}]
    })
    return result["messages"][-1].text

SUPERVISOR_PROMPT = (
    "You are a helpful personal assistant. "
    "You can schedule calendar events and send emails. "
    "Break down user requests into appropriate tool calls and coordinate the results. "
    "When a request involves multiple actions, use multiple tools in sequence."
)

supervisor_agent = create_agent(
    model=model,
    tools=[schedule_event, manage_email],
    system_prompt=SUPERVISOR_PROMPT,
)

config = {"configurable": {"thread_id": "1"}}

# example usage
def test_supervisor_agent():
    query = "hello"
    for event in supervisor_agent.stream(
        {"messages": [{"role": "user", "content": query}]},
        config=config,
        stream_mode="values"
    ):
        event["messages"][-1].pretty_print()
    
    query = ("Schedule a team meeting ['design-team@example.com'] on 2026-06-10 at 14:00 for 1 hour,"
             "then send a email to Alice[alice@example.com] and cc Charlie[charlie@example.com] about the design document meeting details")
    for step in supervisor_agent.stream(
        {"messages": [{"role": "user", "content": query}]},
        config=config,
        stream_mode="values"
    ):
        step["messages"][-1].pretty_print()

    # for step in supervisor_agent.stream(
    #     {"messages": [{"role": "user", "content": query}]},
    #     config=config,
    #     stream_mode="values",
    # ):
    #     if "__interrupt__" in step:
    #         print("INTERRUPTED:")
    #         interrupt = step["__interrupt__"][0]
    #         for request in interrupt.value["action_requests"]:
    #             print(f"description:{request['description']}")
    #         user_point = input("\n请输入您的决定（approve/reject/edit）: ").strip().lower()
    #         if user_point == "approve":
    #             decisions = [{"type": "approve"}]
    #         elif user_point == "reject":
    #             decisions = [{"type": "reject"}]
    #         elif user_point == "edit":
    #             decisions = [{"type": "edit", "edited_action": {"name": "new_tool_name", "args": {"arg1": "value1"}}}]
    #         else:
    #             print("无效输入，默认选择 approve")
    #             decisions = [{"type": "approve"}]
    #     elif "messages" in step:
    #         step["messages"][-1].pretty_print()
    #     else:
    #         pass

    # for step in supervisor_agent.stream(
    #     Command(resume={"decisions": decisions}),
    #     config=config,
    #     stream_mode="values",
    # ):
    #     if "messages" in step:
    #         step["messages"][-1].pretty_print()
    #     elif "__interrupt__" in step:
    #         print("INTERRUPTED:")
    #         interrupt = step["__interrupt__"][0]
    #         for request in interrupt.value["action_requests"]:
    #             print(f"description:{request['description']}")
    #     else:
    #         pass
    

# test_supervisor_agent()
