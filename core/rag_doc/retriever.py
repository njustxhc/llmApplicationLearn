"""
文档 RAG 检索：从本地文档目录加载、分块、建 TF-IDF 索引，按查询返回最相关片段。
"""

from __future__ import annotations

import re
from pathlib import Path


def _simple_chunk(text: str, chunk_size: int = 500, overlap: int = 80) -> list[str]:
    """按字符数分块，带重叠。"""
    text = (text or "").strip()
    if not text:
        return []
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start = end - overlap if end < len(text) else len(text)
    return chunks


def _load_docs_from_dir(docs_dir: str | Path) -> list[tuple[str, str]]:
    """从目录加载 .txt / .md 文件，返回 (文件路径, 内容) 列表。"""
    docs_dir = Path(docs_dir)
    if not docs_dir.is_dir():
        return []
    out = []
    for ext in ("*.txt", "*.md"):
        for p in docs_dir.glob(ext):
            try:
                raw = p.read_text(encoding="utf-8", errors="ignore")
                text = re.sub(r"\s+", " ", raw).strip()
                if text:
                    out.append((str(p.name), text))
            except Exception:
                continue
    return out


def build_index(docs_dir: str | Path) -> tuple[list[str], object, object]:
    """
    从文档目录建索引。返回 (chunks, vectorizer, doc_matrix)。
    """
    docs = _load_docs_from_dir(docs_dir)
    if not docs:
        return [], None, None
    all_chunks = []
    for name, text in docs:
        for c in _simple_chunk(text):
            all_chunks.append(f"[{name}]\n{c}")
    if not all_chunks:
        return [], None, None
    from sklearn.feature_extraction.text import TfidfVectorizer
    vectorizer = TfidfVectorizer(max_features=5000, token_pattern=r"(?u)\b\w+\b")
    doc_matrix = vectorizer.fit_transform(all_chunks)
    return all_chunks, vectorizer, doc_matrix


def retrieve(
    query: str,
    chunks: list[str],
    vectorizer: object,
    doc_matrix: object,
    top_k: int = 3,
) -> str:
    """
    检索与 query 最相关的 top_k 个片段，拼成一段文本。
    """
    if not query or not chunks or vectorizer is None or doc_matrix is None:
        return ""
    try:
        from sklearn.metrics.pairwise import linear_kernel
        q_vec = vectorizer.transform([query.strip()])
        sim = linear_kernel(q_vec, doc_matrix).flatten()
        if sim.size == 0:
            return ""
        top_indices = sim.argsort()[-top_k:][::-1]
        parts = [chunks[i] for i in top_indices if i < len(chunks)]
        return "\n\n---\n\n".join(parts) if parts else ""
    except Exception:
        return ""
