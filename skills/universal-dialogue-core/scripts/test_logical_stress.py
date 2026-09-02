#!/usr/bin/env python3
from __future__ import annotations
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"scripts"))
from compile_logical_stress import compile_line,validate
def main():
    line=json.loads((ROOT/"examples"/"logical-stress-line.json").read_text(encoding="utf-8"))
    checks=["**_不能_**" in compile_line(line,"fountain"),"<emphasis level=\"strong\">不能</emphasis>" in compile_line(line,"ssml"),"逻辑重音" in compile_line(line,"screenplay")]
    broken=dict(line);broken["logical_stress"]=[{"span":"从未出现","role":"contrast","strength":"strong"}];checks.append(bool(validate(broken)))
    print("LOGICAL_STRESS_REGRESSION_PASS" if all(checks) else "LOGICAL_STRESS_REGRESSION_FAIL")
    return 0 if all(checks) else 1
if __name__=="__main__":raise SystemExit(main())
