#!/usr/bin/env python3
"""Validate asset ledger and per-segment bindings against a continuity manifest."""

import argparse
import json
import os
import sys

ASSET_TYPES = {"character", "scene", "prop", "style", "atmosphere"}
APPROVALS = {"draft", "user_approved", "replaced"}
METHODS = {"A_frame_linked", "B_shared_reference", "C_text_only"}


def load(path):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("asset_ledger")
    parser.add_argument("asset_binding")
    parser.add_argument("manifest")
    parser.add_argument("--check-reference-files", action="store_true")
    args = parser.parse_args()

    ledger_path = os.path.abspath(args.asset_ledger)
    base = os.path.dirname(ledger_path)
    ledger = load(ledger_path)
    binding = load(args.asset_binding)
    manifest = load(args.manifest)
    errors = []

    assets = ledger.get("assets")
    bindings = binding.get("bindings")
    segments = manifest.get("segments")
    if not isinstance(assets, list):
        errors.append("asset ledger must contain an assets list")
        assets = []
    if not isinstance(bindings, list):
        errors.append("asset binding must contain a bindings list")
        bindings = []
    if not isinstance(segments, list):
        errors.append("manifest must contain a segments list")
        segments = []

    asset_map = {}
    for asset in assets:
        aid = asset.get("asset_id")
        if not aid or aid in asset_map:
            errors.append(f"invalid or duplicate asset_id: {aid!r}")
            continue
        asset_map[aid] = asset
        if asset.get("type") not in ASSET_TYPES:
            errors.append(f"{aid}: illegal type {asset.get('type')!r}")
        if asset.get("approval_status") not in APPROVALS:
            errors.append(f"{aid}: illegal approval_status {asset.get('approval_status')!r}")
        if not str(asset.get("master_prompt", "")).strip():
            errors.append(f"{aid}: master_prompt is required")
        ref = asset.get("reference_file")
        if args.check_reference_files and ref and not os.path.isfile(os.path.join(base, ref)):
            errors.append(f"{aid}: reference_file not found: {ref}")

    segment_map = {s.get("segment_id"): s for s in segments if s.get("segment_id")}
    binding_map = {}
    for row in bindings:
        sid = row.get("segment_id")
        if not sid or sid in binding_map:
            errors.append(f"invalid or duplicate binding segment_id: {sid!r}")
            continue
        binding_map[sid] = row
        if sid not in segment_map:
            errors.append(f"{sid}: binding has no matching manifest segment")
        method = row.get("continuity_use")
        if method not in METHODS:
            errors.append(f"{sid}: illegal continuity_use {method!r}")
        required = row.get("required_assets")
        if not isinstance(required, list):
            errors.append(f"{sid}: required_assets must be a list")
            required = []
        for aid in required:
            if aid not in asset_map:
                errors.append(f"{sid}: unknown asset {aid}")
                continue
            asset = asset_map[aid]
            if method in {"A_frame_linked", "B_shared_reference"}:
                if asset.get("approval_status") != "user_approved":
                    errors.append(f"{sid}: {method} requires approved asset {aid}")
                if not asset.get("reference_file"):
                    errors.append(f"{sid}: {method} requires reference_file for {aid}")

        manifest_required = segment_map.get(sid, {}).get("required_assets", [])
        if sorted(required) != sorted(manifest_required):
            errors.append(f"{sid}: binding assets differ from manifest required_assets")
        manifest_method = segment_map.get(sid, {}).get("continuity_method")
        if manifest_method and method != manifest_method:
            errors.append(f"{sid}: continuity_use differs from manifest continuity_method")

    missing_bindings = sorted(set(segment_map) - set(binding_map))
    if missing_bindings:
        errors.append(f"segments missing asset bindings: {missing_bindings}")

    for error in errors:
        print(f"[ERROR] {error}")
    if errors:
        print(f"FAIL: {len(errors)} error(s)")
        return 1
    print(f"PASS: {len(asset_map)} assets, {len(binding_map)} segment bindings")
    return 0


if __name__ == "__main__":
    sys.exit(main())
