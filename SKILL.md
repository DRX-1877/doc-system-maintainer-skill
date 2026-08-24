---
name: doc-system-maintainer
description: AI 编程核心文档体系管家。负责在项目中自适应识别架构、初始化、全生命周期维护并巡检 6 类核心文档（Root/Scoped/Test AI Rules, Specs, ADRs, Business Models & Glossary, Tasks, Runbook），保障 Open-SWE 规范注入与 ATDD 闭环。
---

# 文档体系生命周期管家指令 (doc-system-maintainer)

本技能用于为软件工程项目提供自适应架构感知、从零初始化、全生命周期演进与一致性巡检的 6 大核心文档体系支持，原生兼容 **Open-SWE / Deep Agents 级联规范注入标准**（支持业务分层与测试套件专属 `AGENTS.md` 隔离），并提供 **Spec-Driven 即时生成（JIT）的 CI/Pre-commit 物理硬门禁**。

---

## 💡 核心原则：AI 文档维护 4 大黄金法则

AI 在执行本技能的任何模式时，必须严格遵守以下 4 大黄金法则：

1. **“同 PR 原则 (Same PR Principle)”**：
   - 严禁代码已合入主干而文档还未更新。代码改动、测试用例与相关 Spec/ADR/Glossary 必须在同一个 Git Commit / PR 中同步交付。
2. **“业务与测试双轨级联 (Open-SWE Precedence Hierarchy)”**：
   - 全局规则置于根目录 `AGENTS.md`；
   - 业务分层规则下沉至各代码子目录 `AGENTS.md`（如 `domain/AGENTS.md`, `routers/AGENTS.md`）；
   - **测试套件专属规则下沉至各测试目录 `AGENTS.md`**（如 `src/test/AGENTS.md`, `src/contractTest/AGENTS.md`, `tests/AGENTS.md`），明确断言库、命名法与 Mock 隔离红线；
   - **裁决优先级**：`局部/测试子目录 AGENTS.md` > `根目录 AGENTS.md` > `docs/specs/*.md` > `LLM 默认习惯`。
3. **“Token 预算控制 (Keep Rules Lean)”**：
   - 根目录 `AGENTS.md` 控制在 **100 行** 内，局部/测试 `AGENTS.md` 控制在 **50 行** 内。只保留红线规则、命令清单和框架约束，详细的业务逻辑分流到 `docs/specs/` 中按需读取。
4. **“把文档当成 AI 的上下文缓存 (Docs as External Memory)”**：
   - 遇到复杂大任务时，主动在 `docs/tasks/` 记录细粒度子任务 Checklist。即使会话中断、切换分支或新建会话，新 AI 读此文档即可 100% 恢复上下文并断点续传。

---

## 🎯 模式 1：文档体系初始化 (`mode: init`)

当用户请求为项目初始化文档体系时，按以下顺序执行：

1. **逆向扫描项目特征、架构分层与测试套件**：
   - 读取构建文件（`build.gradle.kts` / `pom.xml` / `package.json` / `pyproject.toml` / `go.mod` 等），提取语言版本、核心框架、测试与打包命令。
   - 扫描源码与目录，识别架构风格（DDD 六边形、MVC 三层、FastAPI/SQLModel 数据驱动、Go 扁平包结构等）。
   - **扫描测试套件目录与类型**（如 `src/test/`, `src/integrationTest/`, `src/contractTest/`, `tests/` 等），识别测试框架（JUnit 5, pytest, Jest）与断言习惯（AssertJ, expect）。
