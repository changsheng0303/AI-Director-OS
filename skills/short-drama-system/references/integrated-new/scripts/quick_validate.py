#!/usr/bin/env python3
"""Validate the shortdrama-studio-lite Skill package."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "SKILL.md",
    "agents/openai.yaml",
    "references/asset-analysis.md",
    "references/image-assets.md",
    "references/video-prompts.md",
    "references/dreamina-execution.md",
    "scripts/request_fingerprint.py",
    "scripts/validate_outputs.py",
    "scripts/quick_validate.py",
]


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    paths = [ROOT / relative for relative in REQUIRED]
    for path in paths:
        if not path.is_file():
            errors.append(f"missing: {path.relative_to(ROOT)}")

    skill = ROOT / "SKILL.md"
    if skill.is_file():
        text = skill.read_text(encoding="utf-8")
        match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        if not match:
            errors.append("SKILL.md frontmatter missing or malformed")
        else:
            frontmatter = match.group(1)
            name = re.search(r"^name:\s*(.+)$", frontmatter, re.M)
            description = re.search(r"^description:\s*(.+)$", frontmatter, re.M)
            if not name or name.group(1).strip() != ROOT.name:
                errors.append("frontmatter name must match directory name")
            if not description or len(description.group(1).strip()) < 80:
                errors.append("frontmatter description is too weak")
        for heading in ["## 固定交付结构", "## 工作流", "## 验证", "## 完成定义", "## 边界"]:
            if heading not in text:
                errors.append(f"required heading missing: {heading}")
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
            if "://" in target or target.startswith("#"):
                continue
            resolved = (ROOT / target.split("#", 1)[0]).resolve()
            if not resolved.is_file():
                errors.append(f"broken SKILL.md link: {target}")

    agent = ROOT / "agents/openai.yaml"
    if agent.is_file():
        text = agent.read_text(encoding="utf-8")
        short = re.search(r'^\s*short_description:\s*"(.+)"$', text, re.M)
        if not short or not 25 <= len(short.group(1)) <= 64:
            errors.append("short_description must contain 25-64 characters")
        if "allow_implicit_invocation: true" not in text:
            warnings.append("implicit invocation is not enabled")

    for path in paths:
        if not path.is_file():
            continue
        data = path.read_text(encoding="utf-8")
        if path.suffix == ".py":
            try:
                compile(data, str(path), "exec")
            except SyntaxError as exc:
                errors.append(f"syntax error in {path.name}: {exc}")
        if re.search(r"\b(?:sk-[A-Za-z0-9_-]{16,}|AKIA[0-9A-Z]{16})\b", data):
            errors.append(f"possible secret in {path.relative_to(ROOT)}")

    self_tests = [
        ("output validator", ROOT / "scripts/validate_outputs.py"),
        ("request fingerprint", ROOT / "scripts/request_fingerprint.py"),
    ]
    if not errors:
        for label, script in self_tests:
            completed = subprocess.run([sys.executable, str(script), "--self-test"], capture_output=True, text=True, check=False)
            if completed.returncode != 0:
                errors.append(f"{label} self-test failed: {completed.stdout}{completed.stderr}")

    result = {
        "status": "SUCCESS" if not errors else "FAILED",
        "skill": ROOT.name,
        "root": str(ROOT),
        "filesChecked": len(paths),
        "errors": errors,
        "warnings": warnings,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
