#!/usr/bin/env python3
"""
audit_doc_health.py
Deterministic health audit and physical gate script for Open-SWE hierarchical context engineering and ATDD alignment.
"""

import os
import re
import json
import sys
import argparse

def find_java_endpoints(workspace_root):
    endpoints = []
    web_dir = os.path.join(workspace_root, "app/src/main/java/com/example/demo/adapter/web")
    if not os.path.exists(web_dir):
        return endpoints

    for root, _, files in os.walk(web_dir):
        for file in files:
            if file.endswith("Controller.java"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    
                    # Extract class-level RequestMapping
                    class_mapping = ""
                    class_match = re.search(r'@RequestMapping\(["\'](.*?)["\']\)', content)
                    if class_match:
                        class_mapping = class_match.group(1)

                    # Extract PostMapping
                    for m in re.finditer(r'@PostMapping(?:\(["\'](.*?)["\']\))?', content):
                        path = m.group(1) or ""
                        full_path = f"{class_mapping}{path}".replace("//", "/")
                        endpoints.append({"method": "POST", "path": full_path, "controller": file})

                    # Extract GetMapping
                    for m in re.finditer(r'@GetMapping(?:\(["\'](.*?)["\']\))?', content):
                        path = m.group(1) or ""
                        full_path = f"{class_mapping}{path}".replace("//", "/")
                        endpoints.append({"method": "GET", "path": full_path, "controller": file})
    return endpoints

def find_domain_classes(workspace_root):
    domain_classes = []
    domain_dir = os.path.join(workspace_root, "app/src/main/java/com/example/demo/domain")
    if not os.path.exists(domain_dir):
        return domain_classes

    for root, _, files in os.walk(domain_dir):
        for file in files:
            if file.endswith(".java"):
                class_name = file.replace(".java", "")
                domain_classes.append(class_name)
    return domain_classes

def check_agents_hierarchy(workspace_root):
    """Audit Open-SWE hierarchical AGENTS.md files and token budgets."""
    root_agents = os.path.join(workspace_root, "AGENTS.md")
    root_exists = os.path.exists(root_agents)
    root_line_count = 0
    root_size_bytes = 0
    if root_exists:
        with open(root_agents, "r", encoding="utf-8") as f:
            lines = f.readlines()
            root_line_count = len(lines)
        root_size_bytes = os.path.getsize(root_agents)

    # Inspect scoped AGENTS.md candidates
    scoped_candidates = [
        "app/src/main/java/com/example/demo/domain/AGENTS.md",
        "app/src/main/java/com/example/demo/adapter/web/AGENTS.md",
        "app/src/main/java/com/example/demo/adapter/persistence/AGENTS.md",
        "app/src/test/AGENTS.md",
        "app/src/contractTest/AGENTS.md",
        "app/src/integrationTest/AGENTS.md",
    ]
    scoped_status = {}
    for rel_path in scoped_candidates:
        full_path = os.path.join(workspace_root, rel_path)
        exists = os.path.exists(full_path)
        line_count = 0
        if exists:
            with open(full_path, "r", encoding="utf-8") as f:
                line_count = len(f.readlines())
        scoped_status[rel_path] = {
            "exists": exists,
            "line_count": line_count,
            "lean_budget_ok": line_count <= 60 if exists else False
        }

    return {
        "root_agents_md": {
            "exists": root_exists,
            "line_count": root_line_count,
            "size_bytes": root_size_bytes,
            "lean_budget_ok": root_line_count <= 120 and root_size_bytes <= 64 * 1024
        },
        "directory_scoped_agents": scoped_status
    }

def check_core_docs(workspace_root):
    core_files = [
        "AGENTS.md",
        "docs/architecture.md",
        "docs/domain-glossary.md",
        "docs/runbook.md"
    ]
    status = {}
    for rel_path in core_files:
        full_path = os.path.join(workspace_root, rel_path)
        status[rel_path] = os.path.exists(full_path)
    return status

def check_specs(workspace_root, endpoints):
    specs_dir = os.path.join(workspace_root, "docs/specs")
    if not os.path.exists(specs_dir):
        return [], [f"{ep['method']} {ep['path']}" for ep in endpoints]

    spec_contents = ""
    for root, _, files in os.walk(specs_dir):
        for file in files:
            if file.endswith(".md"):
                with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                    spec_contents += f.read() + "\n"

    matched_endpoints = []
    missing_endpoints = []

    for ep in endpoints:
        # Match HTTP method and path
        path_pattern = ep["path"].replace("{", r"\{").replace("}", r"\}")
        pattern = rf"{ep['method']}.*?{path_pattern}"
        if re.search(pattern, spec_contents, re.IGNORECASE) or ep["path"] in spec_contents:
            matched_endpoints.append(f"{ep['method']} {ep['path']}")
        else:
            missing_endpoints.append(f"{ep['method']} {ep['path']} (Controller: {ep['controller']})")

    return matched_endpoints, missing_endpoints

def check_glossary(workspace_root, domain_classes):
    glossary_path = os.path.join(workspace_root, "docs/domain-glossary.md")
    if not os.path.exists(glossary_path):
        return [], domain_classes

    with open(glossary_path, "r", encoding="utf-8") as f:
        glossary_content = f.read()

    matched_classes = []
    missing_classes = []

    for cls in domain_classes:
        if cls in glossary_content:
            matched_classes.append(cls)
        else:
            missing_classes.append(cls)

    return matched_classes, missing_classes

def main():
    parser = argparse.ArgumentParser(description="Audit documentation alignment and health gates")
    parser.add_argument("--workspace", default=".", help="Root directory of the workspace")
    parser.add_argument("--strict", action="store_true", help="Enable strict gate mode (exit 1 on any misalignment)")
    parser.add_argument("--min-score", type=float, default=90.0, help="Minimum health score threshold (default: 90.0)")
    args = parser.parse_args()

    workspace_root = os.path.abspath(args.workspace)
    if not os.path.exists(workspace_root):
        workspace_root = os.getcwd()

    core_docs = check_core_docs(workspace_root)
    agents_hierarchy = check_agents_hierarchy(workspace_root)
    endpoints = find_java_endpoints(workspace_root)
    domain_classes = find_domain_classes(workspace_root)
    
    matched_specs, missing_specs = check_specs(workspace_root, endpoints)
    matched_classes, missing_classes = check_glossary(workspace_root, domain_classes)

    total_core = len(core_docs)
    existing_core = sum(1 for v in core_docs.values() if v)
    core_score = (existing_core / total_core) * 100

    api_coverage = (len(matched_specs) / len(endpoints) * 100) if endpoints else 100
    domain_coverage = (len(matched_classes) / len(domain_classes) * 100) if domain_classes else 100

    overall_health = round((core_score * 0.4 + api_coverage * 0.3 + domain_coverage * 0.3), 1)
    is_healthy = overall_health >= args.min_score

    report = {
        "overall_health_score": f"{overall_health}%",
        "status": "HEALTHY" if is_healthy else "NEEDS_ATTENTION",
        "context_engineering_open_swe": agents_hierarchy,
        "core_documents_check": core_docs,
        "api_spec_coverage": {
            "total_endpoints_found": len(endpoints),
            "documented_endpoints": len(matched_specs),
            "missing_specs": missing_specs,
            "coverage_rate": f"{round(api_coverage, 1)}%"
        },
        "domain_glossary_coverage": {
            "total_domain_classes": len(domain_classes),
            "documented_classes": len(matched_classes),
            "missing_in_glossary": missing_classes,
            "coverage_rate": f"{round(domain_coverage, 1)}%"
        }
    }

    print(json.dumps(report, indent=2, ensure_ascii=False))

    # Strict physical gate verification
    if args.strict:
        has_violations = bool(missing_specs or missing_classes or existing_core < total_core)
        if has_violations or not is_healthy:
            print("\n❌ [Doc Guard Intercepted] Code and documentation misalignment or missing core artifacts detected!", file=sys.stderr)
            if missing_specs:
                print(f"  - Missing API Specifications: {missing_specs}", file=sys.stderr)
            if missing_classes:
                print(f"  - Unregistered Domain Models in glossary: {missing_classes}", file=sys.stderr)
            if existing_core < total_core:
                missing_core = [k for k, v in core_docs.items() if not v]
                print(f"  - Missing Core Documents: {missing_core}", file=sys.stderr)
            sys.exit(1)

    if not is_healthy:
        sys.exit(1)

    sys.exit(0)

if __name__ == "__main__":
    main()
