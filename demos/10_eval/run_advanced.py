"""
Demo 10 进阶：LLM-as-judge 或批量测试集。规划见 docs/进阶Demo实现说明与计划.md。
当前演示：对一道题让 LLM 作答后，再用另一轮 prompt 让模型自评「回答是否切题」。
"""
import os
import sys
_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _root not in sys.path:
    sys.path.insert(0, _root)
from core.llm import chat

def main():
    q = "用一句话说明什么是 RAG。"
    reply = chat([{"role": "user", "content": q}]) or ""
    judge_prompt = f"问题：{q}\n回答：{reply}\n请判断上述回答是否切题（是否在解释 RAG），只输出「是」或「否」。"
    judge = chat([{"role": "user", "content": judge_prompt}]) or ""
    print("【进阶】LLM-as-judge\n")
    print("问题:", q)
    print("回答:", reply[:200] + "..." if len(reply) > 200 else reply)
    print("判题（是否切题）:", judge.strip())

if __name__ == "__main__":
    main()
