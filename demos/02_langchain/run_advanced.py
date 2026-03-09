"""
Demo 02 进阶：LCEL 链中接入 RAG。链为「检索 → 构造提示 → 调用 LLM」，
从 core.rag_doc 取上下文注入 prompt，再交给 LLM 生成有依据的回复。
"""
import logging
import os
import sys

_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _root not in sys.path:
    sys.path.insert(0, _root)

from core.demo_log import setup_demo_logging
from core.llm import chat
from core.rag_doc import get_rag_context
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda

setup_demo_logging()
log = logging.getLogger(__name__)


def _invoke_llm(messages) -> str:
    raw = []
    for m in messages:
        role = "system" if getattr(m, "type", "") == "system" else "user"
        raw.append({"role": role, "content": getattr(m, "content", "") or ""})
    reply = chat(raw)
    return reply or ""


def main():
    question = "这个项目有哪些功能？"
    log.info("进阶：RAG 链 = 检索 → prompt → LLM")
    log.info("1. 检索：get_rag_context(%s, top_k=3)", repr(question))
    context = get_rag_context(question, top_k=3)
    if context.startswith("[文档 RAG") and "未找到" in context:
        log.warning("检索无结果，使用空上下文")
        context = "（暂无检索到文档片段）"
    log.info("2. 构造提示并调用 LLM")
    prompt = ChatPromptTemplate.from_messages([
        ("system", "根据以下检索到的文档片段回答问题，回答需有依据。\n\n【检索片段】\n{context}"),
        ("human", "{question}"),
    ])
    llm_runnable = RunnableLambda(lambda x: _invoke_llm(x))
    chain = prompt | llm_runnable
    result = chain.invoke({"context": context, "question": question})
    result = (result or "").strip() or "(无回复)"
    log.info("收到回复，长度=%d 字符", len(result))
    print("问题:", question)
    print("回答:", result)


if __name__ == "__main__":
    main()
