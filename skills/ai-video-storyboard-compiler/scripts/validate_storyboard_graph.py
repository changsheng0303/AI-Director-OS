#!/usr/bin/env python3
"""Validate the minimal Storyboard Graph without external dependencies."""
from __future__ import annotations
import argparse, json
from pathlib import Path

VALID_CUTS = {"scene_entry", "information", "reaction", "action_phase", "spatial_clarification", "contrast", "reveal", "rhythm_break"}

def unique(items, key, label, errors):
    values = {}
    for index, item in enumerate(items, 1):
        value = item.get(key) if isinstance(item, dict) else None
        if not value: errors.append(f"{label}[{index}] missing {key}")
        elif value in values: errors.append(f"duplicate {label} {value}")
        else: values[value] = item
    return values

def validate(data):
    errors, warnings = [], []
    if not isinstance(data, dict): return ["root must be an object"], []
    if data.get("schema_version") != "1.0": errors.append("schema_version must be 1.0")
    if not str(data.get("project_id", "")).strip(): errors.append("project_id is required")
    source = data.get("source", {})
    if not str(source.get("scene_id", "")).strip(): errors.append("source.scene_id is required")
    if source.get("status") not in {"provisional", "approved", "locked"}: errors.append("source.status is invalid")
    beats = unique(data.get("beats", []), "beat_id", "beat", errors)
    shots = unique(data.get("shots", []), "shot_id", "shot", errors)
    if not shots: errors.append("at least one shot is required")
    total, previous_end = 0.0, None
    for index, (shot_id, shot) in enumerate(shots.items()):
        duration = shot.get("duration_seconds")
        if not isinstance(duration, (int, float)) or duration <= 0: errors.append(f"shot {shot_id} duration_seconds must be positive")
        else: total += float(duration)
        for field in ("visual_action", "camera", "end_state"):
            if not str(shot.get(field, "")).strip(): errors.append(f"shot {shot_id} missing {field}")
        cut = shot.get("cut_motivation")
        if cut not in VALID_CUTS: errors.append(f"shot {shot_id} has invalid cut_motivation {cut}")
        if index == 0 and cut != "scene_entry": warnings.append(f"first shot {shot_id} should usually use scene_entry")
        for beat_id in shot.get("beat_ids", []):
            if beat_id not in beats: errors.append(f"shot {shot_id} references unknown beat {beat_id}")
        if previous_end and shot.get("start_state") and previous_end != shot.get("start_state"): warnings.append(f"shot {shot_id} start_state differs from previous end_state")
        previous_end = shot.get("end_state")
    groups = unique(data.get("clip_groups", []), "clip_id", "clip_group", errors)
    claimed = []
    for clip_id, group in groups.items():
        duration, group_duration = group.get("duration_seconds"), 0.0
        if not isinstance(duration, (int, float)) or duration <= 0: errors.append(f"clip group {clip_id} duration_seconds must be positive")
        for shot_id in group.get("shot_ids", []):
            if shot_id not in shots: errors.append(f"clip group {clip_id} references unknown shot {shot_id}")
            else: group_duration += float(shots[shot_id].get("duration_seconds", 0) or 0)
            claimed.append(shot_id)
        if isinstance(duration, (int, float)) and abs(group_duration - duration) > 0.25: errors.append(f"clip group {clip_id} duration does not equal its shots")
    duplicates = sorted({item for item in claimed if claimed.count(item) > 1})
    if duplicates: errors.append("shots appear in multiple clip groups: " + ", ".join(duplicates))
    target = source.get("duration_target")
    if isinstance(target, (int, float)) and abs(total - target) > 0.5: errors.append(f"shot duration {total:.2f}s differs from target {target:.2f}s")
    return errors, warnings

def main():
    parser = argparse.ArgumentParser(); parser.add_argument("path"); args = parser.parse_args()
    data = json.loads(Path(args.path).read_text(encoding="utf-8-sig")); errors, warnings = validate(data)
    print("PASS" if not errors else "FAIL")
    for item in errors: print("ERROR:", item)
    for item in warnings: print("WARN:", item)
    return 1 if errors else 0

if __name__ == "__main__": raise SystemExit(main())
