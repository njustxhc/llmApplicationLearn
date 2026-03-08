"""Demo 07：规划步骤拆解。先输出步骤规划，再按步执行（每步可调工具）。使用 core.llm。"""
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

PLAN_SYSTEM = "你是规划型助手。可用工具（TOOL: 服务名.工具名 参数）：\n{tools}"

def get_plan(question: str, tools_text: str) -> list[str]:
    log.info("阶段一：请求步骤规划…")
    messages = [
        {"role": "system", "content": PLAN_SYSTEM.format(tools=tools_text)},
        {"role": "user", "content": f"请仅输出解决以下问题的步骤规划，每步一行，格式「数字. 步骤描述」，不要执行、不要调用工具。\n\n问题：{question}"},
    ]
    reply = chat(messages)
    if not reply:
        return []
    steps = []
    for line in reply.strip().splitlines():
        m = re.match(r"^\d+[\.．]\s*(.+)", line.strip())
        if m:
            steps.append(m.group(1).strip())
    return steps

def execute_step(step_index: int, step_desc: str, tools_text: str, max_rounds: int = 3) -> str:
    messages = [
        {"role": "system", "content": PLAN_SYSTEM.format(tools=tools_text)},
        {"role": "user", "content": f"当前执行步骤 {step_index + 1}：{step_desc}\n若需调用工具请用 TOOL: 服务名.工具名 参数；否则直接给出本步结果。"},
    ]
    for _ in range(max_rounds):
        reply = chat(messages)
        if not reply:
            return "(本步无返回)"
        calls = parse_tool_calls(reply)
        if not calls:
            return reply.strip()
        obs = "\n".join(f"{qname}: {call_tool(qname, *args)}" for qname, args in calls)
        messages.append({"role": "assistant", "content": reply})
        messages.append({"role": "user", "content": f"工具返回:\n{obs}\n请继续；若本步已完成请直接给出本步结果。"})
    return "(本步超时)"

def main():
    log.info("注册工具，开始规划+执行 demo")
    register_demo_servers()
    tools_text = format_tools_for_prompt()
    question = "先查上海天气，再计算 3 和 7 的乘积，最后用一句话总结天气和计算结果。"
    print("问题:", question, "\n--- 阶段一：步骤规划 ---")
    steps = get_plan(question, tools_text) or [question]
    log.info("解析到 %d 个步骤", len(steps))
    for i, s in enumerate(steps):
        print(f"  {i + 1}. {s}")
    print("\n--- 阶段二：按步执行 ---")
    results = []
    for i, desc in enumerate(steps):
        print(f"\n[步骤 {i + 1}] {desc}")
        res = execute_step(i, desc, tools_text)
        results.append((desc, res))
        print("  结果:", res[:120] + ("..." if len(res) > 120 else ""))
    print("\n--- 阶段三：汇总 ---")
    summary_prompt = "根据以下各步执行结果，用一两句话给出最终总结。\n\n" + "\n".join(f"步骤{i+1}（{d}）：{r}" for i, (d, r) in enumerate(results))
    final = chat([{"role": "user", "content": summary_prompt}])
    print(final or "(无)")

if __name__ == "__main__":
    main()
