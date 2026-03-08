---
name: demo-skill
description: 示例技能，用于 OpenClaw 学习与 Demo。当用户请求“介绍自己”或“demo”时，用简洁友好的方式回复并说明本技能已加载。
user-invocable: true
---

# Demo Skill

这是一个用于学习 OpenClaw 的示例 Agent Skill。当 Agent 加载本技能后，可以：

- 在用户说「介绍自己」「跑一下 demo」「用 demo skill」时，用一两句话介绍当前 Agent 并确认本技能已就绪。
- 作为模板，展示 `SKILL.md` 的 YAML frontmatter 和说明正文的写法。

## 使用方式

用户可直接在对话中说：

- “用 demo skill 打个招呼”
- “介绍下你自己 / 跑个 demo”

Agent 会结合系统提示与本技能说明，给出简短、友好的回复，并表明 demo-skill 已生效。

## 技术说明

- 本技能无需额外二进制或环境变量，仅依赖 OpenClaw 默认能力。
- 本仓库将 Skill 示例放在 **demos/11_skill/demo-skill/** 下便于学习。若需被 OpenClaw 加载，请将本目录复制到项目根的 **skills/demo-skill** 或 `~/.openclaw/skills/`。
