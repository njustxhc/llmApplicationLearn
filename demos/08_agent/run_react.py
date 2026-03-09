"""Demo 07：ReAct 格式。Thought → Action → Observation 直至 Final Answer。使用 core.llm。"""
import logging
import os
import re
import sys

_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _root not in sys.path:
    sys.path.insert(0, _root)

from core.demo_log import setup_demo_logging
from core.llm import chat
from .multi_mcp import register_demo_servers, format_tools_for_prompt, call_tool, parse_tool_calls

setup_demo_logging()
log = logging.getLogger(__name__)

REACT_SYSTEM = """你按 ReAct 格式回复：Thought: （简短思考） Action: TOOL: 服务名.工具名 参数 或 Final Answer: （最终答案）
可用工具：{tools}
若不需要调用工具，必须用 Final Answer: 开头给出答案。"""

def extract_final_answer(reply: str) -> str | None:
    m = re.search(r"Final\s+Answer:\s*(.+)", reply.strip(), re.DOTALL | re.IGNORECASE)
    return m.group(1).strip() if m else None

def main():
    log.info("注册 demo 工具，构造 ReAct system prompt")
    register_demo_servers()
    tools_text = format_tools_for_prompt()
    messages = [
        {"role": "system", "content": REACT_SYSTEM.format(tools=tools_text)},
        {"role": "user", "content": "请先查北京天气，再用 calc 算 10 和 20 的和，最后用一句话总结。"},
    ]
    for step in range(8):
        log.info("ReAct 步骤 %d：调用 LLM", step + 1)
        reply = chat(messages)
        if not reply:
            break
        print(f"[Step {step + 1}]", reply[:400], "\n")
        if extract_final_answer(reply):
            print("--- Final Answer ---\n", extract_final_answer(reply))
            break
        calls = parse_tool_calls(reply)
        if not calls:
            break
        obs = "\n".join(f"{qname}: {call_tool(qname, *args)}" for qname, args in calls)
        print("Observation:", obs, "\n")
        messages.append({"role": "assistant", "content": reply})
        messages.append({"role": "user", "content": f"Observation:\n{obs}\n\n请继续；若任务已完成请用 Final Answer: 给出总结。"})
    else:
        print("达到最大步数。")

if __name__ == "__main__":
    main()
