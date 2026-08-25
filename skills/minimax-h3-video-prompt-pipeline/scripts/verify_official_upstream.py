#!/usr/bin/env python3
"""Verify that the installed official H3 skill matches the recorded raw hashes."""

import argparse
import hashlib
import json
import os
import sys


def sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("lock_file")
    args = parser.parse_args()
    with open(args.lock_file, encoding="utf-8") as handle:
        lock = json.load(handle)

    root = lock.get("installed_path")
    hashes = lock.get("raw_sha256", {})
    errors = []
    for relative, expected in hashes.items():
        path = os.path.join(root, *relative.split("/"))
        if not os.path.isfile(path):
            errors.append(f"missing official file: {relative}")
            continue
        actual = sha256(path)
        if actual != expected.upper():
            errors.append(f"official file changed: {relative}; expected {expected}, got {actual}")

    for error in errors:
        print(f"[ERROR] {error}")
    if errors:
        print(f"FAIL: {len(errors)} official file integrity error(s)")
        return 1
    print(f"PASS: official h3-prompt-writing unchanged at {lock.get('commit')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
