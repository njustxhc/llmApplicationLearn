"""
Demo 15：Temperature 与采样参数。同一问题用不同 temperature 调用，对比输出稳定性与多样性。
"""
import logging
import os
import sys

_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _root not in sys.path:
    sys.path.insert(0, _root)

from core.demo_log import setup_demo_logging
from core.llm import get_client
from core.llm.config import ARK_API_KEY, ARK_MODEL_ID

setup_demo_logging()
log = logging.getLogger(__name__)

if not ARK_API_KEY:
    print("未配置 ARK_API_KEY，跳过本 demo")
    sys.exit(0)

USER_QUERY = "用一句话说出一个数字（1 到 10 之间）。"


def call_with_temperature(temperature: float) -> str:
    client = get_client()
    resp = client.chat.completions.create(
        model=ARK_MODEL_ID,
        messages=[{"role": "user", "content": USER_QUERY}],
        temperature=temperature,
    )
    if not resp.choices:
        return "(无)"
    return (resp.choices[0].message.content or "").strip() or "(无)"


def main():
    log.info("同一问题，分别用 temperature=0.2 与 0.9 调用")
    print("同一问题，不同 temperature 下的输出对比：\n")
    for temp, label in [(0.2, "低 temperature（更稳定、重复性高）"), (0.9, "高 temperature（更多样、随机性强）")]:
        log.info("调用 API，temperature=%s", temp)
        print(f"--- temperature={temp} ({label}) ---")
        try:
            reply = call_with_temperature(temp)
            log.info("收到回复: %s", (reply or "")[:80] + ("…" if len(reply or "") > 80 else ""))
            print(reply)
        except Exception as e:
            log.exception("调用失败")
            print(f"调用失败: {e}")
        print()


if __name__ == "__main__":
    main()
