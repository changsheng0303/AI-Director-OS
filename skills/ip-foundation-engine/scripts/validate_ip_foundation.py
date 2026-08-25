#!/usr/bin/env python3
"""Deterministic validator for IP Foundation Package V1.0."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


def index(items, key, label, errors):
    result = {}
    if not isinstance(items, list):
        errors.append(f"{label} must be an array")
        return result
    for position, item in enumerate(items, 1):
        if not isinstance(item, dict) or not item.get(key):
            errors.append(f"{label}[{position}] missing {key}")
            continue
        value = item[key]
        if value in result:
            errors.append(f"duplicate {label} {value}")
        result[value] = item
    return result


def validate(package):
    errors, warnings = [], []
    required = {"schema_version", "foundation_id", "project", "seed", "facts", "entities", "cast", "relationships", "constraints", "canon", "audit"}
    if not isinstance(package, dict):
        return ["foundation root must be an object"], []
    missing = sorted(required - set(package))
    if missing:
        errors.append("missing top-level fields: " + ", ".join(missing))
    if package.get("schema_version") != "1.0":
        errors.append("schema_version must be 1.0")

    facts = index(package.get("facts"), "fact_id", "facts", errors)
    entities = index(package.get("entities"), "entity_id", "entities", errors)
    relationships = index(package.get("relationships"), "relationship_id", "relationships", errors)

    locked_paths = {}
    for fact_id, fact in facts.items():
        if fact.get("origin") == "ai_proposal" and fact.get("authority") == "locked" and not fact.get("accepted_by"):
            errors.append(f"fact {fact_id}: locked AI proposal requires accepted_by")
        if fact.get("authority") == "locked":
            path = fact.get("path")
            if path in locked_paths and locked_paths[path].get("value") != fact.get("value"):
                errors.append(f"conflicting locked facts at path {path}")
            locked_paths[path] = fact

    for entity_id, entity in entities.items():
        for fact_id in entity.get("fact_ids", []):
            fact = facts.get(fact_id)
            if fact is None:
                errors.append(f"entity {entity_id}: unknown fact {fact_id}")
            elif fact.get("layer") != "static":
                errors.append(f"entity {entity_id}: dynamic fact {fact_id} cannot enter IP Foundation")
        relevance = entity.get("narrative_relevance", {})
        used_by = relevance.get("used_by", [])
        if relevance.get("impact") == "high" and not used_by:
            errors.append(f"entity {entity_id}: high narrative relevance requires used_by")
        if relevance.get("impact") == "none" and used_by:
            warnings.append(f"entity {entity_id}: impact none conflicts with used_by references")
        for ref in used_by:
            if ref not in entities:
                errors.append(f"entity {entity_id}: narrative relevance references unknown entity {ref}")

    cast = package.get("cast", {})
    members = cast.get("members", []) if isinstance(cast, dict) else []
    actual_counts = Counter()
    for member in members:
        entity = entities.get(member.get("entity_id"))
        if entity is None:
            errors.append(f"cast member references unknown entity {member.get('entity_id')}")
            continue
        if entity.get("entity_type") not in {"character", "pet"}:
            errors.append(f"cast member {member.get('entity_id')} must be character or pet")
        actual_counts[f"{member.get('kind')}_{member.get('presentation')}"] += 1
        if member.get("cast_role") == "protagonist" and member.get("production_depth") == "skeleton":
            errors.append(f"protagonist {member.get('entity_id')} requires bible or production depth")
    for key, expected in cast.get("declared_counts", {}).items() if isinstance(cast, dict) else []:
        if actual_counts.get(key, 0) != expected:
            errors.append(f"declared_counts {key}={expected}, actual={actual_counts.get(key, 0)}")

    seen_edges = set()
    for relationship_id, edge in relationships.items():
        source, target = edge.get("from"), edge.get("to")
        if source not in entities or target not in entities:
            errors.append(f"relationship {relationship_id}: endpoints must exist")
        if source == target:
            errors.append(f"relationship {relationship_id}: self relationship is invalid")
        edge_key = (source, target, edge.get("public_relation"))
        if edge_key in seen_edges:
            errors.append(f"duplicate directional relationship {source}->{target} ({edge.get('public_relation')})")
        seen_edges.add(edge_key)

    canon = package.get("canon", {})
    for fact_id in canon.get("locked_fact_ids", []):
        fact = facts.get(fact_id)
        if fact is None:
            errors.append(f"canon references unknown fact {fact_id}")
        elif fact.get("authority") != "locked" or fact.get("layer") != "static":
            errors.append(f"canon fact {fact_id} must be locked and static")

    audit = package.get("audit", {})
    unresolved = package.get("seed", {}).get("unresolved_fields", [])
    critical = [item.get("field") for item in unresolved if isinstance(item, dict) and item.get("critical")]
    if audit.get("status") == "FOUNDATION_LOCKED":
        if canon.get("locked") is not True:
            errors.append("FOUNDATION_LOCKED requires canon.locked=true")
        if critical:
            errors.append("FOUNDATION_LOCKED has critical unresolved fields: " + ", ".join(critical))
        if not any(item.get("entity_type") == "world" for item in entities.values()):
            errors.append("FOUNDATION_LOCKED requires a world entity")
        if not any(item.get("cast_role") in {"protagonist", "main"} for item in members):
            errors.append("FOUNDATION_LOCKED requires at least one protagonist or main cast member")

    function_sets = {}
    for entity_id, entity in entities.items():
        if entity.get("entity_type") not in {"character", "pet"}:
            continue
        signature = tuple(sorted(entity.get("narrative_functions", [])))
        if signature:
            function_sets.setdefault(signature, []).append(entity_id)
    for signature, entity_ids in function_sets.items():
        if len(entity_ids) > 1:
            warnings.append(f"possible role duplication {', '.join(entity_ids)}: {', '.join(signature)}")

    return errors, warnings


def main():
    parser = argparse.ArgumentParser(description="Validate IP Foundation Package V1.0")
    parser.add_argument("path")
    parser.add_argument("--warnings-as-errors", action="store_true")
    args = parser.parse_args()
    package = json.loads(Path(args.path).read_text(encoding="utf-8-sig"))
    errors, warnings = validate(package)
    failed = bool(errors or (warnings and args.warnings_as_errors))
    print("FAIL" if failed else "PASS")
    for item in errors:
        print("ERROR:", item)
    for item in warnings:
        print("WARN:", item)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
