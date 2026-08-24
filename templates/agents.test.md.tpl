# 测试套件 AI 协同准则 ({{TEST_SUITE_TYPE}} AGENTS.md)

本文件定义当前测试目录（`{{TEST_DIR_PATH}}`）下的测试编写与断言规范。根据 **Open-SWE 规范注入机制**，当 AI 在编写或修复本目录下的测试用例时，本规则自动生效并**优先于根目录 AGENTS.md**。

---

## 🎯 1. 测试定位与框架约定
- **测试类型**：{{TEST_SUITE_TYPE}} (如: 单元测试 / 契约测试 / 集成测试 / 端到端测试)
- **运行框架与断言库**：{{TEST_FRAMEWORK_AND_ASSERTION}} (如: JUnit 5 + AssertJ, pytest, Jest, Vitest)
- **高频运行命令**：`{{TEST_CMD}}`
- **用例命名规范**：遵循 BDD 命名风格 `{{TEST_NAMING_CONVENTION}}` (如: `should_期望行为_when_前置条件()`)

---

## 🚫 2. 不可违反的测试红线 (Testing Red Lines)
1. **三段式结构**：必须严格遵循 `// Given`, `// When`, `// Then`（或 AAA 模式）组织测试代码。
2. **禁止 Flaky Test**：严禁使用 `Thread.sleep()` 等不确定性休眠，异步等待必须使用显式等待工具（如 `Awaitility`）。
3. **Mock 与隔离原则**：{{MOCKING_AND_ISOLATION_RULES}}
4. **覆盖率与断言质量**：禁止编写无断言的空测试，保证核心业务分支覆盖。

---

## 📋 3. 专属测试数据与夹具规范
- {{TEST_FIXTURE_RULES}}
