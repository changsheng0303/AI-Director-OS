#!/usr/bin/env python3
"""Validate the JSONL production failure registry with no dependencies."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from datetime import date
from pathlib import Path


REQUIRED = {"id", "date", "project_id", "stage", "evidence_type", "signature", "severity", "observed_failure", "evidence", "root_cause", "repair", "regression_target", "status", "occurrences"}
STAGES = {"foundation", "screenplay", "storyboard", "asset", "video_prompt", "generation", "editing", "delivery"}
EVIDENCE = {"source_logic", "validator_failure", "user_feedback", "generation_output"}
SEVERITY = {"critical", "major", "minor"}
STATUS = {"observed", "documented", "candidate", "covered", "needs_generation_proof"}


def validate(path: Path):
    errors, records, ids = [], [], set()
    for line_number, raw in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            record = json.loads(raw)
        except json.JSONDecodeError as exc:
            errors.append(f"line {line_number}: invalid JSON: {exc.msg}")
            continue
        if not isinstance(record, dict):
            errors.append(f"line {line_number}: record must be an object")
            continue
        missing = sorted(REQUIRED - set(record))
        if missing:
            errors.append(f"line {line_number}: missing {', '.join(missing)}")
        record_id = record.get("id")
        if not isinstance(record_id, str) or not re.fullmatch(r"FAIL-[0-9]{8}-[0-9]{3}", record_id):
            errors.append(f"line {line_number}: invalid id {record_id}")
        elif record_id in ids:
            errors.append(f"line {line_number}: duplicate id {record_id}")
        ids.add(record_id)
        try:
            date.fromisoformat(str(record.get("date", "")))
        except ValueError:
            errors.append(f"line {line_number}: invalid date {record.get('date')}")
        for key, allowed in (("stage", STAGES), ("evidence_type", EVIDENCE), ("severity", SEVERITY), ("status", STATUS)):
            if record.get(key) not in allowed:
                errors.append(f"line {line_number}: invalid {key} {record.get(key)}")
        if not re.fullmatch(r"[a-z0-9_]+", str(record.get("signature", ""))):
            errors.append(f"line {line_number}: invalid signature")
        if not isinstance(record.get("occurrences"), int) or record.get("occurrences", 0) < 1:
            errors.append(f"line {line_number}: occurrences must be a positive integer")
        for key in ("project_id", "observed_failure", "evidence", "root_cause", "repair"):
            if not str(record.get(key, "")).strip():
                errors.append(f"line {line_number}: empty {key}")
        if record.get("evidence_type") == "generation_output" and not str(record.get("artifact_path", "")).strip():
            errors.append(f"line {line_number}: generation_output requires artifact_path")
        if record.get("status") == "covered" and not str(record.get("regression_target", "")).strip():
            errors.append(f"line {line_number}: covered record requires regression_target")
        records.append(record)
    return errors, records


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    if not args.path.is_file():
        print(f"FAIL: file not found: {args.path}")
        return 1
    errors, records = validate(args.path)
    print("PASS" if not errors else "FAIL")
    for error in errors:
        print("ERROR:", error)
    if args.summary:
        print(f"records={len(records)}")
        for label, key in (("stage", "stage"), ("evidence", "evidence_type"), ("status", "status")):
            counts = Counter(str(record.get(key)) for record in records)
            print(label + "=" + ",".join(f"{name}:{count}" for name, count in sorted(counts.items())))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
