"""
会话持久化：将会话消息保存到 memory.md、从 memory.md 加载。
格式：Markdown，每个会话一个 ## Session: <id>，每轮为 ### Turn N 与 user/assistant 块。
"""
from pathlib import Path
import re

DEFAULT_MEMORY_FILE = Path(__file__).resolve().parent / "memory.md"
SESSION_HEADER = re.compile(r"^##\s*Session:\s*(.+)$", re.MULTILINE)
TURN_HEADER = re.compile(r"^###\s*Turn\s+(\d+)\s*$", re.MULTILINE)

def _messages_to_md(session_id: str, messages: list[dict]) -> str:
    lines = [f"## Session: {session_id}", ""]
    turn = 0
    for m in messages:
        role = (m.get("role") or "").strip().lower()
        content = (m.get("content") or "").strip()
        if role == "system":
            lines.append("### System")
            lines.append("- " + content.replace("\n", "\n  "))
            lines.append("")
            continue
        if role in ("user", "assistant"):
            turn += 1
            lines.append(f"### Turn {turn}")
            lines.append(f"- {role}:")
            lines.append(content.replace("\n", "\n  ") if content else "(空)")
            lines.append("")
    return "\n".join(lines).strip() + "\n"

def _parse_md(content: str) -> list[dict]:
    messages = []
    current_role = None
    current_lines = []
    for line in content.splitlines():
        if SESSION_HEADER.match(line.strip()):
            continue
        if line.strip() == "### System":
            if current_role is not None and current_lines:
                text = "\n".join(current_lines).strip()
                if text and text != "(空)":
                    messages.append({"role": current_role, "content": text})
            current_role = "system"
            current_lines = []
            continue
        turn_m = TURN_HEADER.match(line.strip())
        if turn_m:
            if current_role is not None and current_lines:
                text = "\n".join(current_lines).strip()
                if text and text != "(空)":
                    messages.append({"role": current_role, "content": text})
            current_role = None
            current_lines = []
            continue
        if line.strip().startswith("- user:"):
            if current_role is not None and current_lines:
                text = "\n".join(current_lines).strip()
                if text and text != "(空)":
                    messages.append({"role": current_role, "content": text})
            current_role = "user"
            current_lines = []
            continue
        if line.strip().startswith("- assistant:"):
            if current_role is not None and current_lines:
                text = "\n".join(current_lines).strip()
                if text and text != "(空)":
                    messages.append({"role": current_role, "content": text})
            current_role = "assistant"
            current_lines = []
            continue
        if line.strip().startswith("- "):
            current_lines.append(line[2:] if len(line) > 2 else "")
            continue
        if current_role is not None:
            current_lines.append(line.strip() if line.startswith("  ") else line)
    if current_role is not None and current_lines:
        text = "\n".join(current_lines).strip()
        if text and text != "(空)":
            messages.append({"role": current_role, "content": text})
    return messages

def load_session(session_id: str = "default", memory_file: str | Path | None = None) -> list[dict]:
    path = Path(memory_file or DEFAULT_MEMORY_FILE)
    if not path.is_file():
        return []
    raw = path.read_text(encoding="utf-8", errors="ignore")
    parts = re.split(r"^##\s*Session:\s*", raw, flags=re.MULTILINE)
    for part in parts:
        if not part.strip():
            continue
        first_line = part.strip().split("\n")[0].strip()
        if first_line == session_id:
            return _parse_md("## Session: " + part)
    return []

def save_session(session_id: str, messages: list[dict], memory_file: str | Path | None = None, append_other_sessions: bool = True) -> None:
    path = Path(memory_file or DEFAULT_MEMORY_FILE)
    other_sections = []
    if append_other_sessions and path.is_file():
        raw = path.read_text(encoding="utf-8", errors="ignore")
        parts = re.split(r"^##\s*Session:\s*", raw, flags=re.MULTILINE)
        for part in parts:
            if not part.strip():
                continue
            first_line = part.strip().split("\n")[0].strip()
            if first_line != session_id:
                other_sections.append("## Session: " + part.strip())
    new_block = _messages_to_md(session_id, messages)
    all_content = "\n\n".join(other_sections + [new_block]).strip() + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(all_content, encoding="utf-8")
