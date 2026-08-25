#!/usr/bin/env python3
"""Verify DIALOGUE_CANON structure and exact-text handoff to an audio timeline."""

import argparse
import json
import sys


def load(path):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dialogue_canon")
    parser.add_argument("audio_timeline")
    args = parser.parse_args()
    raw = load(args.dialogue_canon)
    canon = raw.get("dialogue_canon", raw)
    audio = load(args.audio_timeline)
    errors = []

    for key in ("dialogue_id", "dialogue_version", "source_script_hash", "scene_id", "locked", "lines"):
        if key not in canon:
            errors.append(f"DIALOGUE_CANON missing {key}")
    if canon.get("locked") is not True:
        errors.append("DIALOGUE_CANON must be locked=true for production handoff")

    line_map = {}
    for line in canon.get("lines", []):
        line_id = line.get("line_id")
        if not line_id or line_id in line_map:
            errors.append(f"invalid or duplicate line_id: {line_id!r}")
            continue
        line_map[line_id] = line
        if not str(line.get("speaker", "")).strip():
            errors.append(f"{line_id}: speaker required")
        if not str(line.get("exact_text", "")).strip():
            errors.append(f"{line_id}: exact_text required")

    audio_items = audio.get("items", [])
    audio_by_line = {}
    for item in audio_items:
        if item.get("type") not in {"dialogue", "voiceover"}:
            continue
        line_id = item.get("line_id")
        if not line_id:
            errors.append("dialogue/voiceover audio item missing line_id")
            continue
        if line_id in audio_by_line:
            errors.append(f"duplicate audio item for {line_id}")
        audio_by_line[line_id] = item
        if line_id not in line_map:
            errors.append(f"audio references unknown line_id {line_id}")
            continue
        line = line_map[line_id]
        if item.get("exact_text") != line.get("exact_text"):
            errors.append(f"{line_id}: audio exact_text differs from DIALOGUE_CANON")
        if item.get("speaker") != line.get("speaker"):
            errors.append(f"{line_id}: audio speaker differs from DIALOGUE_CANON")
        if item.get("dialogue_version") != canon.get("dialogue_version"):
            errors.append(f"{line_id}: audio dialogue_version mismatch")
        start, end = item.get("timeline_start_sec"), item.get("timeline_end_sec")
        if not isinstance(start, (int, float)) or not isinstance(end, (int, float)) or end <= start:
            errors.append(f"{line_id}: invalid audio timeline interval")

    missing_audio = sorted(set(line_map) - set(audio_by_line))
    if missing_audio:
        errors.append(f"canonical lines missing from audio timeline: {missing_audio}")

    for error in errors:
        print(f"[ERROR] {error}")
    if errors:
        print(f"FAIL: {len(errors)} error(s)")
        return 1
    print(f"PASS: dialogue handoff; lines={len(line_map)}, version={canon.get('dialogue_version')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
