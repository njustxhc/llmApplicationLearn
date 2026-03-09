"""
Demo 07 进阶：超长摘要演示。构造一段模拟长对话，调用 maybe_summarize 做摘要压缩并展示前后 messages 长度。
"""
import os
import sys
_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _root not in sys.path:
    sys.path.insert(0, _root)
from core.demo_log import setup_demo_logging
from .summarize import maybe_summarize

setup_demo_logging()

def main():
    # 模拟超过阈值的对话（system + 多轮，rest 需 >10 条才会触发摘要）
    messages = [{"role": "system", "content": "你是助手。"}]
    for i in range(1, 8):
        messages.append({"role": "user", "content": f"第{i}个问题：介绍一下主题{i}。"})
        messages.append({"role": "assistant", "content": f"主题{i}的简短回答。"})
    messages.append({"role": "user", "content": "总结一下我们聊过的内容。"})
    print("【进阶】超长摘要：压缩旧消息为一条摘要\n")
    print("压缩前 messages 条数:", len(messages))
    out = maybe_summarize(messages)
    print("压缩后 messages 条数:", len(out))
    for i, m in enumerate(out):
        role = m.get("role", "")
        content = (m.get("content") or "")[:80]
        print(f"  [{role}] {content}...")

if __name__ == "__main__":
    main()
