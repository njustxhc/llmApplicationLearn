# 大模型应用学习（llmApplicationLearn）

本仓库为 **大模型应用学习** 项目，提供 **core**（统一 LLM、文档 RAG）、**demos**（18 个主题 demo，含 Skill 示例、综合对话应用及流式/结构化/重试/截断等基础概念）、**learn_web**（学习站 Web）。

---

## 入口与使用

- **学习站 Web**：`python learn_web/app.py` → 打开 <http://127.0.0.1:5001/> ，按主题查看知识点并运行 Demo。
- **核心能力**：`core/llm`（统一 LLM 调用）、`core/rag_doc`（文档 RAG）。
- **各主题 Demo**：`python -m demos.01_api_chat.run` … `demos.18_context_truncate.run`；综合对话应用 `python -m demos.12_chat_app.app`（Web，端口 5000）。见 [demos/README.md](demos/README.md)。
- **学习路径文档**：[docs/大模型应用学习路径.md](docs/大模型应用学习路径.md)。
- **Skill 示例**：见 [demos/11_skill/](demos/11_skill/)，演示 `SKILL.md` 写法与目录结构。

### 环境配置（API Key、模型、超时）

大模型相关 demo 与 learn_web 需配置 API Key、模型 ID、超时等参数。两种方式任选其一：

1. **使用 .env 文件（推荐）**  
   在项目根目录复制示例并改名为 `.env`，按需填写：
   ```bash
   cp .env.example .env
   ```
   编辑 `.env`，至少填写 `ARK_API_KEY`；`ARK_MODEL_ID`、`ARK_TIMEOUT` 可选（有默认值）。  
   依赖已加入 `python-dotenv`，程序启动时会自动加载项目根目录下的 `.env`。

2. **使用系统环境变量**  
   不创建 `.env` 时，可直接设置环境变量：
   - `ARK_API_KEY`：必填，从所用大模型服务控制台获取  
   - `ARK_MODEL_ID`：可选，默认见 .env.example  
   - `ARK_TIMEOUT`：可选，默认 `120`（秒）

加载顺序：**.env 中的值** → **系统环境变量** → **默认值**。  
配置入口在 `core` 目录，由 `core/llm` 使用。

---

## 环境要求

- **Python 3.11+**
- 大模型调用需配置 API Key（见上方环境配置）

---

## 快速开始

1. **安装依赖**  
   ```bash
   pip install -r requirements.txt
   ```
   学习站单独依赖：`pip install -r learn_web/requirements.txt`（若仅跑 learn_web）。

2. **学习站（推荐）**  
   `python learn_web/app.py`，浏览器打开 <http://127.0.0.1:5001/> 按主题学习并运行 Demo。

3. **综合对话页**  
   `python -m demos.12_chat_app.app`，打开 <http://127.0.0.1:5000/> ，集成 RAG、MCP、联网搜索。

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
    └── 大模型应用学习路径.md
```
