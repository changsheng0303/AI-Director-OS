#!/usr/bin/env python3
"""Regression tests for the Creative Compiler Core.

The suite asserts both positive and negative fixtures. A validator that accepts
the deliberately broken fixture is a test failure.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
EXAMPLES = ROOT / "examples"


def run(name, expected, *args):
    command = [sys.executable, *map(str, args)]
    result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")
    if result.returncode != expected:
        print(f"FAIL {name}: expected exit {expected}, got {result.returncode}")
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)
        return False
    print(f"PASS {name} (exit {expected})")
    return True


def main():
    checks = [
        run(
            "narrative-valid",
            0,
            SCRIPTS / "validate_narrative_ir.py",
            EXAMPLES / "narrative-ir-valid.json",
        ),
        run(
            "narrative-invalid",
            1,
            SCRIPTS / "validate_narrative_ir.py",
            EXAMPLES / "narrative-ir-invalid.json",
        ),
        run(
            "shot-ir-valid",
            0,
            SCRIPTS / "validate_shot_ir.py",
            EXAMPLES / "shot-ir-valid.json",
            "--narrative-ir",
            EXAMPLES / "narrative-ir-valid.json",
            "--strict-provenance",
            "--strict-continuity",
            "--duration",
            "6",
        ),
        run(
            "state-diff-valid",
            0,
            SCRIPTS / "state_diff.py",
            EXAMPLES / "project-state-before-v1.6.json",
            EXAMPLES / "project-state-after-valid-v1.6.json",
        ),
        run(
            "state-diff-invalid",
            1,
            SCRIPTS / "state_diff.py",
            EXAMPLES / "project-state-before-v1.6.json",
            EXAMPLES / "project-state-after-invalid-v1.6.json",
        ),
        run(
            "legacy-story-contract",
            0,
            SCRIPTS / "validate_story_contract.py",
            EXAMPLES / "story-contract-demo.json",
        ),
        run(
            "legacy-storyboard-csv",
            0,
            SCRIPTS / "validate_storyboard.py",
            EXAMPLES / "example-storyboard.csv",
        ),
    ]
    if all(checks):
        print("CREATIVE_COMPILER_REGRESSION_PASS")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
