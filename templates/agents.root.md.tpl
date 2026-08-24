# Global AI Coding Rules (AGENTS.md)

This file serves as the **global baseline and non-negotiable constraints** for AI coding assistants (e.g., Antigravity, Open-SWE, Cursor, Claude Code) working on this codebase.

---

## ⚖️ Precedence Hierarchy
In case of conflicting rules, AI agents MUST resolve precedence in the following strict order:
1. **[Highest Precedence]** `AGENTS.md` located in the current working subdirectory or nearest ancestor directory (Scoped rules).
2. **[Second Precedence]** This file (Root `AGENTS.md` containing global architectural red lines and commands).
3. **[Business Precedence]** `docs/specs/*.md` feature specification documents.
4. **[Lowest Precedence]** The LLM's own general defaults and statistical biases.

---

## 🛠️ 1. Tech Stack & Runtime Environment
- **Language**: {{LANGUAGE_AND_VERSION}}
- **Framework**: {{FRAMEWORK_AND_VERSION}}
- **Build Tool**: {{BUILD_TOOL}}
- **Database / Middleware**: {{DATABASE_AND_MIDDLEWARE}}

---

## ⚡ 2. Common Developer Commands (Must be copy-pasteable)
| Action | Command | Description |
| :--- | :--- | :--- |
| **Full Quality Check** | `{{CMD_CHECK}}` | Run all tests, coverage gates, and linter/format checks |
| **Unit Tests** | `{{CMD_UNIT_TEST}}` | Fast in-memory unit tests execution |
| **Format Code** | `{{CMD_FORMAT}}` | Auto-format codebase |
| **Run Locally** | `{{CMD_RUN}}` | Start local development server |

---

## 🏛️ 3. Architectural Red Lines
{{ARCHITECTURE_RED_LINES}}

---

## 📋 4. Coding & Delivery Standards
1. **Immutability**: {{IMMUTABILITY_RULES}}
2. **Error Handling**: Adhere to standard error structures (e.g., RFC 7807 `ProblemDetail`), handled via global exception interceptors.
3. **Double-Loop ATDD**: New features MUST define BDD acceptance criteria in `docs/specs/` and write failing tests (Red 🔴) before implementation (Green 🟢).
4. **Token Budget Control**: Keep this file lean (< 100 lines). Detailed business specifications belong in `docs/specs/`.
