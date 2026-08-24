# Specification for audit_doc_health.py (JIT Generator Meta-Spec)

This file defines the **AI-Native Spec-Driven contract** for generating the doc health inspection script. In `mode: init`, the AI reads this specification, analyzes the target project's language (Java, Python, TypeScript, Go, etc.), web framework, and directory layout, and **Just-In-Time (JIT) generates a tailored `scripts/audit_doc_health.py` physical gate script**.

---

## 🎯 1. Objective & Operational Constraints
- **Objective**: Provide a deterministic, zero-external-dependency script to audit alignment between source code, specifications, and Open-SWE rule files in milliseconds.
- **Runtime Constraints**: Pure Python 3 Standard Library only (`os`, `re`, `json`, `sys`, `argparse`). No `pip install` required.
- **Gate Enforcement**: Must support `--strict` and `--min-score <float>` CLI flags. Return non-zero exit code (`sys.exit(1)`) on failure to block Git commits and CI pipelines.

---

## 📥 2. Project Reverse-Engineering Logic (Customized by AI per project)

### 2.1 API Endpoint Extractor (`find_endpoints`)
The AI writes regex/AST extractors tailored to the project's web framework:
- **Spring Boot (Java/Kotlin)**: Scan `@RestController`, `@RequestMapping`, `@GetMapping`, `@PostMapping`, `@PutMapping`, `@DeleteMapping`.
- **FastAPI / Flask / Django (Python)**: Scan `@app.get`, `@router.post`, `path(...)`, or `urls.py`.
- **NestJS / Express (TypeScript/JS)**: Scan `@Controller`, `@Get`, `@Post`, or `app.use('/api', ...)`.
- **Gin / Echo (Go)**: Scan `r.GET(...)`, `r.POST(...)`.

### 2.2 Core Business Model Extractor (`find_domain_models`)
- Scan business model directories (e.g., `domain/`, `models/`, `entities/`, `schemas/`) to extract Class, Record, Struct, or Model names.

### 2.3 Open-SWE Rule Hierarchy Audit (`check_agents_hierarchy`)
- **Root `AGENTS.md`**: Verify file existence, line count ($\le 120$ lines), and file size ($\le 64\text{ KB}$).
- **Scoped `AGENTS.md`**: Inspect critical subsystems and test suite directories for presence and Token Budget compliance ($\le 60$ lines each).

---

## 📤 3. Standard JSON Output Contract

Upon execution, the script must output a structured JSON report to `stdout`:

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
      "app/.../domain/AGENTS.md": { "exists": true, "line_count": 25, "lean_budget_ok": true },
      "app/.../test/AGENTS.md": { "exists": true, "line_count": 20, "lean_budget_ok": true }
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

## ⚡ 4. Exit Code & Blocking Rules
1. If `--strict` is enabled:
   - Any `missing_specs` (undocumented API endpoints) $\rightarrow$ `sys.exit(1)`
   - Any `missing_in_glossary` (unregistered models) $\rightarrow$ `sys.exit(1)`
   - Any missing core docs (`AGENTS.md`, `architecture.md`, `domain-glossary.md`, `runbook.md`) $\rightarrow$ `sys.exit(1)`
2. If `overall_health_score < min_score` (default 90.0%) $\rightarrow$ `sys.exit(1)`
3. All compliant $\rightarrow$ `sys.exit(0)`
