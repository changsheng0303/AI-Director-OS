#!/usr/bin/env python3
"""Lightweight screenplay output checks.

Usage:
    python scripts/check_screenplay_text.py path/to/output.md
"""

from __future__ import annotations

import sys
from pathlib import Path


REQUIRED_SIGNALS = {
    "hook": ["hook", "钩子", "开场"],
    "conflict": ["conflict", "冲突"],
    "payoff": ["payoff", "兑现", "结尾"],
    "character": ["character", "人物", "角色"],
    "risk": ["risk", "风险", "合规"],
}


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python scripts/check_screenplay_text.py path/to/output.md")
        sys.exit(2)

    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"FAIL: file not found: {path}")
        sys.exit(1)

    text = path.read_text(encoding="utf-8").lower()
    missing = []
    for name, signals in REQUIRED_SIGNALS.items():
        if not any(signal.lower() in text for signal in signals):
            missing.append(name)

    if missing:
        print("WARN: missing screenplay signals: " + ", ".join(missing))
        sys.exit(1)

    print("OK: screenplay output includes core hook/conflict/payoff/character/risk signals")


if __name__ == "__main__":
    main()
