#!/usr/bin/env python3
"""Validate the optimized Universal Dialogue Core package and preserved source lock."""

import hashlib
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REQUIRED = [
    "SKILL.md", "core-craft-rules.md", "dialogue-rubric.md",
    "scene-function-router.yaml", "voiceprint-schema.yaml",
    "continuity-ledger.yaml", "universal-dialogue-template.yaml",
    "references/source-v2.1-full.md", "references/system-integration.md",
    "references/logical-stress-contract.md", "scripts/compile_logical_stress.py",
    "scripts/test_logical_stress.py", "examples/logical-stress-line.json",
    "references/source-lock.json", "scripts/verify_dialogue_handoff.py",
]


def sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def main():
    errors = []
    for relative in REQUIRED:
        if not os.path.isfile(os.path.join(ROOT, *relative.split("/"))):
            errors.append(f"missing required file: {relative}")

    router_path = os.path.join(ROOT, "scene-function-router.yaml")
    if os.path.isfile(router_path):
        text = open(router_path, encoding="utf-8").read()
        for relative in re.findall(r"^\s+file:\s+(.+?)\s*$", text, re.M):
            if not os.path.isfile(os.path.join(ROOT, *relative.split("/"))):
                errors.append(f"router target missing: {relative}")

    lock_path = os.path.join(ROOT, "references", "source-lock.json")
    source_path = os.path.join(ROOT, "references", "source-v2.1-full.md")
    if os.path.isfile(lock_path) and os.path.isfile(source_path):
        lock = json.load(open(lock_path, encoding="utf-8"))
        actual = sha256(source_path)
        expected = lock.get("source_skill_sha256", "").upper()
        if actual != expected:
            errors.append(f"preserved source SKILL hash mismatch: expected {expected}, got {actual}")

    skill_text = open(os.path.join(ROOT, "SKILL.md"), encoding="utf-8").read()
    rubric_text = open(os.path.join(ROOT, "dialogue-rubric.md"), encoding="utf-8").read()
    skill_failure_section = skill_text.split("以下任一出现即FAIL：", 1)[-1].split("`TAIL_DRIFT`", 1)[0]
    hard_failures = set(re.findall(r"[A-Z][A-Z_]+", skill_failure_section))
    rubric_section = rubric_text.split("Hard Failure Gate", 1)[-1].split("Soft Failure", 1)[0]
    rubric_block = re.search(r"`([^`]+)`", rubric_section, re.S)
    rubric_failures = set(re.findall(r"[A-Z][A-Z_]+", rubric_block.group(1) if rubric_block else ""))
    if not hard_failures:
        errors.append("no hard failures found in SKILL.md")
    elif hard_failures != rubric_failures:
        errors.append(f"hard failure mismatch: skill={sorted(hard_failures)}, rubric={sorted(rubric_failures)}")

    for error in errors:
        print(f"[ERROR] {error}")
    if errors:
        print(f"FAIL: {len(errors)} error(s)")
        return 1
    print(f"PASS: universal-dialogue-core package; hard_failures={len(hard_failures)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
