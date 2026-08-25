#!/usr/bin/env python3
"""Validate the screenplay-master skill package structure."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "SKILL.md",
    "agents/openai.yaml",
    "references/routing-and-output-modes.md",
    "references/format-1-3min-promo.md",
    "references/format-4-6min-short-film.md",
    "references/format-micro-series.md",
    "references/format-long-series.md",
    "references/platform-playbooks.md",
    "references/tree-structure-method.md",
    "references/hook-library.md",
    "references/character-arc-system.md",
    "references/genre-playbooks.md",
    "references/dialogue-and-scene-style.md",
    "references/continuity-system.md",
    "references/commercial-script-rules.md",
    "references/compliance-and-platform-risk.md",
    "references/review-checklists.md",
    "references/screenplay-master-full-blueprint.md",
    "assets/script-template.md",
    "assets/episode-outline-template.md",
    "assets/character-card-template.md",
    "assets/series-bible-template.md",
    "assets/beat-sheet-template.md",
    "assets/review-report-template.md",
    "evals/evals.json",
    "evals/scoring-rubric.md",
    "scripts/check_screenplay_text.py",
]


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


def main() -> None:
    missing = [name for name in REQUIRED_FILES if not (ROOT / name).is_file()]
    if missing:
        fail("missing required files: " + ", ".join(missing))

    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    if not skill.startswith("---\n"):
        fail("SKILL.md missing YAML frontmatter")
    frontmatter = skill.split("---\n", 2)[1]
    if "name: screenplay-master" not in frontmatter:
        fail("frontmatter name must be screenplay-master")
    desc_match = re.search(r"^description:\s*(.+)$", frontmatter, re.M)
    if not desc_match:
        fail("frontmatter description missing")
    if len(desc_match.group(1)) > 1200:
        fail("frontmatter description is too long")

    linked_refs = set(re.findall(r"\]\((references/[^)]+)\)", skill))
    required_refs = {
        name for name in REQUIRED_FILES if name.startswith("references/")
    }
    missing_links = sorted(required_refs - linked_refs)
    if missing_links:
        fail("SKILL.md does not link references: " + ", ".join(missing_links))

    openai_yaml = (ROOT / "agents/openai.yaml").read_text(encoding="utf-8")
    if "$screenplay-master" not in openai_yaml:
        fail("agents/openai.yaml default_prompt must mention $screenplay-master")

    print("OK: screenplay-master skill package structure is valid")


if __name__ == "__main__":
    main()
