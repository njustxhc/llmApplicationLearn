"""
多 MCP Server 模拟：注册多个「服务」，统一列出工具、按「服务名.工具名」调度执行。
"""
from __future__ import annotations
import re
from typing import Callable

_servers: dict[str, dict[str, tuple[str, Callable[..., str]]]] = {}

def register_server(server_name: str, tools: dict[str, tuple[str, Callable[..., str]]]) -> None:
    _servers[server_name] = dict(tools)

def list_all_tools() -> list[tuple[str, str]]:
    out = []
    for sname, tdict in _servers.items():
        for tname, (desc, _) in tdict.items():
            out.append((f"{sname}.{tname}", desc))
    return out

def format_tools_for_prompt() -> str:
    lines = [f"- {qname}：{desc}" for qname, desc in list_all_tools()]
    return "\n".join(lines) if lines else "（无可用工具）"

def call_tool(qualified_name: str, *args: str) -> str:
    if "." not in qualified_name:
        return "错误：请使用 服务名.工具名 格式"
    sname, tname = qualified_name.split(".", 1)
    sname, tname = sname.strip(), tname.strip()
    if sname not in _servers:
        return f"错误：未知服务 {sname}"
    tdict = _servers[sname]
    if tname not in tdict:
        return f"错误：服务 {sname} 下未知工具 {tname}"
    _, fn = tdict[tname]
    try:
        return fn(*args)
    except Exception as e:
        return f"执行失败: {e}"

def parse_tool_calls(reply: str) -> list[tuple[str, list[str]]]:
    out: list[tuple[str, list[str]]] = []
    for m in re.finditer(r"TOOL:\s*([\w.]+)\s*([^\n]*)", reply.strip()):
        qname, rest = m.group(1).strip(), m.group(2).strip().split()
        if qname:
            out.append((qname, rest))
    return out

def parse_tool_call(reply: str) -> tuple[str | None, list[str]]:
    calls = parse_tool_calls(reply)
    if not calls:
        return None, []
    qname, args = calls[0]
    return qname, args

def _weather_get(city: str) -> str:
    return f"{city or '未知'}：晴，15°C。（模拟）"
def _calc_add(a: str, b: str) -> str:
    try:
        return str(float(a) + float(b))
    except ValueError:
        return "参数须为数字"
def _calc_multiply(a: str, b: str) -> str:
    try:
        return str(float(a) * float(b))
    except ValueError:
        return "参数须为数字"
def _search_query(q: str) -> str:
    return f"【搜索模拟】关键词「{q}」的检索结果：示例文档1、示例文档2。"

def register_demo_servers() -> None:
    register_server("weather", {"get_weather": ("获取指定城市天气（模拟）", lambda *a: _weather_get(" ".join(a) if a else "未知"))})
    register_server("calc", {
        "add": ("两数相加", lambda *a: _calc_add(a[0], a[1]) if len(a) >= 2 else "需要2个参数"),
        "multiply": ("两数相乘", lambda *a: _calc_multiply(a[0], a[1]) if len(a) >= 2 else "需要2个参数"),
    })
    register_server("search", {"query": ("根据关键词检索（模拟）", lambda *a: _search_query(" ".join(a) if a else ""))})
