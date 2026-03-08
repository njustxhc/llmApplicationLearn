"""
Demo 10：多模态。演示文本调用；多模态消息结构见文档。使用 core.llm。
"""
import logging
import os
import sys

_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _root not in sys.path:
    sys.path.insert(0, _root)

from core.demo_log import setup_demo_logging
from core.llm import get_client
from core.llm.config import ARK_MODEL_ID

setup_demo_logging()
log = logging.getLogger(__name__)


def main():
    log.info("获取 LLM 客户端，model=%s", ARK_MODEL_ID)
    client = get_client()
    messages = [{"role": "user", "content": "请用一句话说明：多模态模型可以同时接收文本和图像输入。"}]
    log.info("发起文本调用（非流式）…")
    try:
        resp = client.chat.completions.create(
            model=ARK_MODEL_ID,
            messages=messages,
            thinking={"type": "disabled"},
            stream=False,
        )
        if resp.choices:
            content = (resp.choices[0].message.content or "")[:200]
            log.info("调用成功，回复长度=%d", len(resp.choices[0].message.content or ""))
            print("文本调用成功:", content)
        else:
            log.warning("未返回 content")
            print("未返回内容")
    except Exception as e:
        log.exception("调用异常")
        print("调用异常:", e)
    print("\n多模态消息结构: content 可为 list，含 type=text 与 type=image_url；以火山方舟多模态文档为准。")

if __name__ == "__main__":
    main()
