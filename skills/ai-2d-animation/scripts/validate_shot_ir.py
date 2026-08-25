#!/usr/bin/env python3
"""Validate JSON Shot Contract / Shot IR records and their provenance chain."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


VERSION_RE = re.compile(r"^v\d{3}$")
SHA256_RE = re.compile(r"^[a-fA-F0-9]{64}$")
REQUIRED = [
    "shot_id", "purpose", "beat", "subject", "acting", "action", "key_pose",
    "composition", "shot_size", "camera_angle", "camera_motion", "screen_direction",
    "timing", "animation_treatment", "continuity_in", "continuity_out",
    "generation_risk", "acceptance_criteria", "anime_treatment", "visual_question",
    "audience_knowledge", "character_knowledge", "information_withheld", "reveal_point",
    "emotional_landing", "camera_strategy", "camera_logic", "camera_necessity", "version",
    "previous_shot", "adjacency_type", "start_state", "end_state", "spatial_anchor",
    "subject_screen_position", "gaze_match", "action_match", "prop_match", "lighting_match",
    "bridge_reason",
]
BREAK_TYPES = {"SCENE_BREAK", "TIME_JUMP", "BRIDGE"}


def load_shots(path):
    data = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and "shots" in data:
        return data["shots"]
    return [data]


def validate(shots, narrative=None, strict_provenance=False, strict_continuity=False, target_duration=None):
    errors, warnings = [], []
    if not isinstance(shots, list) or not shots:
        return ["shots must be a non-empty array"], []

    narrative_scenes = set()
    narrative_hash = None
    narrative_id = None
    if narrative:
        narrative_scenes = {item.get("scene_id") for item in narrative.get("scenes", [])}
        narrative_hash = (narrative.get("source") or {}).get("source_hash")
        narrative_id = narrative.get("narrative_id")

    seen = set()
    previous = None
    previous_end = None
    previous_scene = None
    total_duration = 0.0

    for index, shot in enumerate(shots, 1):
        tag = f"shot[{index}]"
        if not isinstance(shot, dict):
            errors.append(f"{tag} must be an object")
            continue
        shot_id = shot.get("shot_id")
        if not shot_id:
            errors.append(f"{tag} missing shot_id")
        elif shot_id in seen:
            errors.append(f"duplicate shot_id {shot_id}")
        seen.add(shot_id)

        missing = [field for field in REQUIRED if field not in shot]
        if missing:
            errors.append(f"{tag} missing fields: {', '.join(missing)}")
        if shot.get("version") and not VERSION_RE.fullmatch(str(shot["version"])):
            errors.append(f"{tag} invalid version {shot.get('version')}")

        source_ref = shot.get("source_ref")
        canon = shot.get("canon")
        render = shot.get("render")
        if strict_provenance:
            for field, value in (("source_ref", source_ref), ("canon", canon), ("render", render)):
                if not isinstance(value, dict):
                    errors.append(f"{tag} strict provenance requires {field}")
        elif not source_ref:
            warnings.append(f"{tag} has no source_ref; reverse traceability is unavailable")

        if isinstance(source_ref, dict):
            for field in ("script_hash", "narrative_ir_id", "narrative_ir_version", "scene_id", "beat_id"):
                if not source_ref.get(field):
                    errors.append(f"{tag} source_ref missing {field}")
            if source_ref.get("script_hash") and not SHA256_RE.fullmatch(str(source_ref["script_hash"])):
                errors.append(f"{tag} source_ref.script_hash is not SHA-256")
            if shot.get("scene_id") and source_ref.get("scene_id") != shot.get("scene_id"):
                errors.append(f"{tag} source_ref.scene_id differs from scene_id")
            if narrative:
                if source_ref.get("script_hash") != narrative_hash:
                    errors.append(f"{tag} script_hash does not match Narrative IR")
                if source_ref.get("narrative_ir_id") != narrative_id:
                    errors.append(f"{tag} narrative_ir_id does not match Narrative IR")
                if source_ref.get("scene_id") not in narrative_scenes:
                    errors.append(f"{tag} references unknown Narrative IR scene {source_ref.get('scene_id')}")

        if isinstance(canon, dict):
            if canon.get("plot_change_allowed") is not False:
                errors.append(f"{tag} canon.plot_change_allowed must be false")
            if canon.get("dialogue_policy") not in {"verbatim", "approved_changes_only"}:
                errors.append(f"{tag} invalid canon.dialogue_policy")
            if not isinstance(canon.get("approved_change_ids"), list):
                errors.append(f"{tag} canon.approved_change_ids must be an array")

        if isinstance(render, dict):
            duration = render.get("duration_seconds")
            if not isinstance(duration, (int, float)) or duration <= 0:
                errors.append(f"{tag} render.duration_seconds must be positive")
            else:
                total_duration += float(duration)
            if not render.get("adapter"):
                errors.append(f"{tag} render.adapter is required")

        if index == 1:
            if shot.get("previous_shot") not in {None, "", "NONE", "N/A"}:
                warnings.append(f"{tag} first shot should normally have previous_shot=NONE")
        else:
            if shot.get("previous_shot") != previous:
                errors.append(f"{tag} previous_shot={shot.get('previous_shot')} but prior shot is {previous}")
            adjacency = str(shot.get("adjacency_type", "")).upper()
            if previous_end is not None and shot.get("start_state") != previous_end and adjacency not in BREAK_TYPES:
                message = f"{tag} start_state differs from prior end_state without a break"
                (errors if strict_continuity else warnings).append(message)
            scene_id = shot.get("scene_id") or (source_ref or {}).get("scene_id")
            if previous_scene and scene_id != previous_scene and adjacency not in {"SCENE_BREAK", "TIME_JUMP"}:
                warnings.append(f"{tag} changes scene without SCENE_BREAK/TIME_JUMP")
        previous = shot_id
        previous_end = shot.get("end_state")
        previous_scene = shot.get("scene_id") or (source_ref or {}).get("scene_id")

    if target_duration is not None and abs(total_duration - target_duration) > 0.5:
        errors.append(f"total render duration {total_duration:.2f}s differs from target {target_duration:.2f}s")
    return errors, warnings


def main():
    parser = argparse.ArgumentParser(description="Validate Shot Contract / Shot IR JSON")
    parser.add_argument("path")
    parser.add_argument("--narrative-ir")
    parser.add_argument("--strict-provenance", action="store_true")
    parser.add_argument("--strict-continuity", action="store_true")
    parser.add_argument("--duration", type=float)
    args = parser.parse_args()
    narrative = json.loads(Path(args.narrative_ir).read_text(encoding="utf-8-sig")) if args.narrative_ir else None
    errors, warnings = validate(load_shots(args.path), narrative, args.strict_provenance, args.strict_continuity, args.duration)
    print("PASS" if not errors else "FAIL")
    for item in errors:
        print("ERROR:", item)
    for item in warnings:
        print("WARN:", item)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
