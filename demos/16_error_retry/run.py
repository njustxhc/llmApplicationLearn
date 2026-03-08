"""
Demo 16：错误处理与重试。对 LLM 调用做重试与退避，演示如何提高请求的健壮性。
"""
import logging
import os
import sys
import time

_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _root not in sys.path:
    sys.path.insert(0, _root)

from core.demo_log import setup_demo_logging
from core.llm import chat

setup_demo_logging()
log = logging.getLogger(__name__)

USER_QUERY = "用一句话说你好。"

MAX_RETRIES = 3
BASE_DELAY = 1.0


def chat_with_retry(messages, max_retries=MAX_RETRIES):
    """带重试的 chat：失败时等待后重试，指数退避。"""
    last_error = None
    for attempt in range(max_retries):
        try:
            reply = chat(messages)
            if reply is not None:
                return reply
            last_error = "模型返回空内容"
        except Exception as e:
            last_error = e
            log.warning("第 %d 次调用失败: %s", attempt + 1, last_error)
            print(f"  第 {attempt + 1} 次调用失败: {last_error}")
        if attempt < max_retries - 1:
            delay = BASE_DELAY * (2 ** attempt)
            log.info("%.1fs 后重试（指数退避）…", delay)
            print(f"  {delay:.1f}s 后重试...")
            time.sleep(delay)
    raise last_error if isinstance(last_error, Exception) else RuntimeError(last_error or "未知错误")


def main():
    log.info("带重试的 LLM 调用，最多 %d 次，指数退避", MAX_RETRIES)
    print("演示：带重试的 LLM 调用（最多 %d 次，指数退避）\n" % MAX_RETRIES)
    messages = [{"role": "user", "content": USER_QUERY}]
    try:
        log.info("开始 chat_with_retry…")
        reply = chat_with_retry(messages)
        log.info("成功，回复长度=%d", len(reply or ""))
        print("最终回复:", reply)
    except Exception as e:
        log.error("全部重试后仍失败: %s", e)
        print("全部重试后仍失败:", e)


if __name__ == "__main__":
    main()
