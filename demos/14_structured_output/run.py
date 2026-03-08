"""
Demo 14：结构化输出。通过 prompt 约束让模型返回 JSON，再解析并校验，用于下游程序处理。
"""
import json
import logging
import os
import re
import sys

_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _root not in sys.path:
    sys.path.insert(0, _root)

from core.demo_log import setup_demo_logging
from core.llm import chat

setup_demo_logging()
log = logging.getLogger(__name__)

USER_QUERY = "请介绍 Python 和 JavaScript 两种语言，各用一句话。"

SYSTEM = """你只能输出一个合法的 JSON 对象，不要输出任何其他文字。
格式要求：{"languages": [{"name": "语言名", "summary": "一句话介绍"}, ...]}
只包含 name 和 summary 两个字段。"""


def extract_json(text: str) -> dict | None:
    """从回复中尝试提取 JSON 对象。"""
    if not text or not text.strip():
        return None
    text = text.strip()
    # 尝试直接解析
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    # 尝试提取 ```json ... ``` 或 {...}
    for pattern in [r"```(?:json)?\s*([\s\S]*?)\s*```", r"(\{[\s\S]*\})"]:
        m = re.search(pattern, text)
        if m:
            try:
                return json.loads(m.group(1).strip())
            except json.JSONDecodeError:
                continue
    return None


def main():
    log.info("构造 messages（system=JSON 格式约束 + user 问题）")
    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": USER_QUERY},
    ]
    log.info("调用 core.llm.chat…")
    reply = chat(messages)
    log.info("收到回复，长度=%d 字符，尝试解析 JSON", len(reply or ""))
    print("模型原始回复:")
    print(reply or "(无)")
    print()

    obj = extract_json(reply or "")
    if obj and "languages" in obj:
        log.info("解析成功，languages 条数=%d", len(obj["languages"]))
        print("解析后的结构化数据:")
        for i, lang in enumerate(obj["languages"], 1):
            name = lang.get("name", "?")
            summary = lang.get("summary", "?")
            print(f"  {i}. {name}: {summary}")
    else:
        log.warning("解析失败或格式不符合要求")
        print("解析失败或格式不符合要求，无法得到结构化数据。")


if __name__ == "__main__":
    main()
