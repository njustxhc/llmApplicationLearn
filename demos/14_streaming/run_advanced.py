"""
Demo 14 进阶：SSE 流式接口 + 前端消费。规划见 docs/进阶Demo实现说明与计划.md。
当前演示：仅多次流式调用同一问题，将逐 chunk 拼接后打印（模拟前端拼接）。
"""
import os
import sys
_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _root not in sys.path:
    sys.path.insert(0, _root)
from core.llm import chat_stream

def main():
    q = "用两句话介绍 SSE。"
    print("【进阶】流式逐 chunk 拼接（模拟前端 EventSource 消费）\n")
    print("问题:", q)
    print("回复: ", end="", flush=True)
    full = []
    for c in chat_stream([{"role": "user", "content": q}]):
        full.append(c)
        print(c, end="", flush=True)
    print("\n\n共", len(full), "个 chunk")

if __name__ == "__main__":
    main()
