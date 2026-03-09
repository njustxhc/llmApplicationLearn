# 大模型应用学习 Demo 列表

在项目根目录下运行，例如：`python -m demos.01_api_chat.run`。

| 目录 | 主题 |
|------|------|
| 01_api_chat | 基础 API 与对话 |
| 02_langchain | LangChain 入门（LCEL 链式调用） |
| 03_rag | 检索增强（RAG） |
| 04_mcp | MCP 工具调用 |
| 05_function_calling | Function Calling |
| 06_prompt | Prompt 工程 |
| 07_memory | 多轮对话与记忆 |
| 08_agent | Agent（基础 / 多 MCP / ReAct / 规划） |
| 09_embedding_rag | Embedding 与向量检索 |
| 10_eval | 评估与评测 |
| 11_multimodal | 多模态 |
| 12_skill | Skill 学习与示例（SKILL.md / demo-skill） |
| 13_chat_app | 综合对话应用（Web，集成 RAG / MCP / 联网搜索） |
| 14_streaming | 流式输出（流式 vs 非流式对比） |
| 15_structured_output | 结构化输出（JSON 约束与解析） |
| 16_temperature | Temperature 与采样参数 |
| 17_error_retry | 错误处理与重试（指数退避） |
| 18_tokens | Token 与成本意识（长度估算） |
| 19_context_truncate | 上下文截断（保留最近 N 条） |

依赖：`core.llm`、`core.rag_doc`（见项目根 requirements.txt）。**13_chat_app** 为独立 Web 应用，运行 `python -m demos.13_chat_app.app` 后访问 http://127.0.0.1:5000。
