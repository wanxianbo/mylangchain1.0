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

EMAIL_AGENT_PROMPT = (
    "You are an email assistant. "
    "Compose professional emails based on natural language requests. "
    "Extract recipient information and craft appropriate subject lines and body text. "
    "Use send_email to send the message. "
    "Always confirm what was sent in your final response."
)

@tool
def send_email(
    to: list[str],  # email addresses
    subject: str,
    body: str,
    cc: list[str] = []
) -> str:
    """Send an email via email API. Requires properly formatted addresses."""
    # Stub: In practice, this would call SendGrid, Gmail API, etc.
    print("email_agent tool : called send_email")
    return f"Email sent to {', '.join(to)} - Subject: {subject}"


email_agent = create_agent(
    model=model,
    tools=[send_email],
    system_prompt=EMAIL_AGENT_PROMPT,
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={"send_email": True},
            description_prefix="Outbound email pending approval",
        ),
    ],
)

def test_email_agent():
    query = "hello"
    for event in email_agent.stream(
        {"messages": [{"role": "user", "content": query}]},
        stream_mode="values"
    ):
        event["messages"][-1].pretty_print()
    
    query = "Send a email to Alice[alice@example.com] about the meeting tomorrow at 3pm, and cc Charlie[charlie@example.com]"
    for event in email_agent.stream(
        {"messages": [{"role": "user", "content": query}]},
        stream_mode="values"
    ):
        event["messages"][-1].pretty_print()

# if __name__ == "__main__":
    # test_email_agent()