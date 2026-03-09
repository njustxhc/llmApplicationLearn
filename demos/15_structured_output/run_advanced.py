"""
Demo 15 进阶：多实体抽取。从长文本中抽取多个实体，输出 JSON 数组。
"""
import json
import os
import re
import sys
_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _root not in sys.path:
    sys.path.insert(0, _root)
from core.llm import chat

def extract_json(text):
    text = (text or "").strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    m = re.search(r"(\{[\s\S]*\}|\[[\s\S]*\])", text)
    if m:
        try:
            return json.loads(m.group(1))
        except json.JSONDecodeError:
            pass
    return None

def main():
    system = "你只能输出一个 JSON 数组，每项为 {\"name\":\"人名\",\"role\":\"身份\"}。不要其他文字。"
    user = "从下面文本中抽取出现的人名及身份：张三是一名工程师，李四是产品经理，王五负责设计。"
    reply = chat([{"role": "system", "content": system}, {"role": "user", "content": user}]) or ""
    print("【进阶】多实体抽取\n")
    print("原文:", user)
    print("回复:", reply)
    obj = extract_json(reply)
    if obj:
        print("解析结果:", json.dumps(obj, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
