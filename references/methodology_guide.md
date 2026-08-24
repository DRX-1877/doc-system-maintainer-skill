# 架构自适应、ATDD 与 Open-SWE 规范注入方法论指南 (Methodology Guide)

---

## 🏛️ 1. 常见架构风格与分层映射 (Architecture Patterns)

AI 在接手项目时，必须自适应识别以下架构范式，严禁盲目套用术语：

| 架构范式 | 核心分层与包结构 | 核心模型定位 | 局部 AGENTS.md 建议目录 |
| :--- | :--- | :--- | :--- |
| **DDD 六边形架构** | `domain/` (核心), `application/` (用例), `adapter/web/`, `adapter/persistence/` | 聚合根 (Aggregate Root), 实体 (Entity), 值对象 (Value Object) | `domain/`, `adapter/web/`, `adapter/persistence/` |
| **传统 MVC / 三层架构** | `controller/` (控制层), `service/` (业务层), `dao/` 或 `repository/`, `entity/` | 数据实体 (Entity), DTO, VO | `controller/`, `service/`, `dao/` |
| **FastAPI / 数据驱动** | `routers/` (路由), `models/` (ORM模型), `schemas/` (Pydantic DTO), `services/` | 数据表模型 (ORM Table), 契约模型 (Pydantic Schema) | `routers/`, `models/` |
| **Go Clean / 模块化** | `cmd/`, `internal/domain/`, `internal/usecase/`, `internal/repository/` | 核心结构体 (Struct), 接口 (Interface) | `internal/domain/`, `internal/repository/` |

---

## 🔄 2. ATDD 双环开发法 (Acceptance Test-Driven Development)
- **外环（验收与契约）**：
  - 先根据 `docs/specs/*.md` 编写 API Contract Test 或 Integration Test，执行变红 🔴。
- **内环（领域与单元）**：
  - 编写核心业务单元测试与业务逻辑实现，单元测试变绿 🟢。
- **闭环与门禁**：
  - 外环验收测试变绿 🟢 ➔ 运行代码格式化 ➔ 覆盖率门禁与 `audit_doc_health.py --strict` 物理验证。

---

## 🧠 3. Open-SWE 级联规范注入机制 (Hierarchical Context Engineering)

### 3.1 规则优先级裁决顺序
1. **【最高优先级】** 目录级局部 `AGENTS.md`（如 `domain/AGENTS.md` 或 `service/AGENTS.md`）
2. **【次高优先级】** 项目根目录 `AGENTS.md`
3. **【业务优先级】** `docs/specs/*.md` 需求规格说明书
4. **【最低优先级】** AI 模型自身的通用偏好与默认习惯

### 3.2 Token 预算控制准则
- **根目录 `AGENTS.md`**：保持在 **100 行内**，只保留高频命令、环境版本和全局不可触碰红线。
- **分层局部 `AGENTS.md`**：保持在 **50 行内**，只描述当前分层的依赖方向和禁止引入的包/注解。
- **动态业务规则**：严禁写入 `AGENTS.md`，全部下沉至 `docs/specs/` 中按需加载。
