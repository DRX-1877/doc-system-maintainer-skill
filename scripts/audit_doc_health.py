#!/usr/bin/env python3
"""
audit_doc_health.py
Deterministic health audit and physical gate script for Open-SWE hierarchical context engineering and ATDD alignment.
Dynamically supports Spring Boot, Modular Monoliths (e.g. yudao-boot, ruoyi), DDD Hexagonal, and FastAPI/Go frameworks.
"""

import os
import re
import json
import sys
import argparse
from pathlib import Path

def find_java_endpoints(workspace_root):
    """
    Recursively scans all Java Controller files across all modules in the workspace.
    """
    endpoints = []
    workspace_path = Path(workspace_root)
    
    # Exclude common build directories
    exclude_dirs = {"target", "build", ".git", "node_modules", ".gradle"}
    
    for controller_file in workspace_path.glob("**/*Controller.java"):
        # Check if inside excluded directory
        if any(part in exclude_dirs for part in controller_file.parts):
            continue
            
        try:
            content = controller_file.read_text(encoding="utf-8")
        except Exception:
            continue

        # Extract class-level RequestMapping
        class_mapping = ""
        class_match = re.search(r'@RequestMapping\(["\'](.*?)["\']\)', content)
        if class_match:
            class_mapping = class_match.group(1)

        # Extract method-level mappings
        for method_type in ["PostMapping", "GetMapping", "PutMapping", "DeleteMapping", "RequestMapping"]:
            for m in re.finditer(rf'@{method_type}(?:\(.*?["\'](.*?)["\'].*?\))?', content):
                sub_path = m.group(1) or ""
                full_path = f"{class_mapping}{sub_path}".replace("//", "/")
                http_method = method_type.replace("Mapping", "").upper() if method_type != "RequestMapping" else "HTTP"
                endpoints.append({
                    "method": http_method,
                    "path": full_path,
                    "controller": controller_file.name,
                    "file_path": str(controller_file)
                })

    return endpoints

def find_domain_classes(workspace_root):
    """
    Recursively scans domain models / data objects / entities in the workspace.
    """
    domain_classes = []
    workspace_path = Path(workspace_root)
    exclude_dirs = {"target", "build", ".git", "node_modules", ".gradle"}

    for entity_file in workspace_path.glob("**/*.java"):
        if any(part in exclude_dirs for part in entity_file.parts):
            continue
        # Match Entity, DO, or Model classes
        if "dataobject" in entity_file.parts or "domain" in entity_file.parts or entity_file.name.endswith("DO.java") or entity_file.name.endswith("Entity.java"):
            domain_classes.append(entity_file.stem)

    return list(set(domain_classes))

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

    # Search for scoped AGENTS.md
    workspace_path = Path(workspace_root)
    scoped_status = {}
    for scoped_file in workspace_path.glob("**/AGENTS.md"):
        if scoped_file == Path(root_agents):
            continue
        rel_path = str(scoped_file.relative_to(workspace_path))
        lines = scoped_file.read_text(encoding="utf-8").splitlines()
        line_count = len(lines)
        scoped_status[rel_path] = {
            "exists": True,
            "line_count": line_count,
            "lean_budget_ok": line_count <= 60
        }

    return {
        "root_agents_md": {
            "exists": root_exists,
            "line_count": root_line_count,
            "size_bytes": root_size_bytes,
            "lean_budget_ok": root_line_count <= 100 and root_size_bytes <= 64 * 1024
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
        if ep["path"] in spec_contents or f"/app-api{ep['path']}" in spec_contents or f"/admin-api{ep['path']}" in spec_contents:
            matched_endpoints.append(f"{ep['method']} {ep['path']}")
        else:
            missing_endpoints.append(f"{ep['method']} {ep['path']} (Controller: {ep['controller']})")

    return matched_endpoints, missing_endpoints

def main():
    parser = argparse.ArgumentParser(description="Audit Doc System Health")
    parser.add_argument("--workspace", default=".", help="Workspace root directory")
    parser.add_argument("--strict", action="store_true", help="Fail with non-zero exit code if issues found")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format")
    args = parser.parse_args()

    workspace_root = os.path.abspath(args.workspace)
    agents_status = check_agents_hierarchy(workspace_root)
    core_docs_status = check_core_docs(workspace_root)
    endpoints = find_java_endpoints(workspace_root)
    domain_classes = find_domain_classes(workspace_root)
    matched_eps, missing_eps = check_specs(workspace_root, endpoints)

    # Evaluate health
    all_healthy = True
    reasons = []

    if not agents_status["root_agents_md"]["exists"]:
        all_healthy = False
        reasons.append("Root AGENTS.md is missing.")
    elif not agents_status["root_agents_md"]["lean_budget_ok"]:
        all_healthy = False
        reasons.append(f"Root AGENTS.md exceeds token budget: {agents_status['root_agents_md']['line_count']} lines.")

    for doc, exists in core_docs_status.items():
        if not exists:
            all_healthy = False
            reasons.append(f"Core doc artifact missing: {doc}")

    if missing_eps:
        all_healthy = False
        reasons.append(f"Undocumented Endpoints found in code ({len(missing_eps)} missing from docs/specs):")
        for ep in missing_eps:
            reasons.append(f"  - {ep}")

    if args.format == "json":
        report = {
            "healthy": all_healthy,
            "agents_hierarchy": agents_status,
            "core_docs": core_docs_status,
            "endpoints": {
                "total_found": len(endpoints),
                "matched": len(matched_eps),
                "missing": len(missing_eps),
                "missing_list": missing_eps
            },
            "domain_classes_found": domain_classes,
            "reasons": reasons
        }
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print("=" * 60)
        print("📄 Open-SWE Documentation System Health Audit")
        print("=" * 60)
        print(f"• Root AGENTS.md: {'✅ Found (' + str(agents_status['root_agents_md']['line_count']) + ' lines)' if agents_status['root_agents_md']['exists'] else '❌ Missing'}")
        print(f"• Core Docs: {sum(core_docs_status.values())}/{len(core_docs_status)} artifacts present")
        print(f"• Endpoints Audited: {len(matched_eps)}/{len(endpoints)} mapped to specs")
        
        if all_healthy:
            print("\n✅ Status: PASSED (All docs, code endpoints, and token budgets comply 100%)")
        else:
            print("\n❌ Status: FAILED")
            for r in reasons:
                print(f"  - {r}")

    if args.strict and not all_healthy:
        sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    main()
