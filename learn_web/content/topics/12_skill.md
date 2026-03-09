# 12 Skill 学习与示例

本讲介绍 **Skill**：一种在 OpenClaw 生态中扩展 Agent 能力的规范。通过编写 **SKILL.md** 等约定，可以把自定义能力（如规则、提示词、工具说明）注入到 OpenClaw Gateway 与 Agent 中。本仓库在 **demos/12_skill/** 下提供示例 **demo-skill**，便于理解 Skill 的结构与用法；若需被 OpenClaw 加载，需将 Skill 目录放到项目根下的 **skills/** 中。

---

## 核心概念

### 1. OpenClaw 与 Gateway

**是什么**：OpenClaw 是自托管的 AI Agent 网关，把常用聊天应用（如 WhatsApp、Telegram）与 AI 编程/对话 Agent 连接起来。Gateway 是核心进程，负责接收消息、调用 Agent、返回回复，并支持通过 Skill 扩展行为。

**为什么要有这个概念**：理解 Gateway 的角色，才能知道 Skill 是「挂」在哪一层、影响哪些行为；Gateway 是连接「用户入口」与「Agent 能力」的枢纽。

### 2. Skill（技能）

**是什么**：Skill 是 OpenClaw 中可插拔的能力单元，通常由一个目录及约定文件（如 **SKILL.md**）组成。SKILL.md 中描述该 Skill 的用途、触发条件、提供给 Agent 的说明或工具等，Gateway 或 Agent 在运行时加载这些 Skill，从而扩展行为或上下文。

**为什么要有这个概念**：不同用户、不同场景需要不同的规则或能力；通过 Skill 模块化扩展，可以在不改核心代码的前提下增加新能力、新提示或新工具描述，便于社区与生态共建。

### 3. SKILL.md 与规范

**是什么**：SKILL.md 是 Skill 的元数据与说明文件，通常包含：Skill 名称、描述、适用场景、以及给 Agent 的指引（如系统提示片段、工具列表说明）。具体格式与字段以 OpenClaw 官方文档为准；本仓库的 demo-skill 提供一种可用的示例结构。

**为什么要有这个概念**：统一的文件命名与结构让 Gateway 能自动发现、解析并加载 Skill；SKILL.md 是「人写、机器读」的契约，是 Skill 可复用的前提。

### 4. 与 LLM / Agent 的关系

**是什么**：Skill 中描述的能力（如「回答时优先引用某文档」「可用以下工具」）会被注入到 Agent 的上下文或配置中，影响 Agent 的 prompt、可用工具或决策逻辑。因此 Skill 本质上是「给 Agent 的扩展配置与说明」。

**为什么要有这个概念**：大模型应用学习路径中的其他主题（Prompt、Function Calling、Agent、RAG）是「如何做」；Skill 是「如何在 OpenClaw 里打包与注入这些能力」。理解这一点，便于把本仓库的 demo 能力迁移到 OpenClaw 生态。

### 5. 从 Demo 到生产：skills/ 目录

**是什么**：OpenClaw 通常从项目根目录下的 **skills/** 中加载 Skill。本仓库把示例放在 **demos/11_skill/demo-skill** 便于与其它 demo 一起管理；若要在真实 OpenClaw 中使用，需将 **demos/11_skill/demo-skill** 复制到项目根的 **skills/** 下（如 **skills/demo-skill**），并确保 SKILL.md 中的路径等配置与运行环境一致。

**为什么要有这个概念**：学习时在 demos 下统一管理，部署时按 OpenClaw 约定放到 skills/，避免混淆「示例」与「已启用 Skill」的位置。

---

## 本 Demo 做了什么

### 基础用例

- 无 Python 可执行脚本。通过阅读 **demos/12_skill/** 下的 README 与 **demo-skill/SKILL.md**，理解 Skill 的目录结构、SKILL.md 的 frontmatter 与说明正文，以及如何将自定义能力描述为「技能」供 Agent 或网关加载。学习站内本主题仅展示说明，不提供「运行 Demo」按钮。

### 进阶用例

- 仍无独立 runnable。在 README 或文档中了解如何编写带「触发条件」「工具列表」「系统提示片段」的 SKILL.md，或如何组织多个 Skill 目录、命名与版本约定。若需被某网关加载：将 **demos/12_skill/demo-skill** 复制到项目根的 **skills/demo-skill** 后使用。
