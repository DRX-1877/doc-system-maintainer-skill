# Business Models & Domain Glossary

This document defines the **Ubiquitous Language & Core Models** of the system. All code artifacts (classes, fields, database columns, API parameters) must strictly align with this glossary.

---

## 🌳 1. Model Structure & Package Topology

When bootstrapping or maintaining this file, the AI **scans model directories (e.g., `domain/`, `models/`, `entities/`, `types/`, `schemas/`) based on the project's actual architecture pattern** and generates a structured topology tree annotated with architectural roles:

```text
{{MODEL_DIRECTORY_TREE}}
```

---

## 📖 2. Data Models Dictionary

| Concept / Term | Class / Identifier | Architectural Role | Description & Invariants | File / Package Path |
| :--- | :--- | :--- | :--- | :--- |
| **{{TERM_1}}** | `{{NAME_1}}` | {{ROLE_1}} | {{DESCRIPTION_1}} | `{{PATH_1}}` |

---

## 🔄 3. Lifecycle & State Transitions

```mermaid
stateDiagram-v2
    [*] --> INITIAL_STATE
    INITIAL_STATE --> NEXT_STATE
    NEXT_STATE --> [*]
```
