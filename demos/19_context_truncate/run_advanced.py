"""
Demo 19 进阶：按 token 数截断或摘要+截断。规划见 docs/进阶Demo实现说明与计划.md。
当前演示：在「保留最近 K 条」基础上，对超出部分做简单「前几条合并为一条摘要」再与最近 K 条一起发送。
"""
import os
import sys
_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _root not in sys.path:
    sys.path.insert(0, _root)
from core.llm import chat

KEEP = 2  # 最近 2 条（1 轮）

def main():
    history = [
        {"role": "user", "content": "什么是 Python？"},
        {"role": "assistant", "content": "Python 是编程语言。"},
        {"role": "user", "content": "有什么特点？"},
        {"role": "assistant", "content": "易读易学。"},
        {"role": "user", "content": "总结一下我们聊过的内容。"},
    ]
    if len(history) <= KEEP + 1:
        to_send = history
        summary_msg = None
    else:
        old = history[: -(KEEP + 1)]
        summary_text = "（此前对话共 %d 条，此处省略）" % len(old)
        summary_msg = [{"role": "system", "content": "此前对话摘要: " + summary_text}]
        to_send = summary_msg + history[-(KEEP + 1) :]
    print("【进阶】摘要+截断：较早消息用摘要代替，保留最近 %d 条\n" % KEEP)
    print("发给模型的消息条数:", len(to_send))
    reply = chat(to_send)
    print("模型回复:", reply or "(无)")

if __name__ == "__main__":
    main()
