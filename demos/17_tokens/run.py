"""
Demo 17：Token 与成本意识。用简单启发式估算消息长度（字符数 → 约 token 数），建立「长度与成本」的概念。
"""
import logging
import os
import sys

_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _root not in sys.path:
    sys.path.insert(0, _root)

from core.demo_log import setup_demo_logging

setup_demo_logging()
log = logging.getLogger(__name__)


def rough_token_count(text: str) -> int:
    """
    粗略估算：中文约 1.5 字符/token，英文约 4 字符/token。
    这里用整体 2 字符/token 做近似（仅用于演示）。
    """
    if not text:
        return 0
    # 简化：按字符数 / 2 近似（中英混合）
    return max(1, len(text) // 2)


def main():
    log.info("本 demo 不调用 LLM，仅做消息长度与约 token 估算")
    # 示例：一段 system + user 消息
    system = "你是一个有帮助的助手。"
    user = "请用三句话介绍大模型应用开发中「上下文长度」的概念。"
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]

    total_chars = 0
    total_tokens_approx = 0
    print("消息长度与近似 Token 估算（启发式，非精确）：\n")
    for m in messages:
        content = (m.get("content") or "")
        total_chars += len(content)
        t = rough_token_count(content)
        total_tokens_approx += t
        print(f"  [{m.get('role')}] 字符数={len(content)}, 约 token≈{t}")
    log.info("合计: 字符数=%d, 约 token≈%d", total_chars, total_tokens_approx)
    print(f"\n  合计: 字符数={total_chars}, 约 token≈{total_tokens_approx}")
    print("\n说明：实际 token 数需用模型对应的 tokenizer（如 tiktoken）或 API 返回的 usage 获取。")
    print("成本 ≈ (输入 token + 输出 token) × 单价；控制上下文长度可控制单次调用成本。")


if __name__ == "__main__":
    main()
