"""
Demo 08：Embedding 与向量检索 RAG。用 core.rag_doc 检索后交给 core.llm 回答。
"""
import logging
import os
import sys
from pathlib import Path

_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _root not in sys.path:
    sys.path.insert(0, _root)

from core.demo_log import setup_demo_logging
from core.llm import chat
from core.rag_doc.retriever import build_index, retrieve

setup_demo_logging()
log = logging.getLogger(__name__)

DOCS_DIR = Path(__file__).resolve().parent.parent.parent / "core" / "rag_doc" / "documents"

def main():
    log.info("文档目录: %s", DOCS_DIR)
    if not DOCS_DIR.is_dir():
        log.warning("文档目录不存在")
        print("请确保 core/rag_doc/documents/ 存在并放入 .txt/.md")
        return
    log.info("构建索引（TF-IDF）…")
    chunks, vectorizer, doc_matrix = build_index(DOCS_DIR)
    if not chunks:
        log.warning("未找到可索引文档")
        print("未找到可索引文档")
        return
    log.info("索引完成，共 %d 个片段", len(chunks))
    query = "这个项目有哪些功能？"
    log.info("检索 query=%s, top_k=3", query)
    context = retrieve(query, chunks, vectorizer, doc_matrix, top_k=3)
    log.info("检索到上下文长度=%d 字符，注入 system 并调用 LLM", len(context))
    messages = [
        {"role": "system", "content": f"根据以下检索到的文档片段回答问题。\n\n【检索片段】\n{context}"},
        {"role": "user", "content": query},
    ]
    reply = chat(messages)
    log.info("收到回复，长度=%d 字符", len(reply or ""))
    print("问题:", query)
    print("回答:", reply or "(无回复)")

if __name__ == "__main__":
    main()
