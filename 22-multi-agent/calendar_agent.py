from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

from langchain.tools import tool
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware

load_dotenv()

# 定义模型
model = init_chat_model(
    model="deepseek:deepseek-chat",
    temperature=0.5,
    timeout=10,
    max_tokens=1000
)

@tool
def create_calendar_event(
    title: str,
    start_time: str,       # ISO format: "2024-01-15T14:00:00"
    end_time: str,         # ISO format: "2024-01-15T15:00:00"
    attendees: list[str],  # email addresses
    location: str = ""
) -> str:
    """Create a calendar event. Requires exact ISO datetime format."""
    # Stub: In practice, this would call Google Calendar API, Outlook API, etc.
    print("calendar_agent tool : called create_calendar_event")
    return f"Event created: {title} from {start_time} to {end_time} with {len(attendees)} attendees"


@tool
def get_available_time_slots(
    attendees: list[str],
    date: str,  # ISO format: "2024-01-15"
    duration_minutes: int
) -> list[str]:
    """Check calendar availability for given attendees on a specific date."""
    # Stub: In practice, this would query calendar APIs
    print("calendar_agent tool : called get_available_time_slots")
    return ["09:00", "14:00", "16:00"]


CALENDAR_AGENT_SYSTEM_PROMPT = (
    "You are a calendar scheduling assistant. "
    "Parse natural language scheduling requests (e.g., 'next Tuesday at 2pm') "
    "into proper ISO datetime formats. "
    "Use get_available_time_slots to check availability when needed. "
    "Use create_calendar_event to schedule events. "
    "Always confirm what was scheduled in your final response."
)

calendar_agent = create_agent(
    model=model,
    tools=[create_calendar_event, get_available_time_slots],
    system_prompt=CALENDAR_AGENT_SYSTEM_PROMPT,
    # middleware=[
    #     HumanInTheLoopMiddleware(
    #         interrupt_on={"create_calendar_event": True},
    #         description_prefix="Calendar event pending approval",
    #     ),
    # ],
)

def test_calendar_agent():
    query = "hello"
    for event in calendar_agent.stream(
        {"messages": [{"role": "user", "content": query}]},
        stream_mode="values"
    ):
        event["messages"][-1].pretty_print()
    
    query = "Schedule a team meeting ['demo@qq.com'] on 2025-03-10 at 2pm for 1 hour"
    for step in calendar_agent.stream(
        {"messages": [{"role": "user", "content": query}]},
        stream_mode="values"
    ):
        step["messages"][-1].pretty_print()

# test_calendar_agent()
    