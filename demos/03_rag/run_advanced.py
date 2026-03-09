"""
Demo 03 进阶：多路检索或带引用标注。规划见 docs/进阶Demo实现说明与计划.md。
当前为占位，后续将实现多路检索或答案中标注引用来源。
"""
import sys
import os
_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _root not in sys.path:
    sys.path.insert(0, _root)
from core.rag_doc import get_rag_context
from core.llm import chat

def main():
    query = "这个项目有哪些功能？"
    ctx = get_rag_context(query, top_k=5)
    messages = [
        {"role": "system", "content": f"根据以下检索片段回答，并在答案中标注【来源】。\n\n【检索片段】\n{ctx}"},
        {"role": "user", "content": query},
    ]
    reply = chat(messages)
    print("问题:", query)
    print("回答（进阶：带引用意识）:", reply or "(无回复)")

if __name__ == "__main__":
    main()
