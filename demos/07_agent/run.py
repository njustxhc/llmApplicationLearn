"""
Demo 07：Agent 基础循环。模型决定是否调用工具，执行后结果塞回，直到最终答案。使用 core.llm。
"""
import logging
import os
import re
import sys

_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _root not in sys.path:
    sys.path.insert(0, _root)

from core.demo_log import setup_demo_logging
from core.llm import chat

setup_demo_logging()
log = logging.getLogger(__name__)

TOOLS_DESC = """
你可以使用以下工具（格式：TOOL: 函数名 参数）。
- get_current_weather(city)：返回某城市的天气描述（模拟）。
- add(a, b)：两数相加。
若不需要再调用工具，请直接给出最终答案，不要写 TOOL:。
"""

def run_tool(name: str, *args) -> str:
    if name == "get_current_weather":
        return f"{args[0] if args else '未知'}：晴，15°C。"
    if name == "add" and len(args) >= 2:
        try:
            return str(float(args[0]) + float(args[1]))
        except ValueError:
            return "参数须为数字"
    return f"未知工具: {name}"

def main():
    user_query = "北京和上海今天天气分别怎样？先查天气，再总结一下。"
    log.info("构造初始 messages（system=工具说明 + user=%s）", user_query[:30] + "…")
    messages = [
        {"role": "system", "content": TOOLS_DESC.strip()},
        {"role": "user", "content": user_query},
    ]
    for step in range(5):
        log.info("Agent 步骤 %d：调用 LLM…", step + 1)
        reply = chat(messages)
        if not reply:
            log.warning("步骤 %d 无回复，结束", step + 1)
            break
        log.info("步骤 %d 回复长度=%d，解析是否含 TOOL 调用", step + 1, len(reply))
        print(f"[步骤 {step + 1}] {reply[:200]}{'...' if len(reply) > 200 else ''}\n")
        m = re.match(r"TOOL:\s*(\w+)\s*(.*)", reply.strip())
        if not m:
            log.info("未解析到 TOOL，视为最终答案")
            print("最终答案:", reply)
            break
        tool_name, rest = m.group(1), m.group(2).strip().split()
        log.info("执行工具: %s, 参数=%s", tool_name, rest)
        result = run_tool(tool_name, *rest)
        messages.append({"role": "assistant", "content": reply})
        messages.append({"role": "user", "content": f"工具返回: {result}。请继续，若已足够则直接给出最终总结。"})
    else:
        log.info("达到最大步数 5")
        print("达到最大步数。")

if __name__ == "__main__":
    main()
