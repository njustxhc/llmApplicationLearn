"""
Demo 13：流式输出（Streaming）。对比非流式一次返回与流式逐 token 返回，理解 SSE 与体验差异。
"""
import logging
import os
import sys

_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _root not in sys.path:
    sys.path.insert(0, _root)

from core.demo_log import setup_demo_logging
from core.llm import chat, chat_stream

setup_demo_logging()
log = logging.getLogger(__name__)

USER_QUERY = "用三句话介绍流式输出的好处。"


def main():
    log.info("用户问题: %s", USER_QUERY)
    print("=== 1. 非流式：一次性拿到完整回复 ===\n")
    messages = [{"role": "user", "content": USER_QUERY}]
    log.info("调用 core.llm.chat（非流式）…")
    reply = chat(messages)
    log.info("非流式返回完成，长度=%d 字符", len(reply or ""))
    print("回复:", reply or "(无)")
    print()

    print("=== 2. 流式：逐 token 打印（模拟前端逐字展示）===\n")
    log.info("调用 core.llm.chat_stream（流式）…")
    print("回复: ", end="", flush=True)
    chunk_count = 0
    for chunk in chat_stream(messages):
        chunk_count += 1
        print(chunk, end="", flush=True)
    log.info("流式结束，共 %d 个 chunk", chunk_count)
    print("\n")


if __name__ == "__main__":
    main()
