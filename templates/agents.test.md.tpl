# Test Suite & ATDD Rules ({{TEST_SUITE_TYPE}} AGENTS.md)

This file defines testing conventions and Double-Loop ATDD guidelines for the current test suite directory (`{{TEST_DIR_PATH}}`). Under the **Open-SWE Context Engineering Hierarchy**, these rules take **precedence over the root AGENTS.md** when writing or refactoring tests in this directory.

---

## 🎯 1. ATDD Role & Framework Conventions
- **ATDD Loop Role**: {{ATDD_LOOP_ROLE}} (e.g., [Outer Loop - Acceptance & Contract Testing] / [Inner Loop - Fast Unit TDD])
- **Test Type**: {{TEST_SUITE_TYPE}} (e.g., Unit Test / Contract Test / Integration Test / E2E Test)
- **Framework & Assertions**: {{TEST_FRAMEWORK_AND_ASSERTION}} (e.g., JUnit 5 + AssertJ, Spring Cloud Contract Groovy DSL, pytest)
- **Execution Command**: `{{TEST_CMD}}`
- **Naming Convention**: BDD-style naming `{{TEST_NAMING_CONVENTION}}` (e.g., `should_expectedBehavior_when_precondition()`)

---

## 🔄 2. Double-Loop ATDD Workflow
1. **Outer Loop (Acceptance & Contract)**: For contract/integration tests, tests MUST be written before implementation code, failing initially (Red 🔴), and trace 1:1 to Given-When-Then scenarios in `docs/specs/*.md`.
2. **Inner Loop (Unit & Domain Logic)**: For unit tests, write fast in-memory tests against Domain entities and Application services (Red 🔴) $\rightarrow$ write minimal production code (Green 🟢).
3. **Closing the Loop**: Once all inner loop unit tests pass, verify the outer acceptance test turns Green 🟢, then run formatting and coverage verification gates.

---

## 🚫 3. Testing Red Lines
1. **Three-Phase Structure**: Strictly follow `// Given`, `// When`, `// Then` (or AAA pattern) to structure test cases.
2. **No Flaky Sleep**: NEVER use `Thread.sleep()` or non-deterministic delays. Use explicit wait tools (e.g., `Awaitility`).
3. **Mocking & Isolation**: {{MOCKING_AND_ISOLATION_RULES}}
4. **Assertion Quality**: Never write empty tests without assertions. Ensure edge cases and validation failures are tested.

---

## 📋 4. Test Fixtures & Data Standards
- {{TEST_FIXTURE_RULES}}
