# 17 Token 与成本意识

用简单启发式估算「消息字符数 → 约 token 数」，建立上下文长度与调用成本的概念。实际生产应使用 tokenizer 或 API 返回的 usage。

## 运行

```bash
python -m demos.18_tokens.run
```

本 demo 不调用 LLM，仅做长度与 token 估算的演示。
