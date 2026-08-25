#!/usr/bin/env python3
"""Compute artifact changes, canon violations, and downstream invalidation.

The script is read-only. It prints a deterministic plan and never rewrites the
project state file. A caller may persist the plan after review.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict, deque
from pathlib import Path


def _registry(state, label, errors):
    items = state.get("artifact_registry")
    if not isinstance(items, list):
        errors.append(f"{label}.artifact_registry must be an array")
        return {}
    result = {}
    for index, item in enumerate(items, 1):
        if not isinstance(item, dict) or not item.get("artifact_id"):
            errors.append(f"{label}.artifact_registry[{index}] missing artifact_id")
            continue
        artifact_id = item["artifact_id"]
        if artifact_id in result:
            errors.append(f"{label}: duplicate artifact_id {artifact_id}")
        result[artifact_id] = item
    return result


def diff(before, after):
    errors, warnings = [], []
    old = _registry(before, "before", errors)
    new = _registry(after, "after", errors)
    approved_requests = [
        item for item in after.get("change_requests", [])
        if isinstance(item, dict) and item.get("status") in {"approved", "applied"}
    ]
    approved = {item.get("change_id") for item in approved_requests}
    approved_scopes = {scope for item in approved_requests for scope in item.get("scope", [])}

    added = sorted(set(new) - set(old))
    removed = sorted(set(old) - set(new))
    for artifact_id in removed:
        if old[artifact_id].get("canon_locked") and artifact_id not in approved_scopes:
            errors.append(f"CANON_VIOLATION {artifact_id}: locked artifact removed without an approved change request")
    changed = []
    for artifact_id in sorted(set(old) & set(new)):
        left, right = old[artifact_id], new[artifact_id]
        if any(left.get(key) != right.get(key) for key in ("content_hash", "version", "parents")):
            changed.append(artifact_id)
            if left.get("canon_locked") and left.get("content_hash") != right.get("content_hash"):
                change_id = right.get("approved_change_id")
                if not change_id or change_id not in approved:
                    errors.append(f"CANON_VIOLATION {artifact_id}: content changed without an approved change request")

    children = defaultdict(set)
    for item in list(old.values()) + list(new.values()):
        for parent in item.get("parents", []):
            children[parent].add(item["artifact_id"])

    roots = set(changed) | set(removed)
    affected = set()
    queue = deque(roots)
    while queue:
        parent = queue.popleft()
        for child in children.get(parent, set()):
            if child not in affected and child not in roots:
                affected.add(child)
                queue.append(child)

    invalidated, rebuilt, missing_invalidation = [], [], []
    for artifact_id in sorted(affected):
        current = new.get(artifact_id)
        if current is None:
            continue
        prior = old.get(artifact_id)
        if current.get("status") == "INVALIDATED":
            invalidated.append(artifact_id)
        elif prior and current.get("content_hash") != prior.get("content_hash") and current.get("version") != prior.get("version"):
            rebuilt.append(artifact_id)
        else:
            missing_invalidation.append(artifact_id)
            errors.append(f"INVALIDATION_MISSING {artifact_id}: depends on a changed artifact but is neither rebuilt nor INVALIDATED")

    for artifact_id, item in new.items():
        for parent in item.get("parents", []):
            if parent not in new:
                warnings.append(f"artifact {artifact_id}: parent {parent} is absent from after-state")

    plan = {
        "status": "FAIL" if errors else "PASS",
        "added": added,
        "removed": removed,
        "changed": changed,
        "affected": sorted(affected),
        "invalidated": invalidated,
        "rebuilt": rebuilt,
        "missing_invalidation": missing_invalidation,
        "errors": errors,
        "warnings": warnings,
    }
    return plan


def main():
    parser = argparse.ArgumentParser(description="Compute project artifact diff and invalidation plan")
    parser.add_argument("before")
    parser.add_argument("after")
    parser.add_argument("--output")
    args = parser.parse_args()
    before = json.loads(Path(args.before).read_text(encoding="utf-8-sig"))
    after = json.loads(Path(args.after).read_text(encoding="utf-8-sig"))
    plan = diff(before, after)
    rendered = json.dumps(plan, ensure_ascii=False, indent=2)
    print(rendered)
    if args.output:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")
    return 0 if plan["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
