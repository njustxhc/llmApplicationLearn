# 14 结构化输出（Structured Output）

通过 system prompt 约束模型只输出合法 JSON，再在代码中解析、校验，便于下游程序使用。

## 运行

```bash
python -m demos.15_structured_output.run
```

会请求模型按指定 JSON 格式回答，并演示从回复中提取 JSON、遍历字段的过程。
