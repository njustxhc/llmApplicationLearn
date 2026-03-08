"""
文档 RAG 模块：从本地文档目录检索相关片段，供 demos 与 learn_web 注入到对话上下文中。

用法:
  from core.rag_doc import get_rag_context
  context = get_rag_context("用户问题", top_k=3)
"""

from pathlib import Path

from .retriever import build_index, retrieve

_cached_docs_dir: str | None = None
_cached_chunks: list = []
_cached_vectorizer = None
_cached_doc_matrix = None


def get_rag_context(
    query: str,
    top_k: int = 3,
    docs_dir: str | Path | None = None,
) -> str:
    """
    根据用户问题从文档目录检索相关片段，返回可注入 system 的上下文文本。
    若 docs_dir 未传，使用本模块同级的 documents 目录。
    """
    global _cached_docs_dir, _cached_chunks, _cached_vectorizer, _cached_doc_matrix
    if docs_dir is None:
        docs_dir = Path(__file__).resolve().parent / "documents"
    docs_dir = str(Path(docs_dir).resolve())
    if _cached_docs_dir != docs_dir or not _cached_chunks:
        _cached_docs_dir = docs_dir
        _cached_chunks, _cached_vectorizer, _cached_doc_matrix = build_index(docs_dir)
    if not _cached_chunks:
        return "[文档 RAG：未找到文档或 documents 目录为空，请向 core/rag_doc/documents/ 放入 .txt/.md 文件]"
    text = retrieve(
        query,
        _cached_chunks,
        _cached_vectorizer,
        _cached_doc_matrix,
        top_k=top_k,
    )
    if not text:
        return "[文档 RAG：检索无结果]"
    return f"以下是从本地文档中检索到的相关内容，请结合这些信息回答用户问题：\n\n{text}"
