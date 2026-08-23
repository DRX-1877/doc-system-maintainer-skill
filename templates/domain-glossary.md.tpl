# 领域统一语言与数据字典 (Domain Glossary)

本文档定义系统的**通用语言（Ubiquitous Language）**。所有代码命名（类名、字段名、数据库列名、API 字段名）必须严格与本字典保持一致。

---

## 📖 1. 核心实体与值对象字典

| 领域术语 | 英文命名 | 类型 / 表现形式 | 业务含义与约束 | 代码对应类 |
| :--- | :--- | :--- | :--- | :--- |
| **{{TERM_1}}** | {{NAME_1}} | {{TYPE_1}} | {{DESCRIPTION_1}} | `{{CLASS_1}}` |

---

## 🔄 2. 状态机流转图 (Status Lifecycle)

```mermaid
stateDiagram-v2
    [*] --> INITIAL_STATE
    INITIAL_STATE --> NEXT_STATE
    NEXT_STATE --> [*]
```
