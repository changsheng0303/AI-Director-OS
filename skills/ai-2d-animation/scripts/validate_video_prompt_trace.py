#!/usr/bin/env python3
"""
AI 2D Animation Video Prompt Trace Validator V1.4
校验 video-prompt-trace.schema.json 对应的 TRACE 记录。
No external dependencies required.
"""
import argparse, json, re, sys

CAMERA_LOGIC_VALUES = {"ESTABLISH","OBSERVE","WITHHOLD","ALIGN","ESCALATE","REVEAL","MISDIRECT","RECONTEXTUALIZE","CONTRAST","RELEASE"}
CAMERA_NECESSITY_VALUES = {"information","emotion","spatial_understanding","none"}
REQUIRED = ["shot_id","shot_version","camera_logic","camera_necessity","locked_variables","changed_variables","primary_motion","trigger","start_state","end_state"]

def validate_trace(trace, index=None):
    """校验单条 TRACE 记录，返回 (issues, warnings)"""
    issues, warnings = [], []
    tag = f"Trace {index}" if index else "Trace"

    if not isinstance(trace, dict):
        return [f"{tag}: not an object"], []

    missing = [x for x in REQUIRED if x not in trace]
    if missing:
        issues.append(f"{tag}: missing fields: {', '.join(missing)}")

    logic = (trace.get("camera_logic") or "").upper()
    if logic and logic not in CAMERA_LOGIC_VALUES:
        issues.append(f"{tag}: camera_logic '{logic}' not in {sorted(CAMERA_LOGIC_VALUES)}")

    nec = (trace.get("camera_necessity") or "").lower()
    if nec and nec not in CAMERA_NECESSITY_VALUES:
        issues.append(f"{tag}: camera_necessity '{nec}' invalid")

    # locked_variables 必须在 changed_variables 之外（锁定变量不得改变）
    locked = set(trace.get("locked_variables") or [])
    changed = set(trace.get("changed_variables") or [])
    overlap = locked & changed
    if overlap:
        issues.append(f"{tag}: variables both locked and changed: {sorted(overlap)}")

    # 单主动作原则：primary_motion 不应包含多个并列动作
    pm = (trace.get("primary_motion") or "").strip()
    if pm:
        multi_action_marks = [" and ", " while ", " simultaneously ", " both "]
        if any(m in pm.lower() for m in multi_action_marks):
            warnings.append(f"{tag}: primary_motion may contain multiple actions (V1.4 single-action rule)")

    # start_state / end_state 必须非空且不同
    ss = (trace.get("start_state") or "").strip()
    es = (trace.get("end_state") or "").strip()
    if not ss or not es:
        issues.append(f"{tag}: start_state and end_state are required")
    elif ss == es:
        warnings.append(f"{tag}: start_state == end_state; no observable change")

    return issues, warnings

def validate_file(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    issues, warnings = [], []
    if isinstance(data, list):
        traces = data
    elif isinstance(data, dict) and "traces" in data:
        traces = data["traces"]
    else:
        traces = [data]

    for i, t in enumerate(traces, 1):
        i_, w_ = validate_trace(t, i)
        issues.extend(i_)
        warnings.extend(w_)

    # shot_version 格式检查
    for i, t in enumerate(traces, 1):
        v = (t.get("shot_version") or "").strip()
        if v and not re.match(r"^v\d{3}$", v):
            issues.append(f"Trace {i}: shot_version '{v}' must match v000 format")

    print("PASS" if not issues else "FAIL")
    for x in issues: print("ERROR:", x)
    for x in warnings: print("WARN:", x)
    return 0 if not issues else 1

def main():
    p = argparse.ArgumentParser(description="Validate Video Prompt Trace records (V1.4)")
    p.add_argument("path", help="JSON file with a trace object, array, or {'traces': [...]}")
    args = p.parse_args()
    return validate_file(args.path)

if __name__ == "__main__":
    raise SystemExit(main())
