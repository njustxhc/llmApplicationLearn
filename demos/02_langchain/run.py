"""
Demo 02：LangChain 入门。使用 LangChain 的 LCEL 构建链：Prompt -> LLM -> 输出。
LLM 通过封装 core.llm.chat 接入，与项目现有配置一致。
"""
import logging
import os
import sys

_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _root not in sys.path:
    sys.path.insert(0, _root)

from core.demo_log import setup_demo_logging
from core.llm import chat
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda

setup_demo_logging()
log = logging.getLogger(__name__)


def _invoke_llm(messages) -> str:
    """将 LangChain 消息列表转为 core.llm.chat 格式并调用。"""
    raw = []
    for m in messages:
        role = "system" if getattr(m, "type", "") == "system" else "user"
        raw.append({"role": role, "content": getattr(m, "content", "") or ""})
    reply = chat(raw)
    return reply or ""


def main():
    log.info("构建 LCEL 链：ChatPromptTemplate | RunnableLambda(LLM)")
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个简洁的助手，用一两句话回答。"),
        ("human", "{question}"),
    ])
    llm_runnable = RunnableLambda(lambda x: _invoke_llm(x))
    chain = prompt | llm_runnable

    question = "用一句话介绍 LangChain 是什么。"
    log.info("调用 chain.invoke(question=%s)", repr(question))
    result = chain.invoke({"question": question})
    log.info("收到回复，长度=%d 字符", len(result or ""))

    print("问题:", question)
    print("回答:", result or "(无回复)")


if __name__ == "__main__":
    main()
