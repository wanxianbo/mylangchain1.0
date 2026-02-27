from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

from dotenv import load_dotenv

load_dotenv()

model =init_chat_model(
    # model="ollama:deepseek-r1:8b",
    # model="ollama:gpt-oss:20b",
    base_url="http://192.168.10.93:11434"
)

agent = create_agent(
    # model="deepseek:deepseek-chat"
    model=model,
)

# print(agent)
# langgraph.graph.state.CompiledStateGraph
# Graph: nodes -> edges
# print(agent.nodes)
# {'__start__': <langgraph.pregel._read.PregelNode object at 0x1161c4a90>, 
# 'model': <langgraph.pregel._read.PregelNode object at 0x1161c4d10>}

# pregel: 

result = agent.invoke({"messages": [{"role": "user", "content": "what is the weather in beijing?"}]})
print(result)
# {'messages': [HumanMessage(content='what is the weather in beijing?', additional_kwargs={}, response_metadata={}, id='6bbe78ff-6c06-440c-9781-018e379b951e'), 
# AIMessage(content='I don\'t have real-time data access, so I can\'t provide the current weather in Beijing.\n\nTo get the most accurate and up-to-date weather information, you can:\n\n1.  **Check a weather website or app:** Reliable sources include:\n    *   [Weather.com](https://weather.com) (The Weather Channel)\n    *   [AccuWeather.com](https://www.accuweather.com/)\n    *   [BBC Weather](https://www.bbc.com/weather)\n    *   Your smartphone\'s built-in weather app.\n\n2.  **Search online:** Simply type "**weather Beijing**" into Google, Bing, or another search engine for an instant forecast.\n\n3.  **Ask a voice assistant:** You can ask Siri, Google Assistant, or Alexa on your devices.\n\n**General Climate of Beijing:**\nBeijing has a **humid continental climate** with four distinct seasons:\n*   **Spring (Mar-May):** Mild but can be windy and sandy.\n*   **Summer (Jun-Aug):** Hot and humid, with the majority of the year\'s rainfall.\n*   **Autumn (Sep-Nov):** Generally considered the best season—cool, dry, and sunny.\n*   **Winter (Dec-Feb):** Cold and dry, with occasional snowfall and temperatures often below freezing.\n\nWould you like help finding a specific weather forecast website?', 
# additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 281, 'prompt_tokens': 12, 'total_tokens': 293, 'completion_tokens_details': None, 'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': 0}, 'prompt_cache_hit_tokens': 0, 'prompt_cache_miss_tokens': 12}, 'model_provider': 'deepseek', 'model_name': 'deepseek-chat', 'system_fingerprint': 'fp_eaab8d114b_prod0820_fp8_kvcache', 
# 'id': '806e27af-921d-4f05-bd56-70cf6538ec01', 'finish_reason': 'stop', 'logprobs': None}, id='lc_run--019c8faa-98a5-7dc1-95e0-f1ea8a922ed8-0', tool_calls=[], invalid_tool_calls=[], 
# usage_metadata={'input_tokens': 12, 'output_tokens': 281, 'total_tokens': 293, 'input_token_details': {'cache_read': 0}, 'output_token_details': {}})]}
print("=======================================")
messages = result["messages"]
print(f"历史消息：{len(messages)}条")
for message in messages:
    message.pretty_print()