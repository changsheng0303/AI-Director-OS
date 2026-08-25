#!/usr/bin/env python3
"""Validate the simplified production contract with no external dependencies."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


STEP_ORDER = ["project-script", "review", "storyboard", "visual", "video", "delivery"]


def unique(items, key, label, errors):
    result = {}
    for index, item in enumerate(items, 1):
        value = item.get(key) if isinstance(item, dict) else None
        if not value:
            errors.append(f"{label}[{index}] missing {key}")
            continue
        if value in result:
            errors.append(f"duplicate {label} {value}")
        result[value] = item
    return result


def validate(data, target_duration=None):
    errors, warnings = [], []
    required = {"schema_version", "project_id", "title", "current_step", "canon_lite", "story_map", "runtime_state", "shots", "assets", "prompt_jobs", "warnings"}
    if not isinstance(data, dict):
        return ["root must be an object"], []
    missing = sorted(required - set(data))
    if missing:
        errors.append("missing top-level fields: " + ", ".join(missing))
    if data.get("schema_version") != "1.1":
        errors.append("schema_version must be 1.1")
    step = data.get("current_step")
    if step not in STEP_ORDER:
        errors.append(f"invalid current_step {step}")
        step_index = -1
    else:
        step_index = STEP_ORDER.index(step)

    canon = data.get("canon_lite", {})
    facts = unique(canon.get("fact_basis", []), "fact_id", "fact", errors)
    fact_authorities = {"user_locked", "source_evidence", "ai_proposal", "open_noncritical"}
    for fact_id, fact in facts.items():
        if not str(fact.get("value", "")).strip():
            errors.append(f"fact {fact_id} has empty value")
        authority = fact.get("authority")
        if authority not in fact_authorities:
            errors.append(f"fact {fact_id} has invalid authority {authority}")
        if authority == "source_evidence" and not str(fact.get("evidence", "")).strip():
            errors.append(f"fact {fact_id} marked source_evidence without evidence")
    events = unique(canon.get("locked_events", []), "event_id", "event", errors)
    dialogue = unique(canon.get("locked_dialogue", []), "dialogue_id", "dialogue", errors)
    for dialogue_id, line in dialogue.items():
        if not str(line.get("text", "")).strip():
            errors.append(f"dialogue {dialogue_id} has empty text")

    story = data.get("story_map", {})
    scenes = unique(story.get("scenes", []), "scene_id", "scene", errors)
    assets = unique(data.get("assets", []), "asset_id", "asset", errors)
    beat_owner = {}
    scene_beat_order = {}
    runtime = data.get("runtime_state", {})
    character_state = runtime.get("characters", {}) if isinstance(runtime, dict) else {}
    prop_state = runtime.get("props", {}) if isinstance(runtime, dict) else {}
    locked_characters = set(canon.get("locked_characters", []))
    for scene_id, scene in scenes.items():
        scene_beat_order[scene_id] = []
        local_beats = unique(scene.get("beats", []), "beat_id", f"scene {scene_id} beat", errors)
        for beat_id, beat in local_beats.items():
            if beat_id in beat_owner:
                errors.append(f"duplicate beat {beat_id} across scenes")
            beat_owner[beat_id] = scene_id
            scene_beat_order[scene_id].append(beat_id)
            if beat.get("kind") not in {"action", "dialogue", "event", "transition"}:
                errors.append(f"beat {beat_id} has invalid kind {beat.get('kind')}")
            if not str(beat.get("summary", "")).strip():
                errors.append(f"beat {beat_id} has empty summary")
            dialogue_id = beat.get("dialogue_id")
            if dialogue_id and dialogue_id not in dialogue:
                errors.append(f"beat {beat_id} references unknown dialogue {dialogue_id}")
        for event_id in scene.get("required_events", []):
            if event_id not in events:
                errors.append(f"scene {scene_id} references unknown event {event_id}")
        for dialogue_id in scene.get("dialogue_ids", []):
            if dialogue_id not in dialogue:
                errors.append(f"scene {scene_id} references unknown dialogue {dialogue_id}")
        for character_id in scene.get("characters", []):
            if character_id not in locked_characters:
                errors.append(f"scene {scene_id} references character outside Canon-lite: {character_id}")
        for asset_id in scene.get("asset_refs", []):
            if asset_id not in assets:
                errors.append(f"scene {scene_id} references unknown asset {asset_id}")
        for state_id in scene.get("state_refs", []):
            if state_id not in character_state and state_id not in prop_state:
                errors.append(f"scene {scene_id} references unknown runtime state {state_id}")

    asset_scales = {"hand", "desktop", "furniture", "environment"}
    for asset_id, asset in assets.items():
        anchors = asset.get("anchors")
        if anchors is not None:
            if not isinstance(anchors, list) or not 2 <= len(anchors) <= 5:
                errors.append(f"asset {asset_id} anchors must contain 2 to 5 items")
            elif any(not str(item).strip() for item in anchors):
                errors.append(f"asset {asset_id} has an empty anchor")
            elif len(set(anchors)) != len(anchors):
                errors.append(f"asset {asset_id} has duplicate anchors")
        states = asset.get("states")
        if states is not None:
            if not isinstance(states, list) or any(not str(item).strip() for item in states):
                errors.append(f"asset {asset_id} states must be non-empty strings")
            elif len(set(states)) != len(states):
                errors.append(f"asset {asset_id} has duplicate states")
        scale = asset.get("scale")
        if scale is not None and scale not in asset_scales:
            errors.append(f"asset {asset_id} has invalid scale {scale}")
        parent_id = asset.get("variant_of")
        if parent_id:
            if parent_id == asset_id:
                errors.append(f"asset {asset_id} cannot be a variant of itself")
            elif parent_id not in assets:
                errors.append(f"asset {asset_id} references unknown variant parent {parent_id}")
            elif assets[parent_id].get("type") != asset.get("type"):
                errors.append(f"asset {asset_id} variant parent must have the same type")
    shots = unique(data.get("shots", []), "shot_id", "shot", errors)

    total = 0.0
    previous_end = None
    previous_source_scene = None
    claimed_by_scene = {scene_id: [] for scene_id in scenes}
    segment_scenes = {}
    closed_segments = set()
    active_segment = None
    for shot_id, shot in shots.items():
        source_scene = shot.get("source_scene")
        if source_scene not in scenes:
            errors.append(f"shot {shot_id} references unknown scene {source_scene}")
        duration = shot.get("duration_seconds")
        if not isinstance(duration, (int, float)) or duration <= 0:
            errors.append(f"shot {shot_id} duration must be positive")
        else:
            total += float(duration)
        for dialogue_id in shot.get("dialogue_ids", []):
            if dialogue_id not in dialogue:
                errors.append(f"shot {shot_id} references unknown dialogue {dialogue_id}")
        for asset_id in shot.get("asset_refs", []):
            if asset_id not in assets:
                errors.append(f"shot {shot_id} references unknown asset {asset_id}")
        beat_refs = shot.get("beat_refs", [])
        if len(set(beat_refs)) != len(beat_refs):
            errors.append(f"shot {shot_id} has duplicate beat_refs")
        for beat_id in beat_refs:
            if beat_id not in beat_owner:
                errors.append(f"shot {shot_id} references unknown beat {beat_id}")
            elif beat_owner[beat_id] != source_scene:
                errors.append(f"shot {shot_id} claims beat {beat_id} from another scene")
            elif source_scene in claimed_by_scene:
                claimed_by_scene[source_scene].append(beat_id)
        segment_id = shot.get("segment_id")
        if segment_id:
            if active_segment is not None and segment_id != active_segment:
                closed_segments.add(active_segment)
            if segment_id in closed_segments:
                errors.append(f"segment {segment_id} is not contiguous")
            active_segment = segment_id
            previous_scene = segment_scenes.setdefault(segment_id, source_scene)
            if previous_scene != source_scene:
                errors.append(f"segment {segment_id} crosses scenes")
        elif active_segment is not None:
            closed_segments.add(active_segment)
            active_segment = None
        cut_motivation = shot.get("cut_motivation")
        valid_cut_motivations = {"scene_entry", "emotion_change", "information_change", "subject_change", "action_phase_change", "eyeline_or_viewpoint_change"}
        if cut_motivation is not None and cut_motivation not in valid_cut_motivations:
            errors.append(f"shot {shot_id} has invalid cut_motivation {cut_motivation}")
        if previous_source_scene == source_scene and not cut_motivation:
            warnings.append(f"shot {shot_id} has no cut_motivation; do not cut only to meet the 3-4s average")
        if previous_source_scene != source_scene and cut_motivation not in {None, "scene_entry"}:
            warnings.append(f"shot {shot_id} starts a scene but cut_motivation is {cut_motivation}, not scene_entry")
        if previous_end is not None and shot.get("start_state") and shot.get("start_state") != previous_end:
            warnings.append(f"shot {shot_id} start_state differs from previous end_state")
        previous_end = shot.get("end_state")
        previous_source_scene = source_scene

    enforce_beat_coverage = step_index >= STEP_ORDER.index("storyboard") or any(shot.get("beat_refs") for shot in shots.values())
    if enforce_beat_coverage:
        for scene_id, expected in scene_beat_order.items():
            if not expected:
                continue
            actual = claimed_by_scene.get(scene_id, [])
            if actual != expected:
                missing = [beat_id for beat_id in expected if beat_id not in actual]
                duplicates = sorted({beat_id for beat_id in actual if actual.count(beat_id) > 1})
                details = []
                if missing:
                    details.append("missing " + ", ".join(missing))
                if duplicates:
                    details.append("duplicated " + ", ".join(duplicates))
                if not missing and not duplicates:
                    details.append("out of source order")
                errors.append(f"scene {scene_id} beat coverage mismatch: " + "; ".join(details))

    if target_duration is not None and abs(total - target_duration) > 0.5:
        errors.append(f"duration {total:.2f}s differs from target {target_duration:.2f}s")
    if shots:
        average_shot_seconds = total / len(shots)
        if average_shot_seconds < 3 or average_shot_seconds > 4:
            warnings.append(
                f"average shot duration is {average_shot_seconds:.2f}s; default short-form target is 3-4s, "
                "but revise only when a real emotion/information/subject/action-phase/eyeline change supports the cut"
            )
    if step_index >= STEP_ORDER.index("storyboard") and not shots:
        errors.append("storyboard or later step requires shots")

    prompt_jobs = unique(data.get("prompt_jobs", []), "job_id", "prompt_job", errors)
    for job_id, job in prompt_jobs.items():
        for shot_id in job.get("shot_ids", []):
            if shot_id not in shots:
                errors.append(f"prompt job {job_id} references unknown shot {shot_id}")
    if step_index >= STEP_ORDER.index("video") and not prompt_jobs:
        errors.append("video or delivery step requires prompt_jobs")

    return errors, warnings


def main():
    parser = argparse.ArgumentParser(description="Validate Simple Short Film Production Contract")
    parser.add_argument("path")
    parser.add_argument("--duration", type=float)
    args = parser.parse_args()
    data = json.loads(Path(args.path).read_text(encoding="utf-8-sig"))
    errors, warnings = validate(data, args.duration)
    print("PASS" if not errors else "FAIL")
    for item in errors:
        print("ERROR:", item)
    for item in warnings:
        print("WARN:", item)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
