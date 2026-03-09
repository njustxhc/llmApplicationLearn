"""
MCP 客户端示例：stdio 连接 Server，发起 tools/list 并打印工具列表。
运行（项目根目录）：python -m demos.04_mcp.list_tools_client
"""
import asyncio
import json
import os
import sys

def _get_server_params() -> "tuple[str, list[str], str]":
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    command = os.environ.get("MCP_SERVER_COMMAND", "").strip() or sys.executable
    module = os.environ.get("MCP_SERVER_MODULE", "").strip() or "demos.04_mcp.server"
    cwd = os.environ.get("MCP_SERVER_CWD", "").strip() or project_root
    return command, ["-m", module], cwd

async def run() -> None:
    from mcp.client.session import ClientSession
    from mcp.client.stdio import StdioServerParameters, stdio_client
    command, args, cwd = _get_server_params()
    params = StdioServerParameters(command=command, args=args, cwd=cwd)
    print(f"[client] 连接 MCP Server: cwd={cwd}", file=sys.stderr)
    async with stdio_client(params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            result = await session.list_tools()
            for i, tool in enumerate(result.tools, 1):
                print(f"--- 工具 {i}: {tool.name} ---")
                print(f"  描述: {tool.description}")
                print(f"  参数: {json.dumps(tool.inputSchema, ensure_ascii=False, indent=4)}")

def main() -> None:
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
