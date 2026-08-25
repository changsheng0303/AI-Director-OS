#!/usr/bin/env python3
"""Regression tests for IP Foundation Package validators and interview routing."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
EXAMPLES = ROOT / "examples"


def run(name, expected, *args):
    environment = {**os.environ, "PYTHONUTF8": "1"}
    result = subprocess.run([sys.executable, *map(str, args)], capture_output=True, text=True, encoding="utf-8", env=environment)
    if result.returncode != expected:
        print(f"FAIL {name}: expected {expected}, got {result.returncode}")
        print(result.stdout)
        print(result.stderr)
        return False
    print(f"PASS {name}")
    return True


def main():
    valid = EXAMPLES / "foundation-valid.json"
    invalid = EXAMPLES / "foundation-invalid.json"
    checks = [
        run("foundation-valid", 0, SCRIPTS / "validate_ip_foundation.py", valid),
        run("foundation-invalid", 1, SCRIPTS / "validate_ip_foundation.py", invalid),
        run("foundation-render", 0, SCRIPTS / "render_foundation_markdown.py", valid),
        run("foundation-handoff", 0, SCRIPTS / "build_foundation_handoff.py", valid),
    ]
    route = subprocess.run([sys.executable, str(SCRIPTS / "question_router.py"), str(valid)], capture_output=True, text=True, encoding="utf-8", env={**os.environ, "PYTHONUTF8": "1"})
    try:
        routed = json.loads(route.stdout)
        question_ok = (
            route.returncode == 0
            and routed.get("packet_mode") == "single_stage_batch"
            and routed.get("option_contract", {}).get("D") == "补充内容／自定义"
            and len(routed["questions"]) <= 6
            and all(item["field"] != "project.format" for item in routed["questions"])
        )
    except (json.JSONDecodeError, KeyError):
        question_ok = False
    checks.append(question_ok)
    print("PASS question-router" if question_ok else "FAIL question-router")
    if all(checks):
        print("IP_FOUNDATION_REGRESSION_PASS")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
