# 统一 LLM 调用模块（core.llm）

封装火山方舟（Ark）API，供 demos 与 learn_web 复用。

**配置**：在项目根目录使用 `.env`（复制 `.env.example` 为 `.env` 并填写）或系统环境变量：`ARK_API_KEY`（必填）、`ARK_MODEL_ID`、`ARK_TIMEOUT`。加载顺序：.env → 环境变量 → 默认值。详见项目根 README「环境配置」。

## 用法

```python
from core.llm import get_client, chat, chat_stream
reply = chat([{"role": "user", "content": "你好"}])
```
