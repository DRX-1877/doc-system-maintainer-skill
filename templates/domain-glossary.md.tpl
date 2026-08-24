# 领域统一语言与数据字典 (Domain Glossary)

本文档定义系统的**通用语言（Ubiquitous Language）**。所有代码命名（类名、字段名、数据库列名、API 字段名）必须严格与本字典保持一致。

---

## 🌳 1. 领域层分包与模型拓扑树 (Domain Package & Model Topology)

AI 在初始化或维护本文件时，**必须扫描 `domain/` 目录并绘制当前领域模型与子域拓扑树**，清晰标注各包的职责定位（如核心聚合根 vs 跨上下文弱引用）：

```text
{{DOMAIN_DIRECTORY_TREE}}
```

---

## 📖 2. 核心实体与值对象字典

| 领域术语 | 英文命名 | 类型 / 表现形式 | 业务含义与约束 | 代码对应类 |
| :--- | :--- | :--- | :--- | :--- |
| **{{TERM_1}}** | `{{NAME_1}}` | {{TYPE_1}} | {{DESCRIPTION_1}} | `{{CLASS_1}}` |

---

## 🔄 3. 状态机流转图 (Status Lifecycle)

```mermaid
stateDiagram-v2
    [*] --> INITIAL_STATE
    INITIAL_STATE --> NEXT_STATE
    NEXT_STATE --> [*]
```