2. **基于 templates/ 渲染并生成分层与测试文档**：
   - **根目录 `AGENTS.md`**：读取 `templates/agents.root.md.tpl` 生成全局技术栈、常用命令与全局红线。
   - **分层局部 `AGENTS.md`**：根据识别到的核心业务目录，读取 `templates/agents.scoped.md.tpl` 生成业务分层隔离规则。
   - **测试套件专属 `AGENTS.md`**：为识别到的测试套件目录，读取 `templates/agents.test.md.tpl` 生成专属断言与隔离规则。
   - **架构与决策**：`docs/architecture.md`（架构图与组件依赖流向）及 `docs/adr/0001-...`（基础架构决策）。
   - **业务模型与词汇表**：`docs/domain-glossary.md`（**自适应绘制项目核心模型所在目录的拓扑树**，提炼数据字典与状态机）。
   - **需求规格基线**：`docs/specs/`（现有核心功能的规格说明书）。
   - **运行排错手册**：`docs/runbook.md`（快速启动与自测脚本指南）。
3. **AI-Native 即时生成（JIT）专属巡检脚本与 CI 门禁**：
   - 读取 `templates/audit_script_spec.md` 契约规范。
   - 结合当前项目 Web 框架注解与模型目录特征，**JIT 编写生成专属的 `scripts/audit_doc_health.py`**（支持 `--strict` 门禁退出码）。
   - 为项目配置 Git Pre-commit（`.pre-commit-config.yaml`）与 CI 任务（如 Gradle `auditDocs` 任务 / GitHub Actions）。
4. **输出生成报告**：向用户展示生成的文档拓扑、架构风格与测试套件规范。

---

## 🚀 模式 2：需求生命周期驱动 (`mode: feature`)

当用户要求新增业务功能或修改业务逻辑时，**严禁直接写代码**，强制执行以下 5 步闭环：

### 步骤 0：上下文与级联规则对齐 (Context Resolution)
- 确定待修改的目标模块路径与测试目录，自动向上递归解析所有适用的祖先 `AGENTS.md`（含业务分层与测试专属规则）。

### 步骤 1：起草规格与领域对齐 (Spec-First)
- 读取 `templates/spec.md.tpl`，在 `docs/specs/` 下创建或更新 BDD 格式规格文件（包含 Given-When-Then 验收标准）。
- 在 `docs/domain-glossary.md` 中同步注册新实体/模型、字段与状态机流转。
- **🛑 必须暂停并向人类请求确认**（“Spec 已就绪，请确认业务规则与验收标准”）。

### 步骤 2：任务拆解与技术决策
- 人类确认后，读取 `templates/task.md.tpl` 在 `docs/tasks/` 创建细粒度子任务 Checklist。
- 如涉及重大技术选型变动，读取 `templates/adr.md.tpl` 在 `docs/adr/` 追加新记录。

### 步骤 3：ATDD 测试驱动与实现
- **编写测试**：严格遵循对应测试目录下 `AGENTS.md` 规范（断言库、命名法、禁止 Flaky sleep、三段式结构），编写契约与单元测试（Red 🔴）。
- **编写业务实现**：严格遵守业务目录下 `AGENTS.md` 分层约束，编写领域与应用逻辑（Green 🟢）。
- 运行项目的质量校验命令，确保测试、覆盖率门禁与代码格式全绿。

### 步骤 4：同步交付与自测
- 在 `docs/runbook.md` 中更新自测脚本，并在 `docs/tasks/` 中勾选完成项 `[x]`。
- 运行 `python3 scripts/audit_doc_health.py --strict` 确保物理门禁 100% 通过。

---

## 🔍 模式 3：一致性巡检与自愈 (`mode: audit`)

当用户要求检查文档健康度或提交代码前自检时：
1. 运行 `scripts/audit_doc_health.py --strict` 自动化扫描脚本。
2. 检查 Root、Scoped 业务与 Test `AGENTS.md` 是否完整，行数是否符合 Token 预算（Root $\le 100$, 局部 $\le 50$）。
3. 检查 API 路由是否与 `docs/specs/` 1:1 对应，核心模型是否在 `domain-glossary.md` 中登记。
4. 汇总差异点并主动为用户补充缺失或过期的文档部分。
