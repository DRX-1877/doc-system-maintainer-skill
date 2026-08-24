---
name: doc-system-maintainer
description: AI coding documentation lifecycle manager. Reverse-engineers project architecture, bootstraps and maintains 6 core documentation artifacts (Root/Scoped/Test AI Rules, Specs, ADRs, Business Models & Glossary, Tasks, Runbook), enforcing Open-SWE context engineering and ATDD closed-loop workflows.
---

# Documentation System Lifecycle Manager (doc-system-maintainer)

This skill provides adaptive architecture-aware, zero-to-one bootstrapping, full-lifecycle evolution, and consistency auditing across 6 core documentation artifacts for software engineering projects. It is natively compatible with **Open-SWE / Deep Agents hierarchical context injection standards** (supporting business layer and test suite `AGENTS.md` isolation) and provides **Spec-Driven Just-In-Time (JIT) generated CI/Pre-commit physical guardrails**.

---

## 💡 Core Philosophy: The 4 Golden Laws of AI Documentation

AI agents executing any mode of this skill MUST strictly adhere to the following 4 Golden Laws:

1. **"Same PR Principle"**:
   - Code must NEVER be merged into the main branch with outdated documentation. Code changes, test suites, and associated Specs/ADRs/Glossary must be delivered together in the same Git Commit / PR.
2. **"Dual-Track Hierarchical Context Engineering (Open-SWE Precedence Hierarchy)"**:
   - Global rules reside in the root `AGENTS.md`.
   - Business layer rules are pushed down to subsystem `AGENTS.md` files (e.g., `domain/AGENTS.md`, `routers/AGENTS.md`).
   - **Test suite-specific rules reside in test directories** (e.g., `src/test/AGENTS.md`, `src/contractTest/AGENTS.md`, `tests/AGENTS.md`), defining assertion libraries, naming conventions, and mock isolation red lines.
   - **Precedence Hierarchy**: `Scoped/Test AGENTS.md` > `Root AGENTS.md` > `docs/specs/*.md` > `Default LLM Biases`.
3. **"Token Budget Control (Keep Rules Lean)"**:
   - Root `AGENTS.md` must stay within **100 lines**; scoped/test `AGENTS.md` must stay within **50 lines**. Keep only hard red lines, commands, and structural constraints. Detailed business logic must be deferred to `docs/specs/` and loaded on demand.
4. **"Docs as External Memory"**:
   - For complex tasks, actively record fine-grained subtask checklists in `docs/tasks/`. When a session interrupts, branches switch, or a new agent takes over, reading these docs restores 100% context for seamless continuation.

---

## 🎯 Mode 1: Documentation Bootstrapping (`mode: init`)

When requested to initialize or bootstrap documentation for a project, execute in this exact sequence:

1. **Reverse-engineer project features, architecture patterns, and test suites**:
   - Read build manifests (`build.gradle.kts`, `pom.xml`, `package.json`, `pyproject.toml`, `go.mod`, etc.) to extract runtime versions, core frameworks, test, and build commands.
   - Inspect directory layouts and source code to identify the actual architecture pattern (e.g., DDD Hexagonal, traditional MVC 3-tier, FastAPI/SQLModel schema-driven, Go clean architecture).
   - **Scan test suite directories and types** (`src/test/`, `src/integrationTest/`, `src/contractTest/`, `tests/`, etc.), detecting test frameworks (JUnit 5, pytest, Jest) and assertion styles (AssertJ, expect, pytest assert).
2. **Render and generate hierarchical documentation from templates**:
   - **Root `AGENTS.md`**: Render from `templates/agents.root.md.tpl` for global tech stack, copy-paste commands, and global red lines.
   - **Scoped Business `AGENTS.md`**: Render from `templates/agents.scoped.md.tpl` for key architectural layers (e.g., domain, web, persistence).
   - **Scoped Test `AGENTS.md`**: Render from `templates/agents.test.md.tpl` for detected test suites with ATDD roles and assertion rules.
   - **Architecture & ADRs**: Generate `docs/architecture.md` (topology & dependency flow) and `docs/adr/0001-...` (foundational decisions).
   - **Business Models & Glossary**: Generate `docs/domain-glossary.md` (**adaptively rendering the model package topology tree**, data dictionary, and state machine).
   - **Specification Baseline**: Generate `docs/specs/` (BDD specifications for existing core endpoints).
   - **Runbook**: Generate `docs/runbook.md` (quick start, live curl examples, and troubleshooting FAQ).
3. **AI-Native Just-In-Time (JIT) Audit Script & CI Gate Generation**:
   - Read `templates/audit_script_spec.md`.
   - Based on the project's web framework annotations and model layout, **JIT-generate a zero-dependency `scripts/audit_doc_health.py`** (supporting `--strict` non-zero exit codes).
   - Configure Git Pre-commit (`.pre-commit-config.yaml`) and CI workflows (e.g., Gradle `auditDocs` task / GitHub Actions).
4. **Output Initialization Report**: Present the generated documentation topology, architecture classification, and physical gate status to the user.

---

## 🚀 Mode 2: Feature Lifecycle & ATDD Closed Loop (`mode: feature`)

When developing a new feature or modifying existing business logic, **NEVER jump straight into writing implementation code**. Enforce the 5-step ATDD closed loop:

### Step 0: Context Resolution & Cascading Rules
- Identify target module and test directories. Recursively resolve all applicable ancestor `AGENTS.md` files (including business and test-scoped rules).

### Step 1: Spec-First & Domain Alignment
- Render from `templates/spec.md.tpl` to create/update BDD specifications in `docs/specs/` (Given-When-Then acceptance criteria).
- Register new models, fields, and state transitions in `docs/domain-glossary.md`.
- **🛑 STOP & REQUEST USER CONFIRMATION** ("Spec is ready. Please review and confirm the acceptance criteria.").

### Step 2: Task Breakdown & Technical Decisions
- Upon user approval, render from `templates/task.md.tpl` to create a checklist in `docs/tasks/`.
- If major architectural choices change, record an ADR in `docs/adr/`.

### Step 3: Double-Loop ATDD Implementation
- **Outer Loop (Acceptance & Contract Tests)**: Write contract or integration tests matching the Spec in the corresponding test suite (Red 🔴).
- **Inner Loop (Unit Tests & Domain Logic)**: Following `src/test/AGENTS.md`, write pure in-memory unit tests (Red 🔴) $\rightarrow$ write domain & application logic (Green 🟢).
- Run project quality checks to ensure unit, integration, contract tests, and code formatting pass 100%.

### Step 4: Verification & Synchronized Delivery
- Update manual verification scripts in `docs/runbook.md` and mark checklist items `[x]` in `docs/tasks/`.
- Run `python3 scripts/audit_doc_health.py --strict` to verify 100% compliance.

---

## 🔍 Mode 3: Consistency Audit & Self-Healing (`mode: audit`)

When auditing documentation health or executing pre-commit verification:
1. Run `python3 scripts/audit_doc_health.py --strict`.
2. Verify Root, Scoped, and Test `AGENTS.md` presence and Token Budgets (Root $\le 100$ lines, Scoped $\le 50$ lines).
3. Ensure all API endpoints match 1:1 with `docs/specs/` and all models are registered in `docs/domain-glossary.md`.
4. Summarize discrepancies and proactively self-heal missing or outdated sections.
