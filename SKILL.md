---
name: doc-system-maintainer
description: AI 编程核心文档体系管家。负责在项目中初始化、全生命周期维护并巡检 6 类核心文档（AI Rules, Specs, ADRs, Domain Glossary, Implementation Tasks, Runbook），保障 Spec-Driven 与 ATDD 闭环。
---

# 文档体系生命周期管家指令 (doc-system-maintainer)

本技能用于为软件工程项目提供从零初始化、全生命周期演进与一致性巡检的 6 大核心文档体系支持。

---

## 🎯 模式 1：文档体系初始化 (`mode: init`)

当用户请求为项目初始化文档体系时，按以下顺序执行：
1. **逆向扫描项目**：
   - 读取构建文件（`build.gradle.kts` / `pom.xml` / `package.json`），提取语言版本、核心依赖、测试与打包命令。
   - 扫描包结构，识别分层架构风格（如六边形架构、DDD、传统 MVC）。
2. **基于 templates/ 渲染并生成 6 大基础文档**：
   - 根目录生成 `AGENTS.md`（技术栈、高频命令、架构红线）。
   - `docs/architecture.md`（架构图与依赖流向）及 `docs/adr/0001-...`（基础架构决策）。
   - `docs/domain-glossary.md`（扫描实体提炼词汇表）。
   - `docs/specs/`（现有核心功能的规格说明书）。
   - `docs/runbook.md`（快速启动与自测脚本指南）。
3. **输出生成报告**：向用户展示生成的文档拓扑与后续开发指引。

---

## 🚀 模式 2：需求生命周期驱动 (`mode: feature`)

当用户要求新增业务功能或修改业务逻辑时，**严禁直接写代码**，强制执行以下 4 步 ATDD 闭环：

### 步骤 1：起草规格与领域对齐 (Spec-First)
- 读取 `templates/spec.md.tpl`，在 `docs/specs/` 下创建或更新 BDD 格式规格文件（包含 Given-When-Then 验收标准）。
- 在 `docs/domain-glossary.md` 中同步注册新实体、字段与状态机流转。
- **🛑 必须暂停并向人类请求确认**（“Spec 已就绪，请确认业务规则与验收标准”）。

### 步骤 2：任务拆解与技术决策
- 人类确认后，读取 `templates/task.md.tpl` 在 `docs/tasks/` 创建细粒度子任务 Checklist。
- 如涉及重大技术选型变动，读取 `templates/adr.md.tpl` 在 `docs/adr/` 追加新记录。

### 步骤 3：ATDD 测试驱动与实现
- 先根据 Spec 编写 API 契约测试与应用层单元测试（Red 🔴）。
- 编写领域模型与服务实现，确保架构依赖不违规（Green 🟢）。
- 运行项目的质量校验命令（如 `./gradlew check`），确保测试与代码格式全绿。

### 步骤 4：同步交付与自测
- 在 `http/` 补充端到端测试脚本，并在 `docs/runbook.md` 中更新。
- 在 `docs/tasks/` 中勾选完成项 `[x]`。

---

## 🔍 模式 3：一致性巡检与自愈 (`mode: audit`)

当用户要求检查文档健康度或提交代码前自检时：
1. 运行 `scripts/audit_doc_health.py` 自动化扫描脚本。
2. 检查 Controller API 是否与 `docs/specs/` 1:1 对应。
3. 检查代码中的 Entity / Enum 是否在 `domain-glossary.md` 中登记。
4. 汇总差异点并主动为用户补充缺失的文档部分。
