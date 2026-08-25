#!/usr/bin/env python3
"""
AI 2D Animation Ending Contract Validator V1.7
校验 ending-contract.schema.json 对应的结尾契约。
No external dependencies required.
"""
import argparse, json, sys

ENDING_FUNCTIONS = {"RESOLVE", "IRONY", "OPEN", "REVERSAL", "CIRCLE", "CONSEQUENCE"}
CLOSURE_LEVELS = {"CLOSED", "PARTIAL", "OPEN_ENDED"}

def validate_ending(e, index=None):
    issues, warnings = [], []
    tag = f"Ending {index}" if index else "Ending"

    if not isinstance(e, dict):
        return [f"{tag}: not an object"], []

    required = ["ending_function", "exit_state", "ending_reason", "closure_strength"]
    missing = [x for x in required if x not in e]
    if missing:
        issues.append(f"{tag}: missing fields: {', '.join(missing)}")

    func = (e.get("ending_function") or "").upper()
    if func and func not in ENDING_FUNCTIONS:
        issues.append(f"{tag}: ending_function '{func}' not in {sorted(ENDING_FUNCTIONS)}")

    closure = (e.get("closure_strength") or "").upper()
    if closure and closure not in CLOSURE_LEVELS:
        issues.append(f"{tag}: closure_strength '{closure}' not in {sorted(CLOSURE_LEVELS)}")

    # 结尾功能 vs 收束强度 一致性
    if func == "OPEN" and closure == "CLOSED":
        issues.append(f"{tag}: OPEN ending with CLOSED closure — contradiction")
    if func in {"RESOLVE", "CIRCLE"} and closure == "OPEN_ENDED":
        warnings.append(f"{tag}: RESOLVE/CIRCLE ending with OPEN_ENDED closure — check intent")

    # 空字段检查
    for field in ["exit_state", "ending_reason"]:
        if field in e and not (e.get(field) or "").strip():
            issues.append(f"{tag}: empty {field}")

    return issues, warnings

def validate_file(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    issues, warnings = [], []
    if isinstance(data, list):
        items = data
    elif isinstance(data, dict) and "endings" in data:
        items = data["endings"]
    else:
        items = [data]

    for i, e in enumerate(items, 1):
        i_, w_ = validate_ending(e, i)
        issues.extend(i_)
        warnings.extend(w_)

    print("PASS" if not issues else "FAIL")
    for x in issues: print("ERROR:", x)
    for x in warnings: print("WARN:", x)
    return 0 if not issues else 1

def main():
    p = argparse.ArgumentParser(description="Validate Ending Contract records (V1.7)")
    p.add_argument("path", help="JSON file with an ending object, array, or {'endings': [...]}")
    args = p.parse_args()
    return validate_file(args.path)

if __name__ == "__main__":
    raise SystemExit(main())
