#!/usr/bin/env python3
"""Regression tests for the simplified production base."""

from __future__ import annotations

import copy
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_simple_project.py"
EXAMPLES = ROOT / "examples"


def run(name, expected, *args):
    result = subprocess.run([sys.executable, str(VALIDATOR), *map(str, args)], capture_output=True, text=True, encoding="utf-8", env={**os.environ, "PYTHONUTF8": "1"})
    if result.returncode != expected:
        print(f"FAIL {name}: expected {expected}, got {result.returncode}")
        print(result.stdout)
        print(result.stderr)
        return False
    print(f"PASS {name}")
    return True


def run_data(name, expected, data):
    with tempfile.TemporaryDirectory(prefix="simple-project-test-") as temp_dir:
        path = Path(temp_dir) / "project.json"
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return run(name, expected, path)


def main():
    base = json.loads((EXAMPLES / "simple-project-valid.json").read_text(encoding="utf-8"))
    advanced = copy.deepcopy(base)
    advanced["canon_lite"]["fact_basis"] = [
        {"fact_id": "F01", "value": "包裹中是照片证据", "authority": "source_evidence", "evidence": "照片从裂口露出"}
    ]
    advanced["story_map"]["scenes"][0]["beats"] = [
        {"beat_id": "B01", "kind": "action", "summary": "包裹勾住栏杆"},
        {"beat_id": "B02", "kind": "dialogue", "summary": "林决定提交证据", "dialogue_id": "D001"},
    ]
    advanced["shots"][0].update({"beat_refs": ["B01"], "segment_id": "SEG01", "cut_motivation": "scene_entry"})
    advanced["shots"][1].update({
        "beat_refs": ["B02"],
        "segment_id": "SEG01",
        "cut_motivation": "information_change",
        "performance_direction": "逼对方承认事实；谎言构成阻碍；先回避再施压；停下手中动作后才说出原台词",
    })
    advanced["assets"][1].update({"anchors": ["破损棕纸", "露出的照片角"], "states": ["密封", "破损"], "scale": "hand"})
    advanced["revision_log"] = [
        {
            "revision_id": "REV01",
            "changed_layer": "project-script",
            "summary": "修正照片证据的出现位置",
            "affected_ids": ["SC01", "S02"],
            "status": "confirmed",
        }
    ]
    advanced["stale_outputs"] = [
        {
            "output_id": "PJ01",
            "source_revision_id": "REV01",
            "reason": "提示词仍引用旧版证据位置",
            "status": "possibly-stale",
        }
    ]

    broken_advanced = copy.deepcopy(advanced)
    broken_advanced["canon_lite"]["fact_basis"][0]["evidence"] = ""
    broken_advanced["shots"][1]["beat_refs"] = ["B01"]
    broken_advanced["shots"][1]["cut_motivation"] = "timer_target"
    broken_advanced["assets"][1]["anchors"] = ["唯一锚点"]
    broken_advanced["assets"][1]["variant_of"] = "AS404"
    broken_advanced["shots"][1]["performance_direction"] = ""
    broken_advanced["stale_outputs"][0]["source_revision_id"] = "REV404"

    checks = [
        run("simple-valid", 0, EXAMPLES / "simple-project-valid.json", "--duration", "6"),
        run("simple-invalid", 1, EXAMPLES / "simple-project-invalid.json"),
        run_data("advanced-valid", 0, advanced),
        run_data("advanced-invalid", 1, broken_advanced),
    ]
    context = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "select_relevant_context.py"), str(EXAMPLES / "simple-project-valid.json"), "--scene", "SC01"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        env={**os.environ, "PYTHONUTF8": "1"},
    )
    try:
        view = json.loads(context.stdout)
        context_ok = context.returncode == 0 and view["scene_contract"]["scene_id"] == "SC01" and set(view["runtime_state"]["characters"]) == {"林"}
    except (json.JSONDecodeError, KeyError):
        context_ok = False
    checks.append(context_ok)
    print("PASS context-selector" if context_ok else "FAIL context-selector")

    delta = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "state_delta.py"), str(EXAMPLES / "simple-project-valid.json"), str(EXAMPLES / "simple-project-state-after.json")],
        capture_output=True,
        text=True,
        encoding="utf-8",
        env={**os.environ, "PYTHONUTF8": "1"},
    )
    try:
        delta_data = json.loads(delta.stdout)
        delta_ok = delta.returncode == 0 and delta_data["change_count"] == 5
    except (json.JSONDecodeError, KeyError):
        delta_ok = False
    checks.append(delta_ok)
    print("PASS state-delta" if delta_ok else "FAIL state-delta")
    if all(checks):
        print("SIMPLE_PROJECT_REGRESSION_PASS")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
