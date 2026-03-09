"""
Demo 05 进阶：多轮多次 function call。同一对话中解析多轮 TOOL 调用并回填。
规划见 docs/进阶Demo实现说明与计划.md。此处演示两轮：先 add 再 greet，模型综合后回答。
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
TOOLS = "工具格式: TOOL: 函数名 参数。可用: add(a,b) 两数相加; greet(name) 打招呼。"
def run_tool(name, *args):
    if name == "add" and len(args) >= 2:
        try: return str(float(args[0]) + float(args[1]))
        except ValueError: return "参数须为数字"
    if name == "greet" and args: return f"你好，{args[0]}！"
    return f"未知: {name} {args}"

def main():
    messages = [{"role": "system", "content": TOOLS}, {"role": "user", "content": "请先用 add 算 1 和 2 的和，再用 greet 向“世界”打个招呼，最后用一句话总结。"}]
    reply = chat(messages)
    print("第1轮回复:", reply)
    if not reply: return
    m = re.match(r"TOOL:\s*(\w+)\s*(.*)", reply.strip())
    if m:
        name, rest = m.group(1), m.group(2).strip().split()
        result = run_tool(name, *rest)
        messages.append({"role": "assistant", "content": reply})
        messages.append({"role": "user", "content": f"工具返回: {result}。请继续（若还有工具要调用请用 TOOL: 格式）。"})
        reply2 = chat(messages)
        print("第2轮回复:", reply2)
        if reply2 and "TOOL:" in reply2:
            m2 = re.match(r"TOOL:\s*(\w+)\s*(.*)", reply2.strip())
            if m2:
                r2 = run_tool(m2.group(1), *m2.group(2).strip().split())
                messages.append({"role": "assistant", "content": reply2})
                messages.append({"role": "user", "content": f"工具返回: {r2}。请用一句话总结。"})
                print("最终:", chat(messages))

if __name__ == "__main__":
    main()
