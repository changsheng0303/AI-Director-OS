#!/usr/bin/env python3
"""Validate runtime accounting and adjacency in a long-form H3 manifest."""

import argparse
import json
import os
import sys

STATE_KEYS = {"location", "subjects", "props", "light", "screen_direction", "action_state"}
SUBJECT_KEYS = {"zone", "facing", "pose", "action_phase"}
PROP_KEYS = {"holder", "zone", "state"}
METHODS = {"A_frame_linked", "B_shared_reference", "C_text_only"}
BRIDGES = {"action_match", "eyeline_match", "sound_bridge", "prop_match", "composition_match", "light_match", "scene_transition", "none"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest")
    parser.add_argument("--check-prompt-files", action="store_true")
    parser.add_argument("--require-asset-pack", action="store_true",
                        help="require existing visual_asset_pack.md and asset_binding.md entries")
    parser.add_argument("--strict-state-schema", action="store_true",
                        help="require subjects and props to use structured dictionaries")
    parser.add_argument("--require-audio-timeline", action="store_true",
                        help="require an existing audio_timeline_file")
    args = parser.parse_args()
    manifest_path = os.path.abspath(args.manifest)
    base = os.path.dirname(manifest_path)
    with open(manifest_path, encoding="utf-8") as handle:
        data = json.load(handle)

    errors, warnings = [], []
    segments = data.get("segments")
    target = data.get("target_runtime_sec")
    tolerance = float(data.get("timeline_tolerance_sec", 0.05))
    max_clip = float(data.get("max_generation_clip_sec", 15))
    if args.require_asset_pack:
        for key in ("asset_pack_file", "asset_ledger_file", "asset_binding_file", "asset_binding_json_file"):
            value = data.get(key)
            if not isinstance(value, str) or not value:
                errors.append(f"{key} is required when --require-asset-pack is used")
            elif not os.path.isfile(os.path.join(base, value)):
                errors.append(f"{key} not found: {value}")
    if args.require_audio_timeline:
        value = data.get("audio_timeline_file")
        if not isinstance(value, str) or not value:
            errors.append("audio_timeline_file is required when --require-audio-timeline is used")
        elif not os.path.isfile(os.path.join(base, value)):
            errors.append(f"audio_timeline_file not found: {value}")
    if not isinstance(target, (int, float)) or target <= 0:
        errors.append("target_runtime_sec must be a positive number")
    if not isinstance(segments, list) or not segments:
        errors.append("segments must be a non-empty list")
        segments = []

    seen_ids = set()
    previous = None
    for index, seg in enumerate(segments, start=1):
        sid = seg.get("segment_id", f"index-{index}")
        if sid in seen_ids:
            errors.append(f"{sid}: duplicate segment_id")
        seen_ids.add(sid)
        if seg.get("order") != index:
            errors.append(f"{sid}: order must equal {index}")

        start, end = seg.get("timeline_start_sec"), seg.get("timeline_end_sec")
        generation = seg.get("generation_duration_sec")
        numeric = all(isinstance(v, (int, float)) for v in (start, end, generation))
        if not numeric:
            errors.append(f"{sid}: timeline and generation durations must be numeric")
        else:
            if end <= start:
                errors.append(f"{sid}: timeline_end_sec must exceed timeline_start_sec")
            if generation <= 0 or generation > max_clip:
                errors.append(f"{sid}: generation_duration_sec must be within (0, {max_clip}]")
            if generation + tolerance < end - start:
                errors.append(f"{sid}: generation clip is shorter than timeline occupancy")

        method, bridge = seg.get("continuity_method"), seg.get("bridge_type")
        if method not in METHODS:
            errors.append(f"{sid}: illegal continuity_method {method!r}")
        if bridge not in BRIDGES:
            errors.append(f"{sid}: illegal bridge_type {bridge!r}")
        if bridge not in ("none", "scene_transition") and not seg.get("bridge_reason"):
            errors.append(f"{sid}: bridge_reason required for {bridge}")

        for state_name in ("start_state", "end_state"):
            state = seg.get(state_name)
            if not isinstance(state, dict):
                errors.append(f"{sid}: {state_name} must be an object")
            else:
                missing = sorted(STATE_KEYS - set(state))
                if missing:
                    errors.append(f"{sid}: {state_name} missing {', '.join(missing)}")
                if args.strict_state_schema:
                    subjects = state.get("subjects")
                    props = state.get("props")
                    if not isinstance(subjects, dict):
                        errors.append(f"{sid}: {state_name}.subjects must be an object")
                    else:
                        for asset_id, subject in subjects.items():
                            if not isinstance(subject, dict):
                                errors.append(f"{sid}: {state_name}.subjects.{asset_id} must be an object")
                                continue
                            missing_subject = sorted(SUBJECT_KEYS - set(subject))
                            if missing_subject:
                                errors.append(f"{sid}: {state_name}.subjects.{asset_id} missing {', '.join(missing_subject)}")
                    if not isinstance(props, dict):
                        errors.append(f"{sid}: {state_name}.props must be an object")
                    else:
                        for asset_id, prop in props.items():
                            if not isinstance(prop, dict):
                                errors.append(f"{sid}: {state_name}.props.{asset_id} must be an object")
                                continue
                            missing_prop = sorted(PROP_KEYS - set(prop))
                            if missing_prop:
                                errors.append(f"{sid}: {state_name}.props.{asset_id} missing {', '.join(missing_prop)}")

        prompt_file = seg.get("prompt_file")
        if not prompt_file:
            errors.append(f"{sid}: prompt_file is required")
        elif args.check_prompt_files and not os.path.isfile(os.path.join(base, prompt_file)):
            errors.append(f"{sid}: prompt_file not found: {prompt_file}")

        if previous is not None and numeric:
            prior_id = previous.get("segment_id")
            prior_end = previous.get("timeline_end_sec")
            if isinstance(prior_end, (int, float)) and abs(start - prior_end) > tolerance:
                errors.append(f"{prior_id} -> {sid}: timeline gap/overlap {start - prior_end:.3f}s")
            same_scene = previous.get("scene_id") == seg.get("scene_id")
            transition = bridge == "scene_transition"
            if same_scene and transition:
                warnings.append(f"{prior_id} -> {sid}: scene_transition used inside same scene")
            if not same_scene and not transition:
                errors.append(f"{prior_id} -> {sid}: scene change requires scene_transition")
            if same_scene and not transition:
                prior_state, next_state = previous.get("end_state", {}), seg.get("start_state", {})
                for key in STATE_KEYS:
                    if prior_state.get(key) != next_state.get(key):
                        errors.append(f"{prior_id} -> {sid}: {key} mismatch between END and START")
            if method == "A_frame_linked":
                expected = f"{prior_id}:end_frame"
                if expected not in seg.get("reference_assets", []):
                    errors.append(f"{sid}: A_frame_linked requires {expected}")
        previous = seg

    if segments and isinstance(target, (int, float)):
        first_start = segments[0].get("timeline_start_sec")
        last_end = segments[-1].get("timeline_end_sec")
        if isinstance(first_start, (int, float)) and abs(first_start) > tolerance:
            errors.append(f"timeline must start at 0, got {first_start}")
        if isinstance(last_end, (int, float)) and abs(last_end - target) > tolerance:
            errors.append(f"timeline ends at {last_end}, target is {target}")

    for warning in warnings:
        print(f"[WARNING] {warning}")
    for error in errors:
        print(f"[ERROR] {error}")
    if errors:
        print(f"FAIL: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"PASS: {len(segments)} segments, runtime={target}s, warnings={len(warnings)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
