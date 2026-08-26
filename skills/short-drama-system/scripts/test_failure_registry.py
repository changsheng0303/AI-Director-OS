#!/usr/bin/env python3
"""Regression tests for the failure registry validator."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
VALIDATOR = Path(__file__).resolve().parent / "validate_failure_registry.py"
REPO_REGISTRY = ROOT / "quality" / "failure-registry.jsonl"
LOCAL_FIXTURE = Path(__file__).resolve().parents[1] / "examples" / "failure-registry-valid.jsonl"
REGISTRY = REPO_REGISTRY if REPO_REGISTRY.is_file() else LOCAL_FIXTURE


def run(path: Path, expected: int) -> bool:
    result = subprocess.run([sys.executable, str(VALIDATOR), str(path)], capture_output=True, text=True, encoding="utf-8", env={**os.environ, "PYTHONUTF8": "1"})
    return result.returncode == expected


def main() -> int:
    valid = run(REGISTRY, 0)
    with tempfile.TemporaryDirectory(prefix="failure-registry-test-") as temp_dir:
        bad_path = Path(temp_dir) / "bad.jsonl"
        bad_path.write_text(json.dumps({"id": "bad", "evidence_type": "generation_output"}, ensure_ascii=False), encoding="utf-8")
        invalid = run(bad_path, 1)
    print("PASS registry-valid" if valid else "FAIL registry-valid")
    print("PASS registry-invalid" if invalid else "FAIL registry-invalid")
    return 0 if valid and invalid else 1


if __name__ == "__main__":
    raise SystemExit(main())
