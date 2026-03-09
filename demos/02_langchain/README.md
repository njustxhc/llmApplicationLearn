# 02 LangChain 入门

使用 LangChain 的 LCEL 构建链：Prompt 模板 → LLM → 输出。LLM 通过封装 `core.llm.chat` 接入。

## 基础用例

单链 prompt → llm：`run.py`。

```bash
python -m demos.02_langchain.run
```

## 进阶用例

RAG 链（检索 → prompt → LLM）：`run_advanced.py`。

```bash
python -m demos.02_langchain.run_advanced
```
