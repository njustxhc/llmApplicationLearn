"""
Demo 04：Function Calling。定义工具，模型输出 TOOL: 函数名 参数，执行后结果再交给模型。
使用 core.llm（火山方舟）。
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
你可以使用以下工具（用一行回复，格式严格为：TOOL: 函数名 参数1 参数2）：
- add(a, b)：两数相加，例如 TOOL: add 3 5
- greet(name)：打招呼，例如 TOOL: greet 小明
若不需要调用工具，直接回答即可。
"""

def run_tool(name: str, *args) -> str:
    if name == "add" and len(args) >= 2:
        try:
            return str(float(args[0]) + float(args[1]))
        except ValueError:
            return "参数须为数字"
    if name == "greet" and args:
        return f"你好，{args[0]}！"
    return f"未知工具或参数: {name} {args}"

def main():
    user_query = "请用 add 计算 10 和 20 的和，并告诉我结果。"
    log.info("构造 messages（system=工具说明 + user=%s）", user_query[:30] + "…")
    messages = [
        {"role": "system", "content": TOOLS_DESC.strip()},
        {"role": "user", "content": user_query},
    ]
    log.info("第一次调用 core.llm.chat…")
    reply = chat(messages)
    if not reply:
        log.warning("模型未返回内容")
        print("模型未返回内容")
        return
    log.info("模型回复长度=%d，解析是否包含 TOOL 调用", len(reply))
    print("模型回复:", reply)
    m = re.match(r"TOOL:\s*(\w+)\s*(.*)", reply.strip())
    if m:
        tool_name, rest = m.group(1), m.group(2).strip().split()
        log.info("解析到工具: %s, 参数=%s，执行…", tool_name, rest)
        result = run_tool(tool_name, *rest)
        log.info("工具返回: %s，追加到 messages 并第二次调用 LLM", result)
        messages.append({"role": "assistant", "content": reply})
        messages.append({"role": "user", "content": f"工具返回结果: {result}。请把最终答案用一句话告诉我。"})
        final = chat(messages)
        log.info("最终回复长度=%d", len(final or ""))
        print("最终答案:", final or "")
    else:
        log.info("未解析到 TOOL 调用，仅展示首轮回复")

if __name__ == "__main__":
    main()
