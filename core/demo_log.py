"""
Demo 运行时统一日志配置：输出到 stderr，便于 learn_web 将「运行结果」(stdout) 与「运行日志」(stderr) 分开展示。
各 demo 的 run.py 在入口处调用 setup_demo_logging()，然后用 logging.getLogger(__name__) 打日志即可。
"""
import logging
import sys


def setup_demo_logging(level: int = logging.INFO) -> None:
    """将根 logger 的 handler 设为输出到 stderr，与 print（stdout）分离，前端可分别显示结果与日志。"""
    logging.basicConfig(
        level=level,
        format="[%(levelname)s] %(message)s",
        stream=sys.stderr,
        force=True,
    )
