# 核心业务模型与统一语言字典 (Business Models & Domain Glossary)

本文档定义系统的**通用语言与核心数据模型（Ubiquitous Language & Core Models）**。所有代码命名（类名、字段名、数据库列名、API 字段名）必须严格与本字典保持一致。

---

## 🌳 1. 核心业务模型分包与拓扑树 (Model Structure & Topology)

AI 在初始化或维护本文件时，**需根据项目实际架构风格（如 DDD、传统 MVC、FastAPI 数据驱动、Go Clean Arch 等）**，扫描业务模型所在目录（如 `domain/`、`models/`、`entity/`、`types/`、`schemas/`），绘制反映该项目真实形态的分包与模型拓扑树，并标注其架构角色：

```text
{{MODEL_DIRECTORY_TREE}}
```

---

## 📖 2. 核心概念与数据模型字典 (Data Models Dictionary)

| 业务概念 / 术语 | 英文标识 / 类名 | 架构角色 / 类型 | 业务含义与约束 | 代码所在文件 / 路径 |
| :--- | :--- | :--- | :--- | :--- |
| **{{TERM_1}}** | `{{NAME_1}}` | {{ROLE_1}} | {{DESCRIPTION_1}} | `{{PATH_1}}` |

---

## 🔄 3. 业务生命周期与状态流转图 (Status Lifecycle)

```mermaid
stateDiagram-v2
    [*] --> INITIAL_STATE
    INITIAL_STATE --> NEXT_STATE
    NEXT_STATE --> [*]
```
