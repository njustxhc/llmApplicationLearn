"""
Demo 09：评估与评测。若干题目，LLM 作答后用期望关键词简单判分。使用 core.llm。
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

CASES = [
    ("1+1等于几？", ["2"], 1),
    ("Python 是哪一年发布的？请只回答年份。", ["1991"], 1),
    ("列举一种编程语言。", ["Python", "Java", "C", "JavaScript", "Go"], 1),
]

def score(reply: str, keywords: list[str], at_least: int) -> bool:
    if not reply:
        return False
    reply_lower = reply.lower()
    return sum(1 for k in keywords if k.lower() in reply_lower) >= at_least

def main():
    log.info("开始评测，共 %d 题", len(CASES))
    passed = 0
    for i, (q, keywords, at_least) in enumerate(CASES, 1):
        log.info("第 %d/%d 题: %s", i, len(CASES), q[:40] + "…" if len(q) > 40 else q)
        reply = chat([{"role": "user", "content": q}]) or ""
        ok = score(reply, keywords, at_least)
        passed += 1 if ok else 0
        log.info("回复长度=%d, 期望关键词=%s, 通过=%s", len(reply), keywords, ok)
        print(f"Q: {q}")
        print(f"A: {reply[:150]}{'...' if len(reply) > 150 else ''}")
        print(f"通过: {ok}\n")
    log.info("评测结束，通过 %d/%d", passed, len(CASES))
    print(f"通过: {passed}/{len(CASES)}")

if __name__ == "__main__":
    main()
