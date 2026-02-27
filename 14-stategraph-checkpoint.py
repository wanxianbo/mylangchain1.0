## stategraph 状态图
## checkpointer: 检查点管理器
## checkpoint: 检查点
## thread_id 管理
## 作用：记忆管理、时间旅行（time travel）

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver

from langchain_core.runnables import RunnableConfig

from typing import Annotated
from typing_extensions import TypedDict
from operator import add

# 表达状态:是整个状态图的状态
class State(TypedDict):
    foo: str
    bar: Annotated[list[str], add]

def node_a(state: State):
    return {"foo": "a", "bar": ["a"]}

def node_b(state: State):
    return {"foo": "b", "bar": ["b"]}

# 构建状态图
workflow = StateGraph(State)
workflow.add_node(node_a)
workflow.add_node(node_b)
workflow.add_edge(START, "node_a")
workflow.add_edge("node_a", "node_b")
workflow.add_edge("node_b", END)

# 检查点管理器
checkpointer = InMemorySaver()

# 编译
graph = workflow.compile(checkpointer=checkpointer)

# 配置
config: RunnableConfig = {
    "configurable": {"thread_id": "1"}
}

# 调用
results = graph.invoke({"foo":""}, config)
print(results)
# {'foo': 'b', 'bar': ['a', 'b']}
# for event in graph.stream({"foo":""}, config, stream_mode="values"):
#     print(event)
# {'foo': '', 'bar': []}
# {'foo': 'a', 'bar': ['a']}
# {'foo': 'b', 'bar': ['a', 'b']}

# 查询
print(graph.get_state(config=config))
# StateSnapshot(
# values={'foo': 'b', 'bar': ['a', 'b']}, 
# next=(), 
# config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1f1131bd-f99a-6808-8002-400967259362'}}, 
# metadata={'source': 'loop', 'step': 2, 'parents': {}}, 
# created_at='2026-02-26T14:03:06.162988+00:00', 
# parent_config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1f1131bd-f999-6818-8001-8f940187875c'}}, 
# tasks=(), 
# interrupts=())

for checkpoint_tuple in checkpointer.list(config=config):
    # print(checkpoint_tuple)
    print()
    print(checkpoint_tuple[2]["step"])
    print(checkpoint_tuple[2]["source"])
    print(checkpoint_tuple[1]["channel_values"])
    # CheckpointTuple(
    # config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1f1131c4-2b83-6a26-8002-96b035a7cf64'}}, 
    # checkpoint=
    #       {'v': 4, 
    #        'ts': '2026-02-26T14:05:52.457779+00:00', 'id': '1f1131c4-2b83-6a26-8002-96b035a7cf64', 
    #        'channel_versions': {'__start__': '00000000000000000000000000000002.0.8616213591625447', 
    #               'foo': '00000000000000000000000000000004.0.4084132219230472', 
    #               'branch:to:node_a': '00000000000000000000000000000003.0.20672882772176537', 
    #               'bar': '00000000000000000000000000000004.0.4084132219230472', 
    #               'branch:to:node_b': '00000000000000000000000000000004.0.4084132219230472'}, 
    #         'versions_seen': {'__input__': {}, '__start__': {'__start__': '00000000000000000000000000000001.0.6799473240282329'}, 
    #                'node_a': {'branch:to:node_a': '00000000000000000000000000000002.0.8616213591625447'}, 
    #                'node_b': {'branch:to:node_b': '00000000000000000000000000000003.0.20672882772176537'}}, 
    #                'updated_channels': ['bar', 'foo'], 
    #                'channel_values': {'foo': 'b', 'bar': ['a', 'b']}}, 
    # metadata={'source': 'loop', 'step': 2, 'parents': {}}, 
    # parent_config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1f1131c4-2b82-6e78-8001-921da38c5a80'}}, 
    # pending_writes=[])