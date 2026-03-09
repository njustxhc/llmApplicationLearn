"""长期记忆：RAG 检索 long_term/memories.md，并可追加新记忆。"""
from pathlib import Path
import os
import sys

_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _root not in sys.path:
    sys.path.insert(0, _root)

LONG_TERM_DIR = Path(__file__).resolve().parent / "long_term"
MEMORIES_FILE = LONG_TERM_DIR / "memories.md"

def add_memory(fact: str) -> None:
    MEMORIES_FILE.parent.mkdir(parents=True, exist_ok=True)
    line = (fact or "").strip()
    if not line:
        return
    if not line.endswith("\n"):
        line += "\n"
    with open(MEMORIES_FILE, "a", encoding="utf-8") as f:
        f.write(line)

def get_long_term_context(query: str, top_k: int = 3) -> str:
    if not MEMORIES_FILE.is_file():
        return ""
    try:
        from core.rag_doc.retriever import build_index, retrieve
    except Exception:
        return ""
    chunks, vectorizer, doc_matrix = build_index(LONG_TERM_DIR)
    if not chunks:
        return ""
    text = retrieve(query, chunks, vectorizer, doc_matrix, top_k=top_k)
    if not text:
        return ""
    return f"【长期记忆（与当前问题相关）】\n{text}"

def extract_and_save_memories(user_text: str, assistant_text: str) -> None:
    from core.llm import chat
    prompt = f"从下面这段对话中提取 0～2 条值得长期记住的事实，每条一行。若无则输出「无」。\n\n用户: {user_text[:300]}\n助手: {assistant_text[:300]}"
    reply = chat([{"role": "user", "content": prompt}])
    if not reply:
        return
    for line in (reply or "").strip().splitlines():
        line = line.strip()
        if not line or line == "无" or line.startswith("无") or len(line) < 3:
            continue
        add_memory(line)
