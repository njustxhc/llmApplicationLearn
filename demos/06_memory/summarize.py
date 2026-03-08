"""超长对话时用 LLM 做摘要，将旧消息替换为一条「此前对话摘要」的 system 消息。"""
import os
import sys

_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _root not in sys.path:
    sys.path.insert(0, _root)

from core.llm import chat

MAX_MESSAGES_BEFORE_SUMMARY = 10
KEEP_RECENT = 4

def summarize_old_messages(messages: list[dict]) -> str | None:
    if not messages:
        return None
    rest = messages[1:] if messages and (messages[0].get("role") or "").lower() == "system" else list(messages)
    if len(rest) <= MAX_MESSAGES_BEFORE_SUMMARY - KEEP_RECENT:
        return None
    to_summarize = rest[: -(KEEP_RECENT)]
    if not to_summarize:
        return None
    parts = [f"[{m.get('role','')}]: {(m.get('content') or '')[:200]}{'...' if len((m.get('content') or '')) > 200 else ''}" for m in to_summarize]
    text = "\n\n".join(parts)
    prompt = f"请将以下对话压缩成一段简短摘要（3～5 句话），保留关键事实。\n\n对话内容：\n{text}\n\n请只输出摘要内容。"
    summary = chat([{"role": "user", "content": prompt}])
    return (summary or "").strip() or None

def maybe_summarize(messages: list[dict]) -> list[dict]:
    if not messages:
        return messages
    system_msg = messages[0] if messages and (messages[0].get("role") or "").lower() == "system" else None
    rest = messages[1:] if system_msg else list(messages)
    if len(rest) <= MAX_MESSAGES_BEFORE_SUMMARY:
        return messages
    summary = summarize_old_messages(messages)
    if not summary:
        keep = messages[:1] + rest[-(KEEP_RECENT):] if system_msg else rest[-(KEEP_RECENT):]
        return keep
    new_list = []
    if system_msg:
        new_list.append(system_msg)
    new_list.append({"role": "system", "content": "【此前对话摘要】\n" + summary})
    new_list.extend(rest[-(KEEP_RECENT):])
    return new_list
