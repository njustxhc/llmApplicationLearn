# 02 LangChain 入门

在掌握基础 API 调用后，可以借助 **LangChain** 这类框架来组织提示、模型调用与后续处理，形成可复用的「链」或流水线。本讲介绍用 LangChain 的 **LCEL**（LangChain Expression Language）构建一条简单链：Prompt 模板 → LLM → 输出。

---

## 核心概念

### 1. LangChain 与 LCEL

**是什么**：LangChain 是面向大模型应用的开发框架，提供 Prompt 模板、链式调用、工具绑定、记忆等组件。**LCEL** 用 `|` 运算符把各步骤串成链（如 `prompt | llm`），便于组合与复用。

**为什么要有这个概念**：手写多轮消息和解析容易散落；用链可以把「构造提示 → 调模型 → 解析结果」固定成流程，便于维护和扩展（如后续加 RAG、工具调用）。

### 2. Prompt 模板与 Runnable

**是什么**：**ChatPromptTemplate** 根据变量（如 `{question}`）生成 messages；**Runnable** 是 LCEL 中的可执行单元（如封装好的 LLM、解析器）。链由多个 Runnable 按顺序组成。

**为什么要有这个概念**：模板化提示便于复用和 A/B 测试；Runnable 统一了输入输出形态，方便与项目内已有 LLM（如 core.llm）对接。

---

## 本 Demo 做了什么

### 基础用例

- 使用 **ChatPromptTemplate** 定义带 system 与 human 的提示模板。
- 用 **RunnableLambda** 将 `core.llm.chat` 封装为链中的 LLM 节点，与项目现有 API 配置一致。
- 构建链 `prompt | llm`，对单一问题调用并打印回复。
- 运行：点击「运行基础 Demo」或执行 `python -m demos.02_langchain.run`。

### 进阶用例

- 在链中接入 RAG：先调用 `core.rag_doc.get_rag_context` 检索，再将检索结果注入 prompt，形成「检索 → 构造提示 → 调用 LLM」的 LCEL 链。
- 运行：点击「运行进阶 Demo」或执行 `python -m demos.02_langchain.run_advanced`。
