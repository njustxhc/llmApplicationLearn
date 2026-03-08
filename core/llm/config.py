"""
火山方舟（Ark）API 配置：优先 .env（项目根），再环境变量，否则从 core.volcengine_config 默认值。
"""

import os

# 先触发 .env 加载（volcengine_config 内会执行 load_dotenv），再读环境变量
try:
    import core.volcengine_config  # noqa: F401
except Exception:
    pass


def load_config() -> tuple[str, str, int]:
    """返回 (api_key, model_id, timeout)。"""
    api_key = os.environ.get("ARK_API_KEY", "").strip()
    model_id = (os.environ.get("ARK_MODEL_ID") or "").strip()
    timeout = os.environ.get("ARK_TIMEOUT")
    if not api_key or not model_id or timeout is None:
        try:
            from core.volcengine_config import ARK_API_KEY as _KEY, ARK_MODEL_ID as _MID, ARK_TIMEOUT as _TO
            if not api_key:
                api_key = (_KEY or "").strip()
            if not model_id:
                model_id = (_MID or "").strip() or "deepseek-v3-2-251201"
            if timeout is None:
                timeout = str(_TO)
        except Exception:
            pass
    return (
        api_key or "",
        model_id or "deepseek-v3-2-251201",
        int(timeout or "120"),
    )


ARK_API_KEY, ARK_MODEL_ID, ARK_TIMEOUT = load_config()
