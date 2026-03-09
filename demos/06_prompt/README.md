# 05 Prompt 工程

同一用户问题用不同风格的 prompt 调用大模型，对比输出。运行时会**打印每种风格对应的完整 prompt** 以及模型回复，便于理解各概念。

## 涉及概念

- **System prompt 设计**：用 system 消息设定任务、规则，引导模型整体行为。
- **角色设定**：在 system 里明确「你是…」（如技术老师、客服），统一口吻与风格。
- **Few-shot**：在对话中插入 1～2 个 (user, assistant) 示例，让模型模仿格式或风格。
- **CoT（Chain-of-Thought）**：要求模型「先一步步思考再给答案」，提升推理与结构化输出。
- **输出格式约束**：在 prompt 中规定回答结构（如 1. 2. 3.、JSON、Markdown），便于后续解析。

## 运行

```bash
python -m demos.06_prompt.run
```

输出中会依次展示：默认（无 system）、System+角色、输出格式约束、Few-shot、CoT 五种风格下的 **【本风格使用的 Prompt】** 与 **【模型回复】**。
