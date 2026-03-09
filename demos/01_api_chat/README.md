# 01 基础 API 与对话

调用大模型 API、发消息、收回复。使用统一模块 `core.llm`。

## 基础用例

单轮一问一答：`run.py`。

```bash
python -m demos.01_api_chat.run
```

## 进阶用例

多轮对话（3 轮，维护 messages 历史）：`run_advanced.py`。

```bash
python -m demos.01_api_chat.run_advanced
```
