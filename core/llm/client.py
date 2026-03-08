"""
火山方舟 Ark 客户端封装：对话补全（支持非流式/流式）。
"""

from volcenginesdkarkruntime import Ark

from core.llm.config import ARK_API_KEY, ARK_MODEL_ID, ARK_TIMEOUT


def get_client() -> Ark:
    """返回配置好的 Ark 客户端。"""
    return Ark(api_key=ARK_API_KEY, timeout=ARK_TIMEOUT)


def chat(
    messages: list[dict],
    *,
    model: str | None = None,
    stream: bool = False,
    thinking: str = "disabled",
) -> str | None:
    """
    非流式对话，返回 assistant 的 content 文本；异常或无内容时返回 None。
    """
    if not ARK_API_KEY:
        raise ValueError(
            "未配置 ARK_API_KEY。请在项目根目录将 .env.example 复制为 .env 并填写 ARK_API_KEY，"
            "或设置环境变量 ARK_API_KEY。详见 README「环境配置」。"
        )
    client = get_client()
    resp = client.chat.completions.create(
        model=model or ARK_MODEL_ID,
        messages=messages,
        thinking={"type": thinking},
        stream=False,
    )
    if not resp.choices:
        return None
    return (resp.choices[0].message.content or "").strip() or None


def chat_stream(
    messages: list[dict],
    *,
    model: str | None = None,
    thinking: str = "disabled",
):
    """
    流式对话，yield 每个 content delta 的字符串。
    """
    if not ARK_API_KEY:
        raise ValueError(
            "未配置 ARK_API_KEY。请在项目根目录将 .env.example 复制为 .env 并填写 ARK_API_KEY，"
            "或设置环境变量 ARK_API_KEY。详见 README「环境配置」。"
        )
    client = get_client()
    stream = client.chat.completions.create(
        model=model or ARK_MODEL_ID,
        messages=messages,
        thinking={"type": thinking},
        stream=True,
    )
    for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content
