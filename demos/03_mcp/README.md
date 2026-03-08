# 03 MCP 工具调用

MCP Server 暴露 get_weather 工具（wttr.in）；客户端通过 stdio 连接并 list_tools / call_tool。

## 运行

```bash
# 启动 Server（stdio，供 Cursor/Inspector 连接）
python -m demos.03_mcp.server

# 列出工具
python -m demos.03_mcp.list_tools_client
```

配置 Cursor：`.cursor/mcp.json` 中 `args`: `["-m", "demos.03_mcp.server"]`，cwd 为项目根。
