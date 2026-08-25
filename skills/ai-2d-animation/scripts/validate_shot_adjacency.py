#!/usr/bin/env python3
"""
AI 2D Animation Shot Adjacency Validator V1.5
校验 shot-adjacency.schema.json 对应的相邻镜头契约。
实现 30/70 原则、连续性五锁、ADJACENCY_RISK 检测。
No external dependencies required.
"""
import argparse, json, re, sys

ADJACENCY_TYPES = {"CONTINUE","REACT","REVEAL","CUTAWAY","BRIDGE","CONTRAST","SCENE_BREAK","TIME_JUMP"}
ANCHORS = ["character","space","direction","gaze","prop","lighting","action_phase"]
REQUIRED = ["shot_id","previous_shot","adjacency_type","start_state","end_state",
            "spatial_anchor","subject_screen_position","gaze_match","action_match",
            "prop_match","lighting_match","bridge_reason","transition_risk"]

def validate_adjacency(adj, index=None):
    issues, warnings = [], []
    tag = f"Adjacency {index}" if index else "Adjacency"

    if not isinstance(adj, dict):
        return [f"{tag}: not an object"], []

    missing = [x for x in REQUIRED if x not in adj]
    if missing:
        issues.append(f"{tag}: missing fields: {', '.join(missing)}")

    atype = (adj.get("adjacency_type") or "").upper()
    if atype and atype not in ADJACENCY_TYPES:
        issues.append(f"{tag}: adjacency_type '{atype}' not in {sorted(ADJACENCY_TYPES)}")

    # 30/70 原则：检测变更变量数量（超过3个关键变量 = HARD_CHANGE 风险）
    changed = []
    for field in ["subject_screen_position","gaze_match","action_match","prop_match","lighting_match"]:
        v = (adj.get(field) or "").strip()
        if v and v.lower() not in {"same","不变","keep","kept","unchanged","none","-" }:
            if any(w in v.lower() for w in ["change","changed","new","moved","shift","flip","reverse","变","新","移动","反转","切换"]):
                changed.append(field)
    if len(changed) > 3:
        warnings.append(f"{tag}: {len(changed)} variables changed > 3; mark HARD_CHANGE or add a bridge shot")

    # 五锁：spatial_anchor 数组至少 3 个
    anchors = adj.get("spatial_anchor") or []
    if isinstance(anchors, list) and len(anchors) < 3:
        warnings.append(f"{tag}: fewer than 3 spatial anchors ({len(anchors)}); Six Anchors rule wants >= 3 shared")
    elif not anchors:
        issues.append(f"{tag}: spatial_anchor is required (list of >= 3)")

    # SCENE_BREAK / TIME_JUMP 必须提供 bridge_reason
    if atype in {"SCENE_BREAK","TIME_JUMP","CONTRAST","CUTAWAY"}:
        br = (adj.get("bridge_reason") or "").strip()
        if not br:
            issues.append(f"{tag}: {atype} requires bridge_reason")

    # CONTINUE / REACT / REVEAL：start_state 与 end_state 必须非空
    ss = (adj.get("start_state") or "").strip()
    es = (adj.get("end_state") or "").strip()
    if atype in {"CONTINUE","REACT","REVEAL","BRIDGE"}:
        if not ss or not es:
            issues.append(f"{tag}: {atype} requires start_state and end_state")
    if ss and es and ss == es:
        warnings.append(f"{tag}: start_state == end_state; no observable change between shots")

    # SCENE_BREAK / TIME_JUMP 允许 start==end（状态重置），不报警——上面已限定类型

    return issues, warnings

def validate_file(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    issues, warnings = [], []
    if isinstance(data, list):
        items = data
    elif isinstance(data, dict) and "adjacencies" in data:
        items = data["adjacencies"]
    else:
        items = [data]

    for i, a in enumerate(items, 1):
        i_, w_ = validate_adjacency(a, i)
        issues.extend(i_)
        warnings.extend(w_)

    # 链完整性：previous_shot 必须能在集合中找到（首条除外）
    ids = {a.get("shot_id") for a in items if a.get("shot_id")}
    for i, a in enumerate(items, 1):
        prev = (a.get("previous_shot") or "").strip()
        if prev and prev not in ids and i > 1:
            warnings.append(f"Adjacency {i}: previous_shot '{prev}' not found in shot set")

    print("PASS" if not issues else "FAIL")
    for x in issues: print("ERROR:", x)
    for x in warnings: print("WARN:", x)
    return 0 if not issues else 1

def main():
    p = argparse.ArgumentParser(description="Validate Shot Adjacency records (V1.5)")
    p.add_argument("path", help="JSON file with an adjacency object, array, or {'adjacencies': [...]}")
    args = p.parse_args()
    return validate_file(args.path)

if __name__ == "__main__":
    raise SystemExit(main())
