"""
综合对话 Web 应用 Demo：集成文档 RAG、MCP 天气工具、联网搜索，通过页面与大模型对话。

- 使用 core.llm（火山方舟）、core.rag_doc（文档检索）。
- MCP 默认连接 demos.04_mcp.server（天气）；可通过环境变量 MCP_SERVER_MODULE 等覆盖。
- 运行：在项目根目录执行 python -m demos.13_chat_app.app，然后打开 http://127.0.0.1:5000
"""

import asyncio
import json
import logging
import os
import re
import sys

_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _root not in sys.path:
    sys.path.insert(0, _root)

from flask import Flask, request, jsonify, Response, send_from_directory

from core.llm import get_client, chat as llm_chat, chat_stream
from core.llm.config import ARK_API_KEY, ARK_MODEL_ID

logger = logging.getLogger("chat_app")
logger.setLevel(logging.INFO)
if not logger.handlers:
    _handler = logging.StreamHandler(sys.stderr)
    _handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s", datefmt="%H:%M:%S"))
    logger.addHandler(_handler)
logger.propagate = False

# ---------- MCP（默认 demos.04_mcp.server） ----------
def _get_mcp_server_params() -> "tuple[str, list[str], str]":
    """返回 (command, args, cwd)。"""
    command = os.environ.get("MCP_SERVER_COMMAND", "").strip() or sys.executable
    module = os.environ.get("MCP_SERVER_MODULE", "").strip() or "demos.04_mcp.server"
    cwd = os.environ.get("MCP_SERVER_CWD", "").strip() or _root
    return command, ["-m", module], cwd


def _call_mcp_get_weather(city: str) -> str:
    """连接 MCP Server，list_tools 后调用 get_weather。"""
    logger.info("MCP: 开始连接 Server，city=%s", city)
    try:
        from mcp.client.session import ClientSession
        from mcp.client.stdio import StdioServerParameters, stdio_client
    except ImportError as e:
        logger.warning("MCP: 未安装 mcp 包, %s", e)
        return "[MCP 未安装: pip install mcp]"
    command, args, cwd = _get_mcp_server_params()
    params = StdioServerParameters(command=command, args=args, cwd=cwd)
    logger.info("MCP: 使用 Server command=%s args=%s cwd=%s", command, args, cwd)

    async def _run() -> str:
        async with stdio_client(params) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                list_result = await session.list_tools()
                tool_names = [t.name for t in list_result.tools]
                logger.info("MCP: tools/list 返回 %d 个工具: %s", len(tool_names), tool_names)
                if "get_weather" not in tool_names:
                    return "[MCP Server 未提供 get_weather 工具]"
                result = await session.call_tool("get_weather", {"city": city})
                if result.isError or not result.content:
                    return "[MCP 返回错误]"
                block = result.content[0]
                text = getattr(block, "text", str(block))
                return text

    try:
        return asyncio.run(_run())
    except Exception as e:
        logger.exception("MCP: 调用失败")
        return f"[MCP 调用失败: {e}]"


def _extract_city_for_weather(user_message: str) -> str | None:
    msg = (user_message or "").strip()
    if not re.search(r"天气|weather|气温|温度", msg, re.I):
        return None
    m = re.match(r"^(.+?)(?:的)?天气", msg)
    if m:
        return m.group(1).strip() or "北京"
    m = re.search(r"(\S+)\s*的?\s*天气", msg)
    if m:
        return m.group(1).strip()
    return "北京"


def _inject_mcp_context(messages: list) -> list:
    if not messages or messages[-1].get("role") != "user":
        return messages
    content = (messages[-1].get("content") or "").strip()
    city = _extract_city_for_weather(content)
    if not city:
        return messages
    weather_text = _call_mcp_get_weather(city)
    context = f"以下是通过 MCP 工具获取的实时天气，请结合回答用户：\n\n{weather_text}"
    return [{"role": "system", "content": context}] + messages


