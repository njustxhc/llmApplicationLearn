"""
MCP Server：提供「获取天气」工具。使用 wttr.in，无需 API Key。
运行：python -m demos.04_mcp.server（项目根目录）
"""

import asyncio
import logging
import sys
import urllib.parse

import httpx
import mcp.types as types
from mcp.server import Server
from mcp.server.stdio import stdio_server

logger = logging.getLogger("mcp_demo.weather")
logger.setLevel(logging.INFO)
if not logger.handlers:
    h = logging.StreamHandler(sys.stderr)
    h.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s", datefmt="%H:%M:%S"))
    logger.addHandler(h)
logger.propagate = False

WTTRI_TIMEOUT = 30.0

async def fetch_weather(city: str) -> str:
    url = "https://wttr.in/" + urllib.parse.quote(city) + "?format=3"
    logger.info("fetch_weather: city=%s, url=%s", city, url)
    try:
        async with httpx.AsyncClient(timeout=WTTRI_TIMEOUT, trust_env=False) as client:
            r = await client.get(url, headers={"User-Agent": "MCP-Weather-Demo (Python)"})
            logger.info("wttr.in: status=%s", r.status_code)
            r.raise_for_status()
            text = (r.text or "").strip() or f"{city}: 暂无数据"
            return text
    except httpx.HTTPStatusError as e:
        return f"{city}: 查询失败 (HTTP {e.response.status_code})"
    except Exception as e:
        logger.exception("fetch_weather: 异常")
        return f"{city}: 查询失败 ({e})"

def main() -> None:
    server = Server("weather")

    @server.list_tools()
    async def handle_list_tools(_request: types.ListToolsRequest) -> types.ListToolsResult:
        return types.ListToolsResult(
            tools=[
                types.Tool(
                    name="get_weather",
                    description="获取指定城市当前天气（基于 wttr.in，支持中文城市名）",
                    inputSchema={
                        "type": "object",
                        "required": ["city"],
                        "properties": {"city": {"type": "string", "description": "城市名称"}},
                    },
                )
            ]
        )

    @server.call_tool()
    async def handle_call_tool(name: str, arguments: dict) -> list[types.TextContent]:
        if name != "get_weather":
            return [types.TextContent(type="text", text=f"未知工具: {name}")]
        city = (arguments.get("city") or "").strip() or "北京"
        text = await fetch_weather(city)
        return [types.TextContent(type="text", text=text)]

    async def run() -> None:
        async with stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream, server.create_initialization_options())

    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
