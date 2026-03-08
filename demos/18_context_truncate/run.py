"""
Demo 18：上下文截断。构造较长对话历史，只保留「最近 N 条」再发给模型，演示超长时的截断策略。
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

# 模拟一段较长的历史（实际场景中来自真实多轮对话）
FAKE_HISTORY = [
    {"role": "user", "content": "第一轮：什么是 Python？"},
    {"role": "assistant", "content": "Python 是一种编程语言。"},
    {"role": "user", "content": "第二轮：它有什么特点？"},
    {"role": "assistant", "content": "易读、易学、生态丰富。"},
    {"role": "user", "content": "第三轮：适合做什么？"},
    {"role": "assistant", "content": "Web、数据分析、自动化、AI 等。"},
]

KEEP_LAST_N = 4  # 只保留最近 4 条（2 轮对话）


def truncate_messages(messages: list, keep_last_n: int) -> list:
    """只保留最后 keep_last_n 条消息（保证以 user 结尾时可用于当前请求）。"""
    if len(messages) <= keep_last_n:
        return messages
    return messages[-keep_last_n:]


def main():
    log.info("原始历史条数=%d，截断策略=保留最近 %d 条", len(FAKE_HISTORY), KEEP_LAST_N)
    print("原始历史条数:", len(FAKE_HISTORY))
    print("截断策略: 只保留最近 %d 条\n" % KEEP_LAST_N)

    truncated = truncate_messages(FAKE_HISTORY, KEEP_LAST_N)
    current = "第四轮：总结一下上面我们聊过的内容。"
    to_send = truncated + [{"role": "user", "content": current}]
    log.info("截断后消息条数=%d，追加当前问题后共 %d 条", len(truncated), len(to_send))

    print("发给模型的消息条数:", len(to_send))
    for i, m in enumerate(to_send):
        content_preview = (m.get("content") or "")[:40]
        print(f"  {i+1}. [{m.get('role')}] {content_preview}...")
    print()

    log.info("调用 core.llm.chat…")
    reply = chat(to_send)
    log.info("收到回复，长度=%d 字符", len(reply or ""))
    print("模型回复（基于截断后的最近几轮）:")
    print(reply or "(无)")


if __name__ == "__main__":
    main()
