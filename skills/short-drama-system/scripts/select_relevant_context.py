#!/usr/bin/env python3
"""Project a compact scene-specific context view from simple-project.json."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def indexed(items, key):
    return {item[key]: item for item in items if isinstance(item, dict) and item.get(key)}


def select(project, scene_id):
    canon = project.get("canon_lite", {})
    story = project.get("story_map", {})
    scenes = indexed(story.get("scenes", []), "scene_id")
    if scene_id not in scenes:
        raise ValueError(f"unknown scene_id {scene_id}")
    scene = scenes[scene_id]
    events = indexed(canon.get("locked_events", []), "event_id")
    dialogue = indexed(canon.get("locked_dialogue", []), "dialogue_id")
    assets = indexed(project.get("assets", []), "asset_id")
    runtime = project.get("runtime_state", {})
    state_refs = scene.get("state_refs", [])
    view = {
        "context_version": "1.0",
        "project_id": project.get("project_id"),
        "canon_version": canon.get("version"),
        "story": {
            "premise": story.get("premise"),
            "protagonist": story.get("protagonist"),
            "conflict": story.get("conflict"),
            "emotional_change": story.get("emotional_change"),
        },
        "scene_contract": scene,
        "required_events": [events[item] for item in scene.get("required_events", []) if item in events],
        "dialogue": [dialogue[item] for item in scene.get("dialogue_ids", []) if item in dialogue],
        "runtime_state": {
            "characters": {item: runtime.get("characters", {}).get(item) for item in state_refs if item in runtime.get("characters", {})},
            "props": {item: runtime.get("props", {}).get(item) for item in state_refs if item in runtime.get("props", {})},
            "scene": runtime.get("scene", {}),
        },
        "assets": [assets[item] for item in scene.get("asset_refs", []) if item in assets],
        "shots": [item for item in project.get("shots", []) if item.get("source_scene") == scene_id],
        "prohibited_changes": canon.get("prohibited_changes", []),
    }
    return view


def main():
    parser = argparse.ArgumentParser(description="Select a compact Relevant Context View")
    parser.add_argument("path")
    parser.add_argument("--scene", required=True)
    parser.add_argument("--output")
    args = parser.parse_args()
    project = json.loads(Path(args.path).read_text(encoding="utf-8-sig"))
    try:
        view = select(project, args.scene)
    except ValueError as error:
        print("FAIL")
        print("ERROR:", error)
        return 1
    rendered = json.dumps(view, ensure_ascii=False, indent=2)
    print(rendered)
    if args.output:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
