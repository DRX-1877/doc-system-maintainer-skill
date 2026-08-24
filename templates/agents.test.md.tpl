# 测试套件与 ATDD 协同准则 ({{TEST_SUITE_TYPE}} AGENTS.md)

本文件定义当前测试目录（`{{TEST_DIR_PATH}}`）下的测试编写与 ATDD 双环（Double-Loop ATDD）规范。根据 **Open-SWE 规范注入机制**，当 AI 在编写或修复本目录下的测试用例时，本规则自动生效并**优先于根目录 AGENTS.md**。

---

## 🎯 1. ATDD 双环定位与框架约定
- **ATDD 双环角色**：{{ATDD_LOOP_ROLE}} (如: 【外环验收驱动 - Outer Loop】 / 【内环单元驱动 - Inner Loop】)
- **测试类型**：{{TEST_SUITE_TYPE}} (如: 单元测试 / 契约测试 / 集成测试)
- **运行框架与断言库**：{{TEST_FRAMEWORK_AND_ASSERTION}} (如: JUnit 5 + AssertJ, Spring Cloud Contract Groovy DSL, pytest)
- **高频运行命令**：`{{TEST_CMD}}`
- **用例命名规范**：遵循 BDD 命名风格 `{{TEST_NAMING_CONVENTION}}` (如: `should_期望行为_when_前置条件()`)

---

## 🔄 2. ATDD 双环开发驱动流程
1. **外环驱动 (Outer Loop)**：若为契约/集成测试，必须先于业务代码编写，初始运行必须为 **Red 🔴**，且必须 1:1 溯源自 `docs/specs/*.md` 中的 Given-When-Then 场景。
2. **内环驱动 (Inner Loop)**：若为单元测试，针对 Domain 核心实体与 Application 用例，编写纯内存单测变红 (Red 🔴) $\rightarrow$ 编写最小业务实现变绿 (Green 🟢)。
3. **闭环验收 (Close the Loop)**：内环全部变绿后，驱动外环验收测试变绿 (Green 🟢)，并执行格式化与覆盖率门禁验证。

---

## 🚫 3. 不可违反的测试红线 (Testing Red Lines)
1. **三段式结构**：必须严格遵循 `// Given（前置条件）`, `// When（触发行为）`, `// Then（断言结果）` 组织测试代码。
2. **禁止 Flaky Test**：严禁使用 `Thread.sleep()` 等不确定性休眠，异步等待必须使用显式等待工具（如 `Awaitility`）。
3. **Mock 与隔离原则**：{{MOCKING_AND_ISOLATION_RULES}}
4. **覆盖率与断言质量**：禁止编写无断言的空测试，保证核心业务分支与异常路径覆盖。

---

## 📋 4. 专属测试数据与夹具规范
- {{TEST_FIXTURE_RULES}}
