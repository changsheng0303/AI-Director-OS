#!/usr/bin/env python3
"""Validate a Markdown project record with no external dependencies."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


REQUIRED_GROUPS = {
    "overview": {"项目概览", "Project Overview"},
    "scope": {"目标与范围", "Goals and Scope"},
    "status": {"当前状态", "Current Status"},
    "decisions": {"关键决策", "Key Decisions"},
    "deliverables": {"交付物", "Deliverables"},
    "risks": {"风险与问题", "Risks and Issues"},
    "next": {"下一步", "Next Steps"},
    "history": {"版本记录", "Version History"},
}


def validate(text):
    errors, warnings = [], []
    headings = re.findall(r"^#{1,6}\s+(.+?)\s*$", text, flags=re.M)
    h1 = re.findall(r"^#\s+(.+?)\s*$", text, flags=re.M)
    if len(h1) != 1:
        errors.append(f"expected exactly one H1 title, found {len(h1)}")
    normalized = {item.strip() for item in headings}
    for key, variants in REQUIRED_GROUPS.items():
        if not normalized.intersection(variants):
            errors.append(f"missing required section group: {key}")
    duplicates = sorted({item for item in headings if headings.count(item) > 1})
    if duplicates:
        errors.append("duplicate headings: " + ", ".join(duplicates))
    placeholders = sorted(set(re.findall(r"\{\{[^{}]+\}\}", text)))
    if placeholders:
        errors.append("unresolved template placeholders: " + ", ".join(placeholders))
    if not re.search(r"(?i)(文档版本|document version|版本\s*[:：])", text):
        warnings.append("document version is not explicit")
    if not re.search(r"(?i)(更新日期|updated|date\s*[:：])", text):
        warnings.append("document date is not explicit")
    return errors, warnings


def main():
    parser = argparse.ArgumentParser(description="Validate Markdown project documentation")
    parser.add_argument("path")
    args = parser.parse_args()
    text = Path(args.path).read_text(encoding="utf-8-sig")
    errors, warnings = validate(text)
    print("PASS" if not errors else "FAIL")
    for item in errors:
        print("ERROR:", item)
    for item in warnings:
        print("WARN:", item)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
