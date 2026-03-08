# 大模型应用学习（llmApplicationLearn）

本仓库为 **大模型应用学习** 项目，提供 **core**（统一 LLM、文档 RAG）、**demos**（18 个主题 demo，含 Skill 示例、综合对话应用及流式/结构化/重试/截断等基础概念）、**learn_web**（学习站 Web）。同时保留 **OpenClaw** 与 Skills 相关说明，见下方「什么是 OpenClaw」。

---

## 大模型应用学习（入口）

- **学习站 Web**：`python learn_web/app.py` → 打开 <http://127.0.0.1:5001/> ，按主题查看知识点并运行 Demo。
- **核心能力**：`core/llm`（火山方舟）、`core/rag_doc`（文档 RAG）。
- **各主题 Demo**：`python -m demos.01_api_chat.run` … `demos.18_context_truncate.run`；综合对话应用 `python -m demos.12_chat_app.app`（Web，端口 5000）。见 [demos/README.md](demos/README.md)。
- **学习路径文档**：[docs/大模型应用学习路径.md](docs/大模型应用学习路径.md)。
- **Skill 示例**：见 [demos/11_skill/](demos/11_skill/)。若需被 OpenClaw 加载，可将 `demos/11_skill/demo-skill` 复制到 `skills/`。

### 环境配置（API Key、模型、超时）

大模型相关 demo 与 learn_web 使用 **火山方舟（Ark）**，需配置 API Key 等参数。两种方式任选其一：

1. **使用 .env 文件（推荐）**  
   在项目根目录复制示例并改名为 `.env`，按需填写：
   ```bash
   cp .env.example .env
   ```
   编辑 `.env`，至少填写 `ARK_API_KEY`；`ARK_MODEL_ID`、`ARK_TIMEOUT` 可选（有默认值）。  
   依赖已加入 `python-dotenv`，程序启动时会自动加载项目根目录下的 `.env`。

2. **使用系统环境变量**  
   不创建 `.env` 时，可直接设置环境变量：
   - `ARK_API_KEY`：必填，火山方舟控制台获取  
   - `ARK_MODEL_ID`：可选，默认 `deepseek-v3-2-251201`  
   - `ARK_TIMEOUT`：可选，默认 `120`（秒）

加载顺序：**.env 中的值** → **系统环境变量** → **默认值**。  
配置入口代码：`core/volcengine_config.py`，由 `core/llm` 使用。

---

## 什么是 OpenClaw？

**OpenClaw** 是一个**自托管**的 AI Agent 网关，把你的常用聊天应用（WhatsApp、Telegram、Discord、iMessage 等）和 AI 编程/对话 Agent 连在一起。你只需在本地或服务器上跑一个 **Gateway** 进程，就能在手机上发消息、从口袋里获得 Agent 的回复。

### 核心特点

- **开源**：MIT 协议，社区驱动
- **Agent 原生**：为带工具调用、会话、记忆、多 Agent 路由的编程 Agent 设计
- **多通道**：一个 Gateway 同时服务 WhatsApp、Telegram、Discord 等
- **自托管**：跑在你自己的机器上，数据由你掌控

### 架构示意

```
聊天应用 + 插件  →  Gateway  →  Pi Agent / 其他 Agent
                    ↓
                CLI、Web Control UI、macOS/iOS/Android 节点
```

Gateway 是会话、路由和通道连接的单一事实来源。

---

## 核心概念

### 1. Gateway（网关）

- 默认端口：**18789**
- 控制台 UI：<http://127.0.0.1:18789/>
- 配置目录：`~/.openclaw/openclaw.json`

### 2. Agent（智能体）

- 每个 Agent 有 `agent_id` 和可选的 `session_name`（默认 `"main"`）
- 会话键格式：`agent:{agent_id}:{session_name}`，用于隔离对话历史

### 3. Skills（技能）

Agent 的能力由 **Skills** 扩展。每个 Skill 是一个目录，包含：

- **SKILL.md**：YAML frontmatter + 使用说明（兼容 [AgentSkills](https://agentskills.io/) 规范）
- 可选：脚本、配置、数据文件

**Skill 加载顺序（优先级从高到低）：**

1. 工作区技能：`/skills`（当前项目下的 `skills/`）
2. 本地托管：`~/.openclaw/skills`
3. 内置技能：随安装包一起提供

**ClawHub**（[clawhub.ai](https://clawhub.ai/)）是官方技能市场，可以搜索、安装、更新技能：

```bash
npm i -g clawhub
clawhub search "日历"
clawhub install <skill-slug>
```

---

## 环境要求

- **Node.js 22+**
- **OpenClaw Gateway** 已安装并运行（供 SDK 连接）
- **Python 3.11+**（仅 Demo 脚本需要）

---

## 快速开始

### 1. 安装 OpenClaw

**注意**：安装前需已安装 **Git**（[下载 Git for Windows](https://git-scm.com/download/win)），否则 npm 会报错 `spawn git`。  
详细步骤见 **[INSTALL_OPENCLAW.md](INSTALL_OPENCLAW.md)**。

```bash
npm install -g openclaw@latest
openclaw onboard --install-daemon
```

### 2. 配对通道并启动 Gateway

```bash
openclaw channels login
openclaw gateway --port 18789
```

### 3. 本仓库与 OpenClaw

- **Skill 示例**：见 **`demos/11_skill/demo-skill/`**，演示 `SKILL.md` 写法。若需被 OpenClaw 加载，请将 `demos/11_skill/demo-skill` 复制到项目根下新建的 **`skills/demo-skill`**，或在项目根启动 Gateway 前复制到 `~/.openclaw/skills/`。

### 4. 大模型学习站与对话页

- **学习站**（推荐）：`pip install -r learn_web/requirements.txt` 后 `python learn_web/app.py`，浏览器打开 <http://127.0.0.1:5001/> 按主题学习并运行 Demo。
- **综合对话页**：`python -m demos.12_chat_app.app`，打开 <http://127.0.0.1:5000/> ，集成 RAG、MCP、联网搜索。

---

## 项目结构

```
llmApplicationLearn/
├── README.md
├── requirements.txt
├── core/                 # 大模型应用核心：统一 LLM、文档 RAG
│   ├── llm/
│   └── rag_doc/
├── demos/                # 主题 demo（01_api_chat … 18_context_truncate、11_skill、12_chat_app）
├── learn_web/            # 学习站 Web（知识点 + 运行 Demo），端口 5001
└── docs/
    ├── 大模型应用学习路径.md
    └── 项目重组与学习站规划.md
```

---

## 参考链接

- 官方文档：<https://docs.openclaw.ai/>
- 技能说明：<https://docs.openclaw.ai/skills>
- ClawHub：<https://docs.openclaw.ai/tools/clawhub>
- Python SDK：<https://masteryodaa.github.io/openclaw-sdk/>
