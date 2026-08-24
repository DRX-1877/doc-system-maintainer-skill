# 巡检脚本生成规格书 (Spec for audit_doc_health.py)

本文件是 **AI-Native Spec-Driven** 巡检脚本生成契约。在 `mode: init` 阶段，AI 必须读取本规格，并结合当前项目的具体语言（Java / Python / TypeScript / Go 等）、Web 框架与分层架构，**即时（JIT）生成量身定制的 `scripts/audit_doc_health.py` 巡检门禁脚本**。

---

## 🎯 1. 脚本目标与执行约束
- **目标**：以确定性（Deterministic）、零外部库依赖（仅标准库）的方式，在毫秒级内完成代码与文档体系的对齐度巡检。
- **环境约束**：纯 Python 3 标准库（`os`, `re`, `json`, `sys`, `argparse`），无需 `pip install` 额外包。
- **门禁机制**：支持 `--strict` 与 `--min-score <float>` 命令行参数。当未通过检查时，必须返回非零退出码（`sys.exit(1)`），以阻断 Git 提交与 CI 流水线。

---

## 📥 2. 项目逆向提取逻辑 (由 AI 根据目标项目定制实现)

### 2.1 API 路由提取器 (`find_endpoints`)
AI 需根据项目的 Web 框架逆向编写路由提取逻辑：
- **Spring Boot (Java/Kotlin)**：扫描 `@RestController`, `@RequestMapping`, `@GetMapping`, `@PostMapping`, `@PutMapping`, `@DeleteMapping`。
- **FastAPI / Flask / Django (Python)**：扫描 `@app.get`, `@router.post`, `path(...)` 或 `urls.py`。
- **NestJS / Express (TypeScript/JS)**：扫描 `@Controller`, `@Get`, `@Post` 或 `app.use('/api', ...)`。
- **Gin / Echo (Go)**：扫描 `r.GET(...)`, `r.POST(...)`。

### 2.2 核心领域模型提取器 (`find_domain_models`)
- 扫描领域层（如 `domain/`, `models/`, `entities/`）提取核心 Class / Record / Struct / Schema 名称。

### 2.3 Open-SWE 分层规则巡检 (`check_agents_hierarchy`)
- **根目录 `AGENTS.md`**：验证是否存在、行数是否 $\le 120$ 行、大小是否 $\le 64\text{ KB}$。
- **分层局部 `AGENTS.md`**：检测各关键子模块目录下是否存在局部规则文件，行数是否 $\le 60$ 行。

---

## 📤 3. 输出报表契约 (Standard JSON Output)

脚本在执行完毕后，必须向 `stdout` 输出结构化的 JSON 报表，格式如下：

```json
{
  "overall_health_score": "100.0%",
  "status": "HEALTHY | NEEDS_ATTENTION",
  "context_engineering_open_swe": {
    "root_agents_md": {
      "exists": true,
      "line_count": 88,
      "size_bytes": 5460,
      "lean_budget_ok": true
    },
    "directory_scoped_agents": {
      "app/.../domain/AGENTS.md": { "exists": true, "line_count": 25, "lean_budget_ok": true }
    }
  },
  "core_documents_check": {
    "AGENTS.md": true,
    "docs/architecture.md": true,
    "docs/domain-glossary.md": true,
    "docs/runbook.md": true
  },
  "api_spec_coverage": {
    "total_endpoints_found": 2,
    "documented_endpoints": 2,
    "missing_specs": [],
    "coverage_rate": "100.0%"
  },
  "domain_glossary_coverage": {
    "total_domain_classes": 11,
    "documented_classes": 11,
    "missing_in_glossary": [],
    "coverage_rate": "100.0%"
  }
}
```

---

## ⚡ 4. 退出码与错误拦截规则 (Exit Code Rules)
1. 若指定 `--strict`：
   - 存在任何 `missing_specs`（未写 Spec 的 API） $\rightarrow$ `sys.exit(1)`
   - 存在任何 `missing_in_glossary`（未登记的 Domain 实体） $\rightarrow$ `sys.exit(1)`
   - 核心文档（`AGENTS.md`, `architecture.md`, `domain-glossary.md`, `runbook.md`）缺失 $\rightarrow$ `sys.exit(1)`
2. 若 `overall_health_score < min_score`（默认 90.0%） $\rightarrow$ `sys.exit(1)`
3. 全部合规 $\rightarrow$ `sys.exit(0)`
