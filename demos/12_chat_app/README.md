# 12 综合对话应用（Chat App）

将「基础 API 与对话」「RAG」「MCP 工具」「联网搜索」整合在一个 Web 对话应用里，通过页面与大模型对话，并可勾选是否启用文档 RAG、MCP 天气、联网搜索。

## 功能

- **基础对话**：使用 **core.llm**（火山方舟）完成多轮对话与流式输出。
- **文档 RAG**：勾选「文档 RAG」后，每次发送前从 **core.rag_doc** 检索相关片段并注入上下文，回答基于本地文档。
- **MCP 工具**：勾选「使用 MCP 工具」后，若用户问天气，会连接 **demos.03_mcp.server** 调用 get_weather，将结果注入后再生成回复。
- **联网搜索**：勾选「联网搜索」后，用 DuckDuckGo（ddgs）检索用户问题，将结果注入上下文再回答。

## 运行

在**项目根目录**执行：

```bash
python -m demos.12_chat_app.app
```

然后打开浏览器访问 **http://127.0.0.1:5000**。

## 依赖

- **core.llm**、**core.rag_doc**（见项目根 requirements.txt）
- **mcp**：MCP 客户端，`pip install mcp`
- **ddgs**：联网搜索，`pip install ddgs`

## 配置

- API Key 等：与其它 demo 相同，使用 `.env` 或环境变量 `ARK_API_KEY`、`ARK_MODEL_ID`、`ARK_TIMEOUT`。
- MCP Server：默认连接 `demos.03_mcp.server`；可通过环境变量 `MCP_SERVER_MODULE`、`MCP_SERVER_CWD` 覆盖。

本 demo 为学习项目中的「综合应用」版本，使用 **core.llm**、**core.rag_doc** 和 **demos.03_mcp**。
