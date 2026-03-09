"""
Demo 06 进阶：Few-shot / CoT 提示对比。同一问题用「无 CoT」「有 CoT」两种 system 调用并对比。
"""
import os
import sys
_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _root not in sys.path:
    sys.path.insert(0, _root)
from core.llm import chat

def main():
    q = "小明有 3 个苹果，吃了 1 个，又买了 2 个。他一共有几个苹果？请直接给数字答案。"
    no_cot = [{"role": "system", "content": "你是一个数学助手。直接给出最终数字答案。"}, {"role": "user", "content": q}]
    with_cot = [{"role": "system", "content": "你是一个数学助手。请先一步步推理（写出步骤），再在最后一行给出最终数字答案。"}, {"role": "user", "content": q}]
    print("【进阶】CoT 对比\n")
    print("问题:", q, "\n")
    print("--- 无 CoT（直接答）---")
    print(chat(no_cot) or "")
    print("\n--- 有 CoT（先推理再答）---")
    print(chat(with_cot) or "")

if __name__ == "__main__":
    main()
