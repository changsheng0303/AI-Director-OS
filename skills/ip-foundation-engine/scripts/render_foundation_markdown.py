#!/usr/bin/env python3
"""Render a human-readable World and Character Bible from IP Foundation JSON."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def render(package):
    facts = {item["fact_id"]: item for item in package.get("facts", []) if isinstance(item, dict) and item.get("fact_id")}
    entities = {item["entity_id"]: item for item in package.get("entities", []) if isinstance(item, dict) and item.get("entity_id")}
    lines = [
        f"# {package['project']['title']} · IP Foundation",
        "",
        f"- Foundation: `{package['foundation_id']}`",
        f"- Audit: `{package['audit']['status']}`",
        f"- Format: {package['project'].get('format', '未锁定')}",
        "",
        "## Canon Summary",
        "",
    ]
    for fact_id in package.get("canon", {}).get("locked_fact_ids", []):
        fact = facts.get(fact_id)
        if fact:
            lines.append(f"- `{fact_id}` · {fact['path']}: {fact['value']}")
    lines.extend(["", "## World and Entity Registry", ""])
    for entity in package.get("entities", []):
        lines.append(f"### {entity['name']} · {entity['entity_type']} · {entity['importance']}")
        for fact_id in entity.get("fact_ids", []):
            fact = facts.get(fact_id)
            if fact:
                marker = "锁定" if fact.get("authority") == "locked" else "待确认"
                lines.append(f"- {fact['path']}: {fact['value']}（{marker}）")
        if entity.get("narrative_functions"):
            lines.append("- 叙事功能: " + "、".join(entity["narrative_functions"]))
        lines.append("")
    lines.extend(["## Cast Manifest", "", "| Entity | Role | Depth |", "|---|---|---|"])
    for member in package.get("cast", {}).get("members", []):
        entity = entities.get(member.get("entity_id"), {})
        lines.append(f"| {entity.get('name', member.get('entity_id'))} | {member.get('cast_role')} | {member.get('production_depth')} |")
    lines.extend(["", "## Relationship Graph", ""])
    for edge in package.get("relationships", []):
        left = entities.get(edge.get("from"), {}).get("name", edge.get("from"))
        right = entities.get(edge.get("to"), {}).get("name", edge.get("to"))
        dimensions = "、".join(f"{key}:{value}" for key, value in edge.get("dimensions", {}).items())
        lines.append(f"- {left} → {right}: {edge['public_relation']}；{dimensions}")
    lines.extend(["", "## Downstream Contract", ""])
    lines.append("- Allowed scope: " + "、".join(package.get("constraints", {}).get("allowed_story_scope", [])))
    lines.append("- Prohibited assumptions: " + "、".join(package.get("constraints", {}).get("prohibited_assumptions", [])))
    pending = [fact for fact in package.get("facts", []) if fact.get("authority") == "pending"]
    if pending:
        lines.extend(["", "## Pending Proposals", ""])
        for fact in pending:
            lines.append(f"- `{fact['fact_id']}` · {fact['path']}: {fact['value']}")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Render IP Foundation Markdown")
    parser.add_argument("path")
    parser.add_argument("--output")
    args = parser.parse_args()
    package = json.loads(Path(args.path).read_text(encoding="utf-8-sig"))
    markdown = render(package)
    if args.output:
        Path(args.output).write_text(markdown, encoding="utf-8")
    else:
        print(markdown, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
