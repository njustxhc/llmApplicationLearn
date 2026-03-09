# 11 OpenClaw Skill 学习与示例

本 demo 存放 **OpenClaw Skill** 的学习说明与示例，与「大模型应用」并列一条学习线。

## 内容

- **demo-skill/**：示例 Skill，包含 `SKILL.md`（YAML frontmatter + 使用说明）。可作为模板学习 Skill 的写法与加载方式。

## OpenClaw 加载方式

OpenClaw 默认从工作区 **`skills/`** 目录加载技能。若希望使用本目录下的示例：

1. 将 **`demos/11_skill/demo-skill`** 复制到项目根目录下的 **`skills/demo-skill`**；或  
2. 在 OpenClaw 配置中指定从 `demos/11_skill` 加载（若支持自定义路径）。

## 参考

- 项目根目录 **README.md** 中的 OpenClaw 与 Skills 介绍  
- [AgentSkills 规范](https://agentskills.io/)（SKILL.md 格式）
