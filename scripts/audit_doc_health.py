#!/usr/bin/env python3
"""
audit_doc_health.py
AI 核心文档体系与代码一致性自动化巡检脚本
"""

import os
import re
import json
import sys

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
                    
                    # 获取类级别的 RequestMapping
                    class_mapping = ""
                    class_match = re.search(r'@RequestMapping\(["\'](.*?)["\']\)', content)
                    if class_match:
                        class_mapping = class_match.group(1)

                    # 匹配 PostMapping
                    for m in re.finditer(r'@PostMapping(?:\(["\'](.*?)["\']\))?', content):
                        path = m.group(1) or ""
                        full_path = f"{class_mapping}{path}".replace("//", "/")
                        endpoints.append({"method": "POST", "path": full_path, "controller": file})

                    # 匹配 GetMapping
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

def check_specs(workspace_root, endpoints):
    specs_dir = os.path.join(workspace_root, "docs/specs")
    existing_specs = []
    if os.path.exists(specs_dir):
        for file in os.listdir(specs_dir):
            if file.endswith(".md"):
                with open(os.path.join(specs_dir, file), "r", encoding="utf-8") as f:
                    existing_specs.append({"file": file, "content": f.read()})

    missing_specs = []
    matched_specs = []
    for ep in endpoints:
        matched = False
        # 去掉路径变量如 {orderId}
        base_path = re.sub(r'\{.*?\}', '', ep["path"])
        for spec in existing_specs:
            if ep["path"] in spec["content"] or (base_path and base_path in spec["content"]):
                matched = True
                matched_specs.append({"endpoint": f"{ep['method']} {ep['path']}", "spec": spec["file"]})
                break
        if not matched:
            missing_specs.append(f"{ep['method']} {ep['path']} (Controller: {ep['controller']})")

    return matched_specs, missing_specs

def check_glossary(workspace_root, domain_classes):
    glossary_path = os.path.join(workspace_root, "docs/domain-glossary.md")
    if not os.path.exists(glossary_path):
        return [], domain_classes

    with open(glossary_path, "r", encoding="utf-8") as f:
        content = f.read()

    matched_classes = []
    missing_classes = []
    for cls in domain_classes:
        if cls in content:
            matched_classes.append(cls)
        else:
            missing_classes.append(cls)

    return matched_classes, missing_classes

def check_core_docs(workspace_root):
    required_files = [
        "AGENTS.md",
        "docs/architecture.md",
        "docs/domain-glossary.md",
        "docs/runbook.md",
    ]
    status = {}
    for req in required_files:
        full_path = os.path.join(workspace_root, req)
        status[req] = os.path.exists(full_path)
    return status

def main():
    # 查找工作区根目录
    current_dir = os.path.abspath(os.path.dirname(__file__))
    workspace_root = os.path.abspath(os.path.join(current_dir, "../../../"))
    
    # 验证是否为项目根目录
    if not os.path.exists(os.path.join(workspace_root, "app")):
        workspace_root = os.getcwd()

    core_docs = check_core_docs(workspace_root)
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

    report = {
        "overall_health_score": f"{overall_health}%",
        "status": "HEALTHY" if overall_health >= 90 else "NEEDS_ATTENTION",
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

if __name__ == "__main__":
    main()
