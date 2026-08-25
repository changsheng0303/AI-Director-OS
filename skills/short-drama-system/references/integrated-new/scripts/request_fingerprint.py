#!/usr/bin/env python3
"""Create auditable fingerprints for image or Dreamina request plans."""

from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
from pathlib import Path
from typing import Any


PATH_LIST_FIELDS = ("references", "referenceImages", "referenceVideos", "referenceAudio")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_record(raw: str, root: Path) -> dict[str, Any]:
    path = Path(raw).expanduser()
    if not path.is_absolute():
        path = (root / path).resolve()
    if not path.is_file():
        raise ValueError(f"referenced file does not exist: {path}")
    data = path.read_bytes()
    return {
        "path": str(path),
        "name": path.name,
        "size": len(data),
        "sha256": sha256_bytes(data),
    }


def prompt_value(item: dict[str, Any], root: Path) -> tuple[str, str | None]:
    inline = item.get("prompt")
    prompt_file = item.get("promptFile")
    if isinstance(inline, str) and inline.strip():
        if prompt_file:
            raise ValueError("request must use prompt or promptFile, not both")
        return inline, None
    if isinstance(prompt_file, str) and prompt_file.strip():
        path = Path(prompt_file).expanduser()
        if not path.is_absolute():
            path = (root / path).resolve()
        if not path.is_file():
            raise ValueError(f"promptFile does not exist: {path}")
        return path.read_text(encoding="utf-8"), str(path)
    raise ValueError("request is missing prompt or promptFile")


def fingerprint_request(item: dict[str, Any], root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    request_id = item.get("id")
    if not isinstance(request_id, str) or not request_id.strip():
        raise ValueError("every request needs a non-empty id")
    prompt, prompt_file = prompt_value(item, root)
    inputs: dict[str, list[dict[str, Any]]] = {}
    for field in PATH_LIST_FIELDS:
        values = item.get(field, [])
        if not isinstance(values, list) or not all(isinstance(value, str) for value in values):
            raise ValueError(f"{request_id}: {field} must be a list of file paths")
        inputs[field] = [file_record(value, root) for value in values]

    canonical = {
        key: value
        for key, value in item.items()
        if key not in {*PATH_LIST_FIELDS, "prompt", "promptFile"}
    }
    canonical["prompt"] = prompt
    canonical["inputs"] = inputs
    encoded = json.dumps(canonical, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    digest = sha256_bytes(encoded)
    summary = {
        "id": request_id,
        "backend": item.get("backend"),
        "command": item.get("command"),
        "model": item.get("model") or item.get("modelVersion"),
        "duration": item.get("duration"),
        "ratio": item.get("ratio"),
        "resolution": item.get("resolution"),
        "output": item.get("output") or item.get("outputDir"),
        "promptFile": prompt_file,
        "promptLength": len(prompt),
        "promptSha256": sha256_bytes(prompt.encode("utf-8")),
        "inputs": inputs,
        "requestFingerprint": digest,
    }
    return canonical, summary


def self_test() -> int:
    with tempfile.TemporaryDirectory(prefix="request-fingerprint-") as raw:
        root = Path(raw)
        reference = root / "reference.png"
        reference.write_bytes(b"first-version")
        item = {
            "id": "G001",
            "command": "multimodal2video",
            "modelVersion": "seedance2.0",
            "duration": 15,
            "prompt": "完整提示词",
            "referenceImages": [str(reference)],
        }
        _, first = fingerprint_request(item, root)
        reference.write_bytes(b"second-version")
        _, second = fingerprint_request(item, root)
        passed = first["requestFingerprint"] != second["requestFingerprint"]
        print(json.dumps({"status": "PASS" if passed else "FAILED", "fingerprintChangesWithInput": passed}, ensure_ascii=False, indent=2))
        return 0 if passed else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path, nargs="?")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    if args.plan is None:
        parser.error("plan is required unless --self-test is used")
    plan_path = args.plan.expanduser().resolve()
    try:
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
        if not isinstance(plan, dict):
            raise ValueError("plan root must be a JSON object")
        requests = plan.get("requests")
        if not isinstance(requests, list) or not requests:
            raise ValueError("plan requests must be a non-empty list")
        ids = [item.get("id") for item in requests if isinstance(item, dict)]
        if len(ids) != len(requests) or len(set(ids)) != len(ids):
            raise ValueError("request ids must be present and unique")

        canonical_requests: list[dict[str, Any]] = []
        summaries: list[dict[str, Any]] = []
        for item in requests:
            canonical, summary = fingerprint_request(item, plan_path.parent)
            canonical_requests.append(canonical)
            summaries.append(summary)
        canonical_plan = {
            key: value for key, value in plan.items() if key != "requests"
        }
        canonical_plan["requests"] = canonical_requests
        encoded = json.dumps(canonical_plan, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
        result = {
            "status": "SUCCESS",
            "plan": str(plan_path),
            "kind": plan.get("kind"),
            "project": plan.get("project"),
            "requestCount": len(summaries),
            "requests": summaries,
            "planFingerprint": sha256_bytes(encoded),
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        print(json.dumps({"status": "FAILED", "plan": str(plan_path), "error": str(exc)}, ensure_ascii=False, indent=2))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
