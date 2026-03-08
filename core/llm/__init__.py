"""
LLM 统一调用模块：火山方舟（Ark）API，供 demos 与 learn_web 复用。

用法:
  from core.llm import get_client, chat, chat_stream
  from core.llm.config import ARK_API_KEY, ARK_MODEL_ID, ARK_TIMEOUT
"""

from core.llm.config import ARK_API_KEY, ARK_MODEL_ID, ARK_TIMEOUT, load_config
from core.llm.client import get_client, chat, chat_stream

__all__ = [
    "get_client",
    "chat",
    "chat_stream",
    "ARK_API_KEY",
    "ARK_MODEL_ID",
    "ARK_TIMEOUT",
    "load_config",
]
