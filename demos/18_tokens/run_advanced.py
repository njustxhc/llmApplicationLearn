"""
Demo 18 进阶：按 token 预算截断或结合 usage。规划见 docs/进阶Demo实现说明与计划.md。
当前演示：用粗略 token 估算，给定预算只保留「不超预算」的最近消息。
"""
import os
import sys
_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _root not in sys.path:
    sys.path.insert(0, _root)

def rough_tokens(text):
    return max(1, len((text or "")) // 2)

def main():
    messages = [
        {"role": "user", "content": "第一轮问题"},
        {"role": "assistant", "content": "第一轮回答" * 10},
        {"role": "user", "content": "第二轮问题"},
        {"role": "assistant", "content": "第二轮回答" * 10},
        {"role": "user", "content": "第三轮：总结"},
    ]
    budget = 50  # 约 50 token 预算
    total = 0
    kept = []
    for m in reversed(messages):
        t = rough_tokens(m.get("content"))
        if total + t > budget:
            break
        kept.insert(0, m)
        total += t
    print("【进阶】按 token 预算截断（预算约 %d token）\n" % budget)
    print("保留消息数:", len(kept), "，约 token:", total)

if __name__ == "__main__":
    main()
