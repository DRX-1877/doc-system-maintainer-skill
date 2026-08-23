# 六边形架构与 ATDD 研发方法论参考 (Methodology Guide)

## 1. 六边形架构核心原则
- **领域独立性**：Domain 包必须是纯 Java，不能引入任何 Spring、JPA、Jackson。
- **端口与适配器**：
  - Inbound: Controller ➔ ApplicationService
  - Outbound: ApplicationService ➔ Port ➔ PersistenceAdapter ➔ Database

## 2. ATDD 双环开发法
- **外环**：先根据 Spec 写 Contract Test (Groovy) 或 Integration Test (MockMvc)，执行变红 🔴。
- **内环**：编写纯内存 Domain & Service 单元测试与实现，单元测试变绿 🟢。
- **闭环**：外环验收测试变绿 🟢 ➔ Spotless 格式化与覆盖率门禁验证。
