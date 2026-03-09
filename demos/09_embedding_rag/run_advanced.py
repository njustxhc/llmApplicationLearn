"""
Demo 09 进阶：多段检索合并或真实 Embedding+向量库。规划见 docs/进阶Demo实现说明与计划.md。
当前演示：用更大 top_k 做检索并合并展示，模拟多源检索。
"""
import os
import sys
_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _root not in sys.path:
    sys.path.insert(0, _root)
from core.rag_doc import get_rag_context
from core.llm import chat

def main():
    query = "这个项目有哪些功能？"
    ctx = get_rag_context(query, top_k=5)
    messages = [{"role": "system", "content": f"根据检索片段回答。\n【检索】\n{ctx}"}, {"role": "user", "content": query}]
    print("【进阶】多段检索 (top_k=5) + LLM\n")
    print("问题:", query)
    print("回答:", chat(messages) or "(无回复)")

if __name__ == "__main__":
    main()
