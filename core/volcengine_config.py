"""
火山方舟（Ark）API 配置：供 core.llm 使用。
加载顺序：.env 文件（项目根目录）-> 环境变量 -> 默认值。
"""
import os
from pathlib import Path

# 尝试从项目根目录的 .env 加载（需安装 python-dotenv）
def _load_dotenv() -> None:
    try:
        from dotenv import load_dotenv
        root = Path(__file__).resolve().parent.parent
        env_file = root / ".env"
        if env_file.is_file():
            load_dotenv(env_file, override=False)
    except ImportError:
        pass


_load_dotenv()

ARK_API_KEY = os.environ.get("ARK_API_KEY", "").strip()
ARK_MODEL_ID = (os.environ.get("ARK_MODEL_ID") or "").strip() or "deepseek-v3-2-251201"
ARK_TIMEOUT = int(os.environ.get("ARK_TIMEOUT") or "120")
