"""
Demo 06：多轮对话与记忆。会话持久化 memory.md、超长摘要、长期记忆 RAG。使用 core.llm。
"""
import logging
import os
import sys

_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _root not in sys.path:
    sys.path.insert(0, _root)

from core.demo_log import setup_demo_logging
from core.llm import chat
from .memory_store import load_session, save_session, DEFAULT_MEMORY_FILE
from .summarize import maybe_summarize
from .long_term import get_long_term_context, extract_and_save_memories

setup_demo_logging()
log = logging.getLogger(__name__)

SESSION_ID = "default"
SYSTEM_PROMPT = "你是助手。请简短回答，并记住对话中提到的信息。若上下文中有「此前对话摘要」或「长期记忆」，请结合使用。"

def ensure_system(messages: list[dict]) -> list[dict]:
    if not messages:
        return [{"role": "system", "content": SYSTEM_PROMPT}]
    if (messages[0].get("role") or "").lower() != "system":
        return [{"role": "system", "content": SYSTEM_PROMPT}] + list(messages)
    return list(messages)

def inject_long_term(messages: list[dict], query: str) -> list[dict]:
    ctx = get_long_term_context(query, top_k=3)
    if not ctx:
        return messages
    system = messages[0] if messages and (messages[0].get("role") or "").lower() == "system" else None
    if not system:
        return [{"role": "system", "content": ctx}] + list(messages)
    new_system = {"role": "system", "content": system.get("content", "") + "\n\n" + ctx}
    return [new_system] + messages[1:]

def main():
    log.info("加载会话: SESSION_ID=%s", SESSION_ID)
    messages = load_session(SESSION_ID)
    messages = ensure_system(messages)
    print(f"会话存储文件: {DEFAULT_MEMORY_FILE}")
    if len(messages) > 1:
        print(f"已从 memory.md 加载 {len(messages) - 1} 条历史消息。")
    else:
        print("无历史会话，从新对话开始。")
    print("输入内容按 Enter 发送；输入 quit 或 exit 结束对话。\n")
    while True:
        try:
            user_text = input("你: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n对话已结束。")
            break
        if not user_text:
            continue
        if user_text.lower() in ("quit", "exit", "q"):
            print("对话已结束。会话已写入 memory.md。")
            break
        messages = inject_long_term(messages, user_text)
        messages = maybe_summarize(messages)
        messages.append({"role": "user", "content": user_text})
        log.info("当前 messages 条数=%d，调用 LLM…", len(messages))
        reply = chat(messages)
        if not reply:
            reply = "(无回复)"
        messages.append({"role": "assistant", "content": reply})
        print(f"助手: {reply}\n")
        save_session(SESSION_ID, messages)
        extract_and_save_memories(user_text, reply)

if __name__ == "__main__":
    main()