# ---------- 文档 RAG（core.rag_doc） ----------
def _inject_rag_doc_context(messages: list, query: str, top_k: int = 3) -> list:
    logger.info("文档 RAG: query=%s, top_k=%s", query[:60] + ("..." if len(query) > 60 else ""), top_k)
    try:
        from core.rag_doc import get_rag_context
        context = get_rag_context(query, top_k=top_k)
    except Exception as e:
        logger.warning("文档 RAG: 调用失败 %s", e)
        context = f"[文档 RAG 暂不可用: {e}]"
    if not context or (context.startswith("[") and "未找到文档" in context):
        return messages
    return [{"role": "system", "content": context}] + messages


# ---------- 联网搜索（ddgs） ----------
def _web_search(query: str, max_results: int = 5) -> list[dict]:
    logger.info("联网搜索: query=%s, max_results=%s", query[:80] + ("..." if len(query) > 80 else ""), max_results)
    try:
        from ddgs import DDGS
        ddgs = DDGS()
        results = list(ddgs.text(query, max_results=max_results))
        return [{"title": r.get("title", ""), "snippet": r.get("body", r.get("snippet", "")), "href": r.get("href", "")} for r in results]
    except Exception as e:
        logger.warning("联网搜索: 失败 %s", e)
        return [{"error": str(e)}]


def _inject_search_context(messages: list, search_query: str) -> list:
    results = _web_search(search_query, max_results=5)
    if not results or (len(results) == 1 and results[0].get("error")):
        err = results[0].get("error", "搜索无结果") if results else "搜索无结果"
        context = f"[联网搜索暂时不可用: {err}]"
    else:
        parts = []
        for i, r in enumerate(results, 1):
            title = r.get("title", "")
            snippet = r.get("snippet", "") or r.get("body", "")
            href = r.get("href", "")
            parts.append(f"{i}. {title}\n   {snippet}\n   链接: {href}")
        context = "以下是最新联网搜索结果，请结合这些信息简要回答用户问题：\n\n" + "\n\n".join(parts)
    return [{"role": "system", "content": context}] + messages


# ---------- Flask ----------
_static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
app = Flask(__name__, static_folder=_static_dir, static_url_path="")


@app.route("/")
def index():
    return send_from_directory(_static_dir, "index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    logger.info("POST /api/chat 收到请求")
    if not ARK_API_KEY:
        return jsonify({"error": "未配置 ARK_API_KEY，请在环境变量或 .env 中设置"}), 500
    data = request.get_json() or {}
    messages = data.get("messages")
    if not messages or not isinstance(messages, list):
        return jsonify({"error": "请提供 messages 数组"}), 400
    stream = data.get("stream", False)
    use_search = data.get("use_search", False)
    use_mcp = data.get("use_mcp", False)
    use_rag_doc = data.get("use_rag_doc", False)
    search_query = (data.get("search_query") or "").strip()
    last_content = (messages[-1].get("content") or "").strip() if messages else ""

    if use_search and not search_query and messages and messages[-1].get("role") == "user":
        search_query = last_content
    if use_search and search_query:
        messages = _inject_search_context(messages, search_query)
    if use_mcp:
        messages = _inject_mcp_context(messages)
    if use_rag_doc and last_content:
        messages = _inject_rag_doc_context(messages, last_content, top_k=3)

    try:
        if stream:
            return _stream_response(messages)
        return _normal_response(messages)
    except Exception as e:
        logger.exception("请求处理异常")
        return jsonify({"error": str(e)}), 500


def _normal_response(messages: list) -> Response:
    content = llm_chat(messages)
    if content is None:
        return jsonify({"error": "模型未返回内容"}), 500
    return jsonify({"reply": content})


def _stream_response(messages: list) -> Response:
    def generate():
        for chunk in chat_stream(messages):
            yield f"data: {json.dumps({'content': chunk})}\n\n"
        yield "data: [DONE]\n\n"

    return Response(
        generate(),
        mimetype="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


if __name__ == "__main__":
    port = 5000
    logger.info("chat_app 启动: host=0.0.0.0, port=%s", port)
    if not ARK_API_KEY:
        logger.warning("未设置 ARK_API_KEY，请设置环境变量或 .env 后再使用 /api/chat")
    app.run(host="0.0.0.0", port=port, debug=True, use_reloader=False)
