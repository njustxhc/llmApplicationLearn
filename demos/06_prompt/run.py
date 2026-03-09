"""
Demo 05：Prompt 工程。日志输出到 stdout，learn_web 前端运行时会一并显示。

涵盖概念：
- System prompt 设计：用 system 消息设定任务、规则，引导模型行为。
- 角色设定：在 system 里明确「你是…」（如技术老师、客服），统一口吻与风格。
- Few-shot：在对话中插入 1～2 个 (user, assistant) 示例，让模型模仿格式或风格。
- CoT（Chain-of-Thought）：要求模型「先一步步思考再给答案」，提升推理与结构化输出。
- 输出格式约束：在 prompt 中规定回答结构（如 1. 2. 3.、JSON、Markdown），便于后续解析。

本 demo 对同一用户问题用不同风格的 prompt 调用 LLM，运行时会打印每种风格对应的 prompt 与模型回复。
"""
import logging
import os
import sys

_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _root not in sys.path:
    sys.path.insert(0, _root)

from core.demo_log import setup_demo_logging
from core.llm import chat

setup_demo_logging()
log = logging.getLogger(__name__)

USER_QUERY = "用三句话介绍一下 Python 语言。"


def _format_messages_for_display(messages: list[dict]) -> str:
    """把 messages 转成可读的 prompt 文本，便于在运行时报出。"""
    parts = []
    for m in messages:
        role = m.get("role", "").upper()
        content = (m.get("content") or "").strip()
        parts.append(f"[{role}]\n{content}")
    return "\n\n".join(parts)


# 每种风格：(显示名称, messages 列表)
STYLES = [
    (
        "1. 默认（无 system）",
        [{"role": "user", "content": USER_QUERY}],
        "不设 system，仅用户问题，模型按默认行为回答。",
    ),
    (
        "2. System prompt + 角色设定",
        [
            {
                "role": "system",
                "content": "你是一位技术老师，面向初学者。回答请简洁、有条理，每条一句话。",
            },
            {"role": "user", "content": USER_QUERY},
        ],
        "用 system 设定「角色」和「风格」，统一输出口吻。",
    ),
    (
        "3. 输出格式约束",
        [
            {
                "role": "system",
                "content": "请严格按以下格式回答：\n1. 第一句：…\n2. 第二句：…\n3. 第三句：…\n不要加其他说明。",
            },
            {"role": "user", "content": USER_QUERY},
        ],
        "在 system 中规定回答结构，便于解析或展示。",
    ),
    (
        "4. Few-shot 示例",
        [
            {
                "role": "system",
                "content": "你是一位技术老师。请用「要点 + 一句话解释」的方式回答，参考下面示例。",
            },
            {"role": "user", "content": "什么是变量？"},
            {
                "role": "assistant",
                "content": "要点：变量是存储数据的容器。\n一句话：编程时用名字代表一块内存，存数字、文字等，可随时修改。",
            },
            {"role": "user", "content": USER_QUERY},
        ],
        "在对话中插入 (user, assistant) 示例，让模型模仿格式与风格。",
    ),
    (
        "5. CoT（链式思考）",
        [
            {
                "role": "system",
                "content": "你是一位技术老师。回答时请先写「思考：」再一步步简要推理，最后在「答案：」后给出三句话结论。",
            },
            {"role": "user", "content": USER_QUERY},
        ],
        "要求先思考再作答，适合需要推理或结构化步骤的问题。",
    ),
]


def main():
    log.info("用户问题: %s", USER_QUERY)
    print("用户问题:", USER_QUERY)
    print()
    for i, (name, messages, concept_note) in enumerate(STYLES, 1):
        log.info("风格 %d/%d: %s", i, len(STYLES), name)
        prompt_display = _format_messages_for_display(messages)
        print("=" * 60)
        print(name)
        print("概念:", concept_note)
        print("-" * 40)
        print("【本风格使用的 Prompt】")
        print(prompt_display)
        print("-" * 40)
        log.info("调用 core.llm.chat（风格: %s）…", name.split(".")[0] if "." in name else name)
        reply = chat(messages)
        log.info("收到回复，长度=%d 字符", len(reply or ""))
        print("【模型回复】")
        print(reply or "(无回复)")
        print()


if __name__ == "__main__":
    main()
