import requests, pathlib

url = "https://storage.googleapis.com/benchmarks-artifacts/chinook/Chinook.db"
local_path = pathlib.Path("Chinook.db")


if local_path.exists():
    print(f"{local_path} already exists, skipping download.")
else:
    response = requests.get(url)
    if response.status_code == 200:
        local_path.write_bytes(response.content)
        print(f"File downloaded and saved as {local_path}")
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")

from langchain_community.utilities import SQLDatabase

db = SQLDatabase.from_uri("sqlite:///Chinook.db")

print(f"数据库方言: {db.dialect}")
print(f"数据库可用表: {db.get_usable_table_names()}")
print(f'艺术家（Artist）事例: {db.run("SELECT * FROM Artist LIMIT 5;")}')


from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

load_dotenv()

# 定义模型
model = init_chat_model(
    model="deepseek:deepseek-chat",
    temperature=0.5,
    timeout=10,
    max_tokens=1000
)

toolkit = SQLDatabaseToolkit(db=db, llm=model)

tools = toolkit.get_tools()

for tool in tools:
    print(f"可用工具：{tool.name}: {tool.description}\n")

system_prompt = """
You are an agent designed to interact with a SQL database.
Given an input question, create a syntactically correct {dialect} query to run,
then look at the results of the query and return the answer. Unless the user
specifies a specific number of examples they wish to obtain, always limit your
query to at most {top_k} results.

You can order the results by a relevant column to return the most interesting
examples in the database. Never query for all the columns from a specific table,
only ask for the relevant columns given the question.

You MUST double check your query before executing it. If you get an error while
executing a query, rewrite the query and try again.

DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the
database.

To start you should ALWAYS look at the tables in the database to see what you
can query. Do NOT skip this step.

Then you should query the schema of the most relevant tables.
使用中文
""".format(
    dialect=db.dialect,
    top_k=5,
)

from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents.middleware import HumanInTheLoopMiddleware

# 创建智能体
agent = create_agent(
    model=model,
    tools=tools,
    checkpointer=InMemorySaver(),
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={"sql_db_query": True},
            description_prefix="Tool execution pending approval"
        )
    ]
)

question = "哪种音乐类型的歌曲平均时长最长？"
config = {"configurable": {"thread_id": "1"}}

decisions = []

for step in agent.stream(
    {"messages": [{"role": "user", "content": question}]},
    config=config,
    stream_mode="values",
):
    if "__interrupt__" in step:
        print("INTERRUPTED:")
        interrupt = step["__interrupt__"][0]
        for request in interrupt.value["action_requests"]:
            print(f"description:{request['description']}")
        user_point = input("\n请输入您的决定（approve/reject/edit）: ").strip().lower()
        if user_point == "approve":
            decisions = [{"type": "approve"}]
        elif user_point == "reject":
            decisions = [{"type": "reject"}]
        elif user_point == "edit":
            decisions = [{"type": "edit", "edited_action": {"name": "new_tool_name", "args": {"arg1": "value1"}}}]
        else:
            print("无效输入，默认选择 approve")
            decisions = [{"type": "approve"}]
    elif "messages" in step:
        step["messages"][-1].pretty_print()
    else:
        pass

from langgraph.types import Command
for step in agent.stream(
    Command(resume={"decisions": decisions}),
    config=config,
    stream_mode="values",
):
    if "messages" in step:
        step["messages"][-1].pretty_print()
    elif "__interrupt__" in step:
        print("INTERRUPTED:")
        interrupt = step["__interrupt__"][0]
        for request in interrupt.value["action_requests"]:
            print(f"description:{request['description']}")
    else:
        pass