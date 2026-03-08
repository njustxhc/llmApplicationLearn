# 18 上下文截断（Context Truncation）

当对话历史超过模型上下文长度限制时，需要截断。本 demo 演示「只保留最近 N 条消息」的策略：构造一段模拟历史，截断后再追加当前问题发给模型。

## 运行

```bash
python -m demos.18_context_truncate.run
```

更完整的方案还可结合「摘要压缩」（见 06_memory）或按 token 数截断。
