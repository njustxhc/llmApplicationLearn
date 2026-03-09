"""
Demo 16 进阶：同一参数多次采样，观察多样性。
"""
import os
import sys
_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _root not in sys.path:
    sys.path.insert(0, _root)
from core.llm import get_client
from core.llm.config import ARK_API_KEY, ARK_MODEL_ID

def main():
    if not ARK_API_KEY:
        print("未配置 ARK_API_KEY，跳过")
        return
    q = "说一个 1～5 之间的整数。"
    client = get_client()
    print("【进阶】同一问题 temperature=0.8 采样 3 次\n")
    for i in range(1, 4):
        r = client.chat.completions.create(model=ARK_MODEL_ID, messages=[{"role": "user", "content": q}], temperature=0.8)
        out = (r.choices[0].message.content or "").strip() if r.choices else "(无)"
        print(f"第{i}次:", out)

if __name__ == "__main__":
    main()
