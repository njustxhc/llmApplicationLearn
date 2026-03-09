"""
Demo 17 进阶：区分可重试/不可重试错误。规划见 docs/进阶Demo实现说明与计划.md。
当前演示：封装 chat_with_retry 时对异常类型做判断，仅对「可重试」错误重试并打印策略说明。
"""
import os
import sys
_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _root not in sys.path:
    sys.path.insert(0, _root)
from core.llm import chat

def is_retryable(e):
    """简单判断：超时、连接错误、5xx 可重试；4xx（除 429）一般不重试。"""
    msg = str(e).lower()
    if "429" in msg or "rate" in msg or "limit" in msg:
        return True  # 限流可重试
    if "timeout" in msg or "connection" in msg or "5" in msg:
        return True
    if "400" in msg or "401" in msg or "403" in msg:
        return False
    return True  # 默认重试

def main():
    print("【进阶】可重试 vs 不可重试错误策略")
    print("可重试：超时、连接错误、5xx、429 限流。不可重试：400/401/403 等。")
    print("当前仅做策略说明；实际重试逻辑见 run.py 的 chat_with_retry。\n")
    messages = [{"role": "user", "content": "说你好"}]
    try:
        reply = chat(messages)
        print("调用成功:", (reply or "")[:50])
    except Exception as e:
        print("若调用失败，是否重试:", is_retryable(e))

if __name__ == "__main__":
    main()
