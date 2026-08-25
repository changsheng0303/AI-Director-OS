#!/usr/bin/env python3
"""
AI 2D Animation Story Architecture V1.7 Validator
校验 story-architecture-v1.7.schema.json 对应的 State Ledger / Promise Registry。
No external dependencies required.
"""
import argparse, json, sys

def validate_arch(a, index=None):
    issues, warnings = [], []
    tag = f"Architecture {index}" if index else "Architecture"

    if not isinstance(a, dict):
        return [f"{tag}: not an object"], []

    required = ["story_question", "state_ledger", "promises", "scenes"]
    missing = [x for x in required if x not in a]
    if missing:
        issues.append(f"{tag}: missing fields: {', '.join(missing)}")

    # story_question 非空
    sq = (a.get("story_question") or "").strip()
    if not sq:
        issues.append(f"{tag}: empty story_question")

    # State Ledger：每个状态必须有 name + initial + final
    ledger = a.get("state_ledger")
    if isinstance(ledger, list):
        for i, s in enumerate(ledger, 1):
            if not isinstance(s, dict):
                issues.append(f"{tag}: state_ledger[{i}] not an object")
                continue
            for k in ["name", "initial", "final"]:
                if k not in s:
                    warnings.append(f"{tag}: state_ledger[{i}] missing '{k}'")
        # 状态必须有变化
        changed = [s for s in ledger if isinstance(s, dict) and s.get("initial") != s.get("final")]
        if ledger and not changed:
            warnings.append(f"{tag}: no state changes — story has no movement")
    elif ledger is not None:
        warnings.append(f"{tag}: state_ledger should be an array")

    # Promise Registry：每个 promise 必须有 seed + payoff
    promises = a.get("promises")
    if isinstance(promises, list):
        for i, pr in enumerate(promises, 1):
            if not isinstance(pr, dict):
                issues.append(f"{tag}: promises[{i}] not an object")
                continue
            for k in ["seed", "payoff"]:
                if k not in pr:
                    warnings.append(f"{tag}: promises[{i}] missing '{k}'")
        # 有 promise 无 payoff 检查（seed 数量 vs payoff 数量）
        seeds = [p for p in promises if isinstance(p, dict) and "seed" in p]
        payoffs = [p for p in promises if isinstance(p, dict) and "payoff" in p]
        if len(seeds) > len(payoffs):
            warnings.append(f"{tag}: {len(seeds) - len(payoffs)} promises may lack payoff (unresolved foreshadow)")
    elif promises is not None:
        warnings.append(f"{tag}: promises should be an array")

    # Scenes：每场必须有 turn
    scenes = a.get("scenes")
    if isinstance(scenes, list):
        for i, s in enumerate(scenes, 1):
            if not isinstance(s, dict):
                issues.append(f"{tag}: scenes[{i}] not an object")
                continue
            turn = s.get("turn") or s.get("scene_turn")
            if not turn:
                warnings.append(f"{tag}: scenes[{i}] missing 'turn' — scene must change state")
    elif scenes is not None:
        warnings.append(f"{tag}: scenes should be an array")

    return issues, warnings

def validate_file(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    issues, warnings = [], []
    if isinstance(data, list):
        items = data
    elif isinstance(data, dict) and "architectures" in data:
        items = data["architectures"]
    else:
        items = [data]

    for i, a in enumerate(items, 1):
        i_, w_ = validate_arch(a, i)
        issues.extend(i_)
        warnings.extend(w_)

    print("PASS" if not issues else "FAIL")
    for x in issues: print("ERROR:", x)
    for x in warnings: print("WARN:", x)
    return 0 if not issues else 1

def main():
    p = argparse.ArgumentParser(description="Validate Story Architecture V1.7 records")
    p.add_argument("path", help="JSON file with an architecture object, array, or {'architectures': [...]}")
    args = p.parse_args()
    return validate_file(args.path)

if __name__ == "__main__":
    raise SystemExit(main())
