#!/usr/bin/env python3
from __future__ import annotations
import subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];VALIDATOR=ROOT/"scripts"/"validate_screenplay_graph.py"
def run(name,expected,path):
    r=subprocess.run([sys.executable,str(VALIDATOR),str(path)],capture_output=True,text=True,encoding="utf-8");ok=r.returncode==expected;print(("PASS" if ok else "FAIL"),name)
    if not ok: print(r.stdout,r.stderr)
    return ok
def main():
    checks=[run("screenplay-valid",0,ROOT/"examples"/"screenplay-graph-valid.json"),run("screenplay-invalid",1,ROOT/"examples"/"screenplay-graph-invalid.json")]
    return 0 if all(checks) else 1
if __name__=="__main__":raise SystemExit(main())
