#!/usr/bin/env python3
"""
AI 2D Animation Story Contract Validator V1.5
校验 story-contract.schema.json 对应的故事契约 + 基本 Beat Chain 因果检查。
No external dependencies required.
"""
import argparse, json, sys

REQUIRED_STORY = ["story_id","premise","story_question","theme","protagonist_want",
                  "protagonist_need","core_flaw_or_belief","opposition","stakes",
                  "inciting_incident","turning_points","climax_choice","consequence",
                  "resolution","character_arc","relationship_arc","motif_arc",
                  "foreshadow_payoff_map"]
STAKES_KEYS = ["external","internal","relational"]
TURNING_KEYS = ["first","midpoint","second"]

def validate_story(s, index=None):
    issues, warnings = [], []
    tag = f"Story {index}" if index else "Story"

    if not isinstance(s, dict):
        return [f"{tag}: not an object"], []

    missing = [x for x in REQUIRED_STORY if x not in s]
    if missing:
        issues.append(f"{tag}: missing fields: {', '.join(missing)}")

    # 非空检查（核心叙事字段不能为空）
    for field in ["premise","story_question","theme","protagonist_want","protagonist_need",
                  "opposition","inciting_incident","climax_choice","consequence","resolution"]:
        if field in s and not (s.get(field) or "").strip():
            issues.append(f"{tag}: empty {field}")

    # Stakes 三维
    stakes = s.get("stakes")
    if isinstance(stakes, dict):
        for k in STAKES_KEYS:
            if k not in stakes:
                warnings.append(f"{tag}: stakes missing '{k}' dimension (external/internal/relational)")
    elif stakes is not None:
        warnings.append(f"{tag}: stakes should be an object with external/internal/relational")

    # Turning Points
    tp = s.get("turning_points")
    if isinstance(tp, dict):
        for k in TURNING_KEYS:
            if k not in tp:
                warnings.append(f"{tag}: turning_points missing '{k}'")
    elif tp is not None:
        warnings.append(f"{tag}: turning_points should be an object")

    # Want vs Need 张力（Story Architecture 要求两者存在张力）
    want = (s.get("protagonist_want") or "").strip()
    need = (s.get("protagonist_need") or "").strip()
    if want and need and want == need:
        warnings.append(f"{tag}: protagonist_want == protagonist_need; no internal tension")

    # Foreshadow/Payoff map
    fp = s.get("foreshadow_payoff_map")
    if fp is not None:
        if not isinstance(fp, list):
            issues.append(f"{tag}: foreshadow_payoff_map must be an array")
        else:
            for i, item in enumerate(fp, 1):
                if not isinstance(item, dict):
                    issues.append(f"{tag}: foreshadow_payoff_map[{i}] not an object")
                    continue
                for k in ["seed","reinforcement","payoff"]:
                    if k not in item:
                        warnings.append(f"{tag}: foreshadow_payoff_map[{i}] missing '{k}'")
    else:
        warnings.append(f"{tag}: no foreshadow_payoff_map; foreshadow may be unplanned")

    return issues, warnings

def validate_beats(beats):
    issues, warnings = [], []
    if not isinstance(beats, list) or not beats:
        return [], [f"Beats: empty or not a list (optional, skipped)"]

    for i, b in enumerate(beats, 1):
        tag = f"Beat {i}"
        if not isinstance(b, dict):
            issues.append(f"{tag}: not an object")
            continue
        # 因果链：new_state[N] 解释 trigger[N+1]
        if i > 1:
            prev_new = (beats[i-2].get("new_state") or "").strip() if isinstance(beats[i-2], dict) else ""
            trig = (b.get("trigger") or "").strip()
            if prev_new and trig and prev_new.lower() not in trig.lower() and trig.lower() not in prev_new.lower():
                warnings.append(f"{tag}: trigger not obviously explained by previous beat's new_state (causal chain risk)")

        # 情绪跳级：emotion_delta 应有过渡
        ed = (b.get("emotion_delta") or "").strip()
        if ed and any(w in ed.lower() for w in ["冷静→崩溃","calm→break","jump","直接","突然"]):
            warnings.append(f"{tag}: emotion_delta may skip ladder steps (story-craft §5)")

    return issues, warnings

def validate_file(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    issues, warnings = [], []

    # Story 部分（单个或列表）
    if isinstance(data, dict) and "stories" in data:
        stories = data["stories"]
    elif isinstance(data, list):
        stories = data
    else:
        stories = [data]

    for i, s in enumerate(stories, 1):
        i_, w_ = validate_story(s, i)
        issues.extend(i_)
        warnings.extend(w_)

    # Beats 部分（可选）
    if isinstance(data, dict) and "beats" in data:
        bi_, bw_ = validate_beats(data["beats"])
        issues.extend(bi_)
        warnings.extend(bw_)

    print("PASS" if not issues else "FAIL")
    for x in issues: print("ERROR:", x)
    for x in warnings: print("WARN:", x)
    return 0 if not issues else 1

def main():
    p = argparse.ArgumentParser(description="Validate Story Contract records (V1.5)")
    p.add_argument("path", help="JSON file with a story object, array, {'stories': [...]}, or {'stories': [...], 'beats': [...]}")
    args = p.parse_args()
    return validate_file(args.path)

if __name__ == "__main__":
    raise SystemExit(main())
