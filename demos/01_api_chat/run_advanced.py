"""
Demo 01 进阶：多轮对话。维护 messages 历史，连续 3～5 轮「用户提问 → 模型回复」，
每轮将上一轮的 user 与 assistant 追加到 messages 再请求，演示多轮对话与上下文。
"""
import logging
import os
import sys

_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _root not in sys.path:
    sys.path.insert(0, _root)

from core.demo_log import setup_demo_logging
from core.llm import chat

setup_demo_logging()
log = logging.getLogger(__name__)

# 预设 3 轮问答，模拟多轮对话
ROUNDS = [
    "用一句话介绍你自己。",
    "你能做什么？",
    "谢谢，再见。",
]


def main():
    messages = []
    log.info("进阶：多轮对话，共 %d 轮", len(ROUNDS))
    for i, user_msg in enumerate(ROUNDS, 1):
        messages.append({"role": "user", "content": user_msg})
        log.info("第 %d 轮：请求 messages 长度=%d", i, len(messages))
        reply = chat(messages)
        reply = (reply or "").strip() or "(无回复)"
        messages.append({"role": "assistant", "content": reply})
        print(f"[第{i}轮] 用户: {user_msg}")
        print(f"[第{i}轮] 助手: {reply}")
        print()
    log.info("多轮对话结束，总 messages 条数=%d", len(messages))


if __name__ == "__main__":
    main()
