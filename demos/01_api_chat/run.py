"""
Demo 01：基础 API 与对话。使用 core.llm 调用火山方舟，完成一次简单问答。
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


def main():
    user_msg = "用一句话介绍你自己。"
    log.info("构造 messages（仅一条 user）")
    messages = [{"role": "user", "content": user_msg}]
    log.info("调用 core.llm.chat，请求 API…")
    reply = chat(messages)
    log.info("收到回复，长度=%d 字符", len(reply or ""))
    print("用户:", user_msg)
    print("助手:", reply or "(无回复)")

if __name__ == "__main__":
    main()
