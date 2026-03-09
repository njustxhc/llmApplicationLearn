"""
Demo 04 进阶：多工具或 LLM 选工具+调用。规划见 docs/进阶Demo实现说明与计划.md。
当前演示：调用 list_tools_client 列出 MCP Server 工具（需先另启 Server：python -m demos.04_mcp.server）。
"""
import subprocess
import sys
import os
_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _root not in sys.path:
    sys.path.insert(0, _root)

def main():
    print("【进阶】MCP 客户端列出工具列表。若未启动 Server 会连接失败。")
    print("请先在另一终端运行: python -m demos.04_mcp.server\n")
    proc = subprocess.run(
        [sys.executable, "-m", "demos.04_mcp.list_tools_client"],
        cwd=_root,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=10,
    )
    print(proc.stdout or "")
    if proc.stderr:
        print("stderr:", proc.stderr, file=sys.stderr)

if __name__ == "__main__":
    main()
