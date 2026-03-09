# 04 MCP 工具调用

本讲介绍 **MCP（Model Context Protocol）**：一种让大模型与外部工具、数据源对接的开放协议。工具以「Server」形式暴露（如查天气、查库），客户端通过标准方式发现工具并调用，从而扩展模型能力。本 Demo 提供一个基于 MCP 的天气查询 Server（内部调用 wttr.in），并可通过 Cursor / MCP Inspector 连接。

---

## 核心概念

### 1. MCP（Model Context Protocol）

**是什么**：MCP 是一套开放协议，用于定义「工具/数据服务」（Server）与「使用这些服务的客户端」（Client）之间的通信方式。Server 暴露能力（如工具列表、执行接口），Client 通过协议发现并调用，再把结果交给大模型或用户。

**为什么要有这个概念**：大模型本身不会查天气、查数据库；能力需要由外部系统提供。若每家都自定义一套「工具协议」，客户端难以复用。MCP 提供统一约定（如 list_tools、call_tool、资源读取），便于工具生态与各类客户端（IDE、Agent、应用）对接。

### 2. 工具（Tools）与 list_tools / call_tool

**是什么**：在 MCP 中，**工具** 由 Server 声明（名称、描述、参数 schema）。Client 通过 **list_tools** 获取工具列表，通过 **call_tool** 传入工具名与参数并拿到执行结果。结果可再交回给大模型，用于下一轮推理或回复。

**为什么要有这个概念**：模型需要「知道能调用什么、怎么传参」；应用需要「按名调用、拿到结构化结果」。list_tools 解决「发现」，call_tool 解决「执行」，二者是工具调用的最小闭环。

### 3. 传输方式（Transport）：stdio / HTTP 等

**是什么**：MCP 的 Client 与 Server 之间可以通过不同方式通信，常见有 **stdio**（标准输入/输出，同进程或子进程管道）、**HTTP/SSE**（网络服务）。本 Demo 使用 stdio：Server 以子进程形式启动，Client 通过 stdin/stdout 收发 JSON-RPC 消息。

**为什么要有这个概念**：本地 IDE、Agent 常以子进程方式拉起工具服务，无需开端口；而云上或远程工具可能用 HTTP。协议与传输解耦，同一套「list_tools / call_tool」语义可在不同传输上实现。

### 4. 客户端与 Server 的分工

**是什么**：**Server** 只负责声明工具、执行工具、返回结果；**Client** 负责发起 list_tools、根据用户意图或模型输出选择工具与参数、调用 call_tool，并把结果整合进对话或再交给模型。

**为什么要有这个概念**：工具实现与「谁在何时调用」分离：同一套天气 Server 可被 Cursor、被自家 Agent、被 MCP Inspector 共用；客户端负责编排（何时查天气、何时查库），Server 只做「能力提供」。

---

## 本 Demo 做了什么

### 基础用例

- 启动一个 MCP Server（`demos.04_mcp.server`），暴露单一工具 **get_weather**，内部请求 wttr.in 获取天气。
- 通过 **list_tools_client** 或等价方式列出工具、再对单个工具发起 call_tool，将返回结果打印。演示 MCP 的 list_tools / call_tool 协议与「工具描述 → 调用 → 结果」的闭环。
- 学习站内「运行基础 Demo」会提示：本 Demo 为 Server 端，请单独运行 `python -m demos.04_mcp.server`。实际调用可在终端运行 `python -m demos.04_mcp.list_tools_client` 或通过 Cursor/Inspector 体验。

### 进阶用例

- 运行 **run_advanced**：调用 list_tools_client 列出 MCP Server 的工具列表（需先另启 Server）。演示客户端发现工具的过程；若 Server 暴露多工具，可进一步演示按意图选工具并传参。
- 运行：点击「运行进阶 Demo」或执行 `python -m demos.04_mcp.run_advanced`（需先启动 Server）。
