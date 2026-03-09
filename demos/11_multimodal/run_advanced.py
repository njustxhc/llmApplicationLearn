"""
Demo 11 进阶：真实传图或 TTS/STT。规划见 docs/进阶Demo实现说明与计划.md。
当前为占位：多模态消息结构已见基础用例，进阶需接入支持 Vision 的 API。
"""
import sys
import os
_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _root not in sys.path:
    sys.path.insert(0, _root)

def main():
    print("【进阶】多模态进阶（传图 / TTS / STT）")
    print("需使用支持图像或语音的 API。规划与接口说明见 docs/进阶Demo实现说明与计划.md 第三节 11 多模态。")
    print("当前为占位，请先完成基础用例中的多模态消息结构演示。")

if __name__ == "__main__":
    main()
