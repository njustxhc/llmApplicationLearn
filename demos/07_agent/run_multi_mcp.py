"""Demo 07：多 MCP Server。多组工具以「服务名.工具名」列出与调度。使用 core.llm。"""
import logging
import os
import sys

_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _root not in sys.path:
    sys.path.insert(0, _root)

from core.demo_log import setup_demo_logging
from core.llm import chat
from .multi_mcp import register_demo_servers, format_tools_for_prompt, call_tool, parse_tool_calls

setup_demo_logging()
log = logging.getLogger(__name__)

SYSTEM = "你可以使用多个来源的工具，格式：TOOL: 服务名.工具名 参数1 参数2 ...\n若不需要调用工具，请直接给出最终答案。\n\n可用工具：\n{tools}"

def main():
    log.info("注册多 MCP 工具，构造 system prompt")
    register_demo_servers()
    tools_text = format_tools_for_prompt()
    messages = [
        {"role": "system", "content": SYSTEM.format(tools=tools_text)},
        {"role": "user", "content": "用 weather 查北京天气，用 calc 算 10*20（multiply），最后用 search 搜「北京 天气」，并一句话总结。"},
    ]
    for step in range(8):
        log.info("步骤 %d：调用 LLM", step + 1)
        reply = chat(messages)
        if not reply:
            break
        print(f"[步骤 {step + 1}] {reply[:250]}{'...' if len(reply) > 250 else ''}\n")
        calls = parse_tool_calls(reply)
        if not calls:
            print("最终答案:", reply)
            break
        results = [f"{qname}: {call_tool(qname, *args)}" for qname, args in calls]
        combined = "\n".join(results)
        print("工具返回:", combined, "\n")
        messages.append({"role": "assistant", "content": reply})
        messages.append({"role": "user", "content": f"工具返回:\n{combined}\n请继续，若已足够则直接给出最终总结。"})
    else:
        print("达到最大步数。")

if __name__ == "__main__":
    main()
