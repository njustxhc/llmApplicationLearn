"""
Demo 02：检索增强（RAG）。从 core.rag_doc 检索文档片段，再交给 core.llm 生成回答。
"""
import logging
import os
import sys

_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _root not in sys.path:
    sys.path.insert(0, _root)

from core.demo_log import setup_demo_logging
from core.llm import chat
from core.rag_doc import get_rag_context

setup_demo_logging()
log = logging.getLogger(__name__)


def main():
    query = "这个项目有哪些功能？"
    log.info("用户问题: %s", query)
    log.info("调用 core.rag_doc.get_rag_context(query, top_k=3)")
    context = get_rag_context(query, top_k=3)
    if context.startswith("[文档 RAG") and "未找到" in context:
        log.warning("检索无结果，跳过 LLM 调用")
        print(context)
        return
    log.info("检索到上下文，长度=%d 字符，注入 system 消息", len(context))
    messages = [
        {"role": "system", "content": f"根据以下检索到的文档片段回答问题。\n\n【检索片段】\n{context}"},
        {"role": "user", "content": query},
    ]
    log.info("调用 core.llm.chat，请求 API…")
    reply = chat(messages)
    log.info("收到回复，长度=%d 字符", len(reply or ""))
    print("问题:", query)
    print("回答:", reply or "(无回复)")

if __name__ == "__main__":
    main()
