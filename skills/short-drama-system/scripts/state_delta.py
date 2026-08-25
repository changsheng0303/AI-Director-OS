#!/usr/bin/env python3
"""Compute runtime-state deltas without calling an LLM or rewriting project files."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


MISSING = object()


def walk(before, after, prefix=""):
    changes = []
    if isinstance(before, dict) and isinstance(after, dict):
        for key in sorted(set(before) | set(after)):
            path = f"{prefix}.{key}" if prefix else key
            left = before.get(key, MISSING)
            right = after.get(key, MISSING)
            if left is MISSING:
                changes.append({"path": path, "operation": "add", "before": None, "after": right})
            elif right is MISSING:
                changes.append({"path": path, "operation": "remove", "before": left, "after": None})
            else:
                changes.extend(walk(left, right, path))
    elif before != after:
        changes.append({"path": prefix, "operation": "replace", "before": before, "after": after})
    return changes


def runtime(data):
    return data.get("runtime_state", data) if isinstance(data, dict) else data


def main():
    parser = argparse.ArgumentParser(description="Compute machine runtime-state delta")
    parser.add_argument("before")
    parser.add_argument("after")
    parser.add_argument("--output")
    args = parser.parse_args()
    before = json.loads(Path(args.before).read_text(encoding="utf-8-sig"))
    after = json.loads(Path(args.after).read_text(encoding="utf-8-sig"))
    changes = walk(runtime(before), runtime(after), "runtime_state")
    result = {"status": "PASS", "change_count": len(changes), "changes": changes}
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    print(rendered)
    if args.output:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
