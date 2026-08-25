#!/usr/bin/env python3
"""Create the machine-readable S-1B handoff and canonical SHA-256 hash."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

from validate_ip_foundation import validate


def canonical_hash(data):
    encoded = json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def build(package):
    errors, warnings = validate(package)
    if errors:
        raise ValueError("Foundation validation failed: " + "; ".join(errors))
    if package.get("audit", {}).get("status") != "FOUNDATION_LOCKED" or package.get("canon", {}).get("locked") is not True:
        raise ValueError("Foundation must be FOUNDATION_LOCKED before handoff")
    entities = package.get("entities", [])
    rules = [item["entity_id"] for item in entities if item.get("entity_type") == "rule"]
    return {
        "artifact_id": package["foundation_id"],
        "artifact_type": "ip_foundation",
        "version": package["foundation_version"],
        "content_hash": canonical_hash(package),
        "status": "LOCKED",
        "canon_locked": True,
        "parents": [],
        "locked_fact_ids": package["canon"]["locked_fact_ids"],
        "locked_entity_ids": [item["entity_id"] for item in entities],
        "locked_rule_ids": rules,
        "cast_manifest": package.get("cast", {}),
        "relationship_graph": package.get("relationships", []),
        "allowed_story_scope": package.get("constraints", {}).get("allowed_story_scope", []),
        "prohibited_assumptions": package.get("constraints", {}).get("prohibited_assumptions", []),
        "open_noncritical_questions": package.get("canon", {}).get("open_noncritical_questions", []),
        "warnings": warnings,
    }


def main():
    parser = argparse.ArgumentParser(description="Build an IP Foundation handoff contract")
    parser.add_argument("path")
    parser.add_argument("--output")
    args = parser.parse_args()
    package = json.loads(Path(args.path).read_text(encoding="utf-8-sig"))
    try:
        handoff = build(package)
    except ValueError as error:
        print("FAIL")
        print("ERROR:", error)
        return 1
    rendered = json.dumps(handoff, ensure_ascii=False, indent=2)
    print(rendered)
    if args.output:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
