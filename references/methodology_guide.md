# 六边形架构、ATDD 与 Open-SWE 规范注入方法论指南 (Methodology Guide)

---

## 🏛️ 1. 六边形架构核心原则 (Hexagonal Architecture)
- **领域独立性**：Domain 包必须是纯 POJO/Record，严禁依赖任何 Spring、JPA、Jackson 或 Web 框架。
- **端口与适配器（依赖倒置）**：
  - **Inbound（入站）**：`Web Controller ➔ Inbound Port / ApplicationService`（数据通过 Request/Response DTO 隔离）。
  - **Outbound（出站）**：`ApplicationService ➔ Outbound Port ➔ PersistenceAdapter ➔ Database`（通过 Port 接口解耦）。
- **不可变性**：禁止使用 Lombok `@Setter` / `@Data`，保持实体与值对象的状态流转可预测。

---

## 🔄 2. ATDD 双环开发法 (Acceptance Test-Driven Development)
- **外环（验收与契约）**：
  - 先根据 `docs/specs/*.md` 编写 API Contract Test (Groovy) 或 Integration Test (MockMvc)，执行变红 🔴。
- **内环（领域与单元）**：
  - 编写纯内存 Domain & Application Service 单元测试与核心业务逻辑，单元测试变绿 🟢。
- **闭环与门禁**：
  - 外环验收测试变绿 🟢 ➔ 运行代码格式化（如 `spotlessApply`）➔ 覆盖率门禁验证（Jacoco $\ge$ 70%）。

---

## 🧠 3. Open-SWE 级联规范注入机制 (Hierarchical Context Engineering)

### 3.1 规则优先级裁决顺序
1. **【最高优先级】** 目录级局部 `AGENTS.md`（如 `domain/AGENTS.md`）
2. **【次高优先级】** 项目根目录 `AGENTS.md`
3. **【业务优先级】** `docs/specs/*.md` 需求规格说明书
4. **【最低优先级】** AI 模型自身的通用偏好与默认习惯

### 3.2 Token 预算控制准则
- **根目录 `AGENTS.md`**：保持在 **100 行内**，只保留高频命令、环境版本和全局不可触碰红线。
- **分层局部 `AGENTS.md`**：保持在 **50 行内**，只描述当前分层的依赖方向和禁止引入的包/注解。
- **动态业务规则**：严禁写入 `AGENTS.md`，全部下沉至 `docs/specs/` 中按需加载。
- **历史决策沉淀**：技术演进原因记录在 `docs/adr/` 中，保持主规则精炼。
