from langgraph.checkpoint.postgres import PostgresSaver

DB_URL = "postgresql://postgres:postgres@192.168.10.5:5432/langchain?sslmode=disable"
with PostgresSaver.from_conn_string(DB_URL) as checkpointer:
    # 获取所有的checkpoint 检查点
    checkpoints = checkpointer.list(
        {"configurable": {"thread_id": "1"}}
    )

    for checkpoint in checkpoints:
        messages = checkpoint[1]["channel_values"]["messages"]
        for message in messages:
            message.pretty_print()
        break
        # print(checkpoint)
        # CheckpointTuple(config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1f11198d-9951-6642-8004-ed7ba820b30c'}}, 
        # checkpoint={'v': 4, 'id': '1f11198d-9951-6642-8004-ed7ba820b30c', 'ts': '2026-02-24T15:52:40.832323+00:00', 
        # 'versions_seen': {'model': {'branch:to:model': '00000000000000000000000000000005.0.7336686412014856'}, 
        # '__input__': {}, '__start__': {'__start__': '00000000000000000000000000000004.0.3901420461998588'}}, 
        # 'channel_values': {'messages': [HumanMessage(content='来段宋词', additional_kwargs={}, response_metadata={}, id='c1aac464-00e4-407a-9375-a58e08adb39f'), AIMessage(content='《行香子·山居》\n野径苔深，竹牖云亲。\n偶扶筇、半是闲人。\n溪声漱玉，林影筛金。\n对一瓯春，一帘雨，一床琴。\n\n浮名何用，蜗角纷纭。\n算不如、鸥鹭为邻。\n石枰棋老，松火茶新。\n任风敲梦，灯温字，月披襟。\n\n注：此词以山居生活为背景，通过“苔深”“云亲”“漱玉”“筛金”等意象勾勒出幽静自然的意境。下阕以“鸥鹭为邻”表达脱俗之志，结句“风敲梦，灯温字，月披襟”三层递进，将隐逸之趣凝练于日常细节，暗含对红尘名利的疏离，对精神自由的追寻。', 
        # additional_kwargs={'refusal': None}, 
        # response_metadata={'token_usage': {'completion_tokens': 190, 'prompt_tokens': 8, 'total_tokens': 198, 'completion_tokens_details': None, 'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': 0}, 'prompt_cache_hit_tokens': 0, 'prompt_cache_miss_tokens': 8}, 'model_provider': 'deepseek', 'model_name': 'deepseek-chat', 'system_fingerprint': 'fp_eaab8d114b_prod0820_fp8_kvcache', 'id': 'fc4ec34d-28c6-4c45-9564-6b7dacfc243c', 'finish_reason': 'stop', 'logprobs': None}, id='lc_run--019c905a-1555-7582-aad2-dd44bf0a0601-0', tool_calls=[], invalid_tool_calls=[], usage_metadata={'input_tokens': 8, 'output_tokens': 190, 'total_tokens': 198, 'input_token_details': {'cache_read': 0}, 'output_token_details': {}}), HumanMessage(content='再来', additional_kwargs={}, response_metadata={}, id='07578d72-5c28-483e-9fe4-b8c0f18685a8'), AIMessage(content='《鹧鸪天·夜泊枫桥》\n苇絮沾衣过晚钟，孤篷斜系酒旗风。\n一星渔火沉寒水，半榻诗愁叠旧篷。\n灯影碎，橹声空。十年心事转朦胧。\n何人立尽霜桥月，拾得秋声在梦中。\n\n注：此词化用唐人张继《枫桥夜泊》意境而另辟蹊径。以“沉寒水”“叠旧篷”暗喻心事沉积，“灯影碎”三句将时空感揉碎重组。结句“拾得秋声在梦中”以虚写实，将羁旅愁思升华为对永恒秋意的审美捕捉，在古典意象中注入现代时空观。', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 160, 'prompt_tokens': 203, 'total_tokens': 363, 'completion_tokens_details': None, 'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': 192}, 'prompt_cache_hit_tokens': 192, 'prompt_cache_miss_tokens': 11}, 'model_provider': 'deepseek', 'model_name': 'deepseek-chat', 'system_fingerprint': 'fp_eaab8d114b_prod0820_fp8_kvcache', 'id': '953aef66-e83f-4e5d-a6f6-3fc38efe2e3e', 'finish_reason': 'stop', 'logprobs': None}, id='lc_run--019c905a-2dd5-7af3-af82-f1bd414cdff2-0', tool_calls=[], invalid_tool_calls=[], usage_metadata={'input_tokens': 203, 'output_tokens': 160, 'total_tokens': 363, 'input_token_details': {'cache_read': 192}, 'output_token_details': {}})]}, 'channel_versions': {'messages': '00000000000000000000000000000006.0.2831496918780534', '__start__': '00000000000000000000000000000005.0.7336686412014856', 'branch:to:model': '00000000000000000000000000000006.0.2831496918780534'}, 'updated_channels': ['messages']}
