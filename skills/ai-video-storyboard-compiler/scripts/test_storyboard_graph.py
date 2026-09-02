#!/usr/bin/env python3
from __future__ import annotations
import os, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; VALIDATOR = ROOT / "scripts" / "validate_storyboard_graph.py"
def run(name, expected, path):
    result = subprocess.run([sys.executable, str(VALIDATOR), str(path)], capture_output=True, text=True, encoding="utf-8", env={**os.environ, "PYTHONUTF8": "1"})
    ok = result.returncode == expected; print(("PASS" if ok else "FAIL"), name)
    if not ok: print(result.stdout, result.stderr)
    return ok
def main():
    checks=[run("storyboard-valid",0,ROOT/"examples"/"storyboard-graph-valid.json"),run("storyboard-invalid",1,ROOT/"examples"/"storyboard-graph-invalid.json")]
    return 0 if all(checks) else 1
if __name__ == "__main__": raise SystemExit(main())
