#!/usr/bin/env python3
"""Validate Narrative IR structure, causality, canon, and continuity.

Uses only the Python standard library so it can run in constrained Codex
workspaces. Structural errors exit 1; warnings remain visible but exit 0 unless
--warnings-as-errors is supplied.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path


SHA256_RE = re.compile(r"^[a-fA-F0-9]{64}$")
TOP_LEVEL = {
    "schema_version",
    "narrative_id",
    "source",
    "canon",
    "story",
    "characters",
    "scenes",
    "events",
    "continuity",
    "promises",
}


def _ids(items, key, label, errors):
    result = {}
    if not isinstance(items, list):
        errors.append(f"{label} must be an array")
        return result
    for index, item in enumerate(items, 1):
        if not isinstance(item, dict):
            errors.append(f"{label}[{index}] must be an object")
            continue
        value = item.get(key)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{label}[{index}] missing {key}")
            continue
        if value in result:
            errors.append(f"duplicate {key}: {value}")
        result[value] = item
    return result


def _rank(scene, event):
    return (scene.get("order", 10**9), event.get("order", 10**9))


def validate(data, foundation=None, foundation_handoff=None):
    errors, warnings = [], []
    if not isinstance(data, dict):
        return ["Narrative IR root must be an object"], []

    missing = sorted(TOP_LEVEL - set(data))
    if missing:
        errors.append("missing top-level fields: " + ", ".join(missing))
    if data.get("schema_version") != "1.0":
        errors.append("schema_version must be '1.0'")

    source = data.get("source") or {}
    for key in ("script_id", "script_version", "source_hash"):
        if not source.get(key):
            errors.append(f"source missing {key}")
    if source.get("source_hash") and not SHA256_RE.fullmatch(str(source["source_hash"])):
        errors.append("source.source_hash must be a 64-character SHA-256 hex digest")

    foundation_ref = data.get("foundation_ref")
    if foundation_ref is not None:
        for key in ("foundation_id", "foundation_version", "foundation_hash", "locked_entity_ids", "locked_rule_ids"):
            if key not in foundation_ref:
                errors.append(f"foundation_ref missing {key}")
        if foundation_ref.get("foundation_hash") and not SHA256_RE.fullmatch(str(foundation_ref["foundation_hash"])):
            errors.append("foundation_ref.foundation_hash must be a 64-character SHA-256 hex digest")
        if foundation is not None:
            if foundation_ref.get("foundation_id") != foundation.get("foundation_id"):
                errors.append("foundation_ref.foundation_id does not match supplied foundation")
            foundation_entities = {item.get("entity_id") for item in foundation.get("entities", []) if isinstance(item, dict)}
            for entity_id in foundation_ref.get("locked_entity_ids", []):
                if entity_id not in foundation_entities:
                    errors.append(f"foundation_ref references unknown foundation entity {entity_id}")
        if foundation_handoff is not None:
            for key, handoff_key in (("foundation_id", "artifact_id"), ("foundation_version", "version"), ("foundation_hash", "content_hash")):
                if foundation_ref.get(key) != foundation_handoff.get(handoff_key):
                    errors.append(f"foundation_ref.{key} does not match supplied foundation handoff")
            locked_entities = set(foundation_handoff.get("locked_entity_ids", []))
            for entity_id in foundation_ref.get("locked_entity_ids", []):
                if entity_id not in locked_entities:
                    errors.append(f"foundation_ref references entity {entity_id} not locked by supplied handoff")

    canon = data.get("canon") or {}
    if canon.get("locked") is not True:
        errors.append("canon.locked must be true")
    if canon.get("plot_change_allowed") is not False:
        errors.append("canon.plot_change_allowed must be false")
    if canon.get("dialogue_policy") not in {"verbatim", "approved_changes_only"}:
        errors.append("canon.dialogue_policy is invalid")

    characters = _ids(data.get("characters"), "character_id", "characters", errors)
    scenes = _ids(data.get("scenes"), "scene_id", "scenes", errors)
    events = _ids(data.get("events"), "event_id", "events", errors)
    promises = _ids(data.get("promises"), "promise_id", "promises", errors)

    scene_orders = defaultdict(list)
    for scene_id, scene in scenes.items():
        order = scene.get("order")
        if not isinstance(order, int) or order < 1:
            errors.append(f"scene {scene_id}: order must be a positive integer")
        scene_orders[order].append(scene_id)
        event_ids = scene.get("event_ids")
        if not isinstance(event_ids, list) or not event_ids:
            errors.append(f"scene {scene_id}: event_ids must be a non-empty array")
            continue
        for event_id in event_ids:
            if event_id not in events:
                errors.append(f"scene {scene_id}: unknown event_id {event_id}")
            elif events[event_id].get("scene_id") != scene_id:
                errors.append(f"scene {scene_id}: event {event_id} declares scene_id={events[event_id].get('scene_id')}")
    for order, ids in scene_orders.items():
        if order is not None and len(ids) > 1:
            errors.append(f"duplicate scene order {order}: {', '.join(ids)}")

    ranks = {}
    event_orders = defaultdict(list)
    for event_id, event in events.items():
        scene_id = event.get("scene_id")
        if scene_id not in scenes:
            errors.append(f"event {event_id}: unknown scene_id {scene_id}")
            continue
        order = event.get("order")
        if not isinstance(order, int) or order < 1:
            errors.append(f"event {event_id}: order must be a positive integer")
        event_orders[(scene_id, order)].append(event_id)
        ranks[event_id] = _rank(scenes[scene_id], event)
        for character_id in event.get("participants", []):
            if character_id not in characters:
                errors.append(f"event {event_id}: unknown participant {character_id}")
        for character_id in event.get("mentions", []):
            if character_id not in characters:
                errors.append(f"event {event_id}: unknown mentioned character {character_id}")
        for change in event.get("knowledge_changes", []):
            if not isinstance(change, dict):
                errors.append(f"event {event_id}: knowledge_changes entries must be objects")
                continue
            character_id = change.get("character_id")
            if character_id not in characters:
                errors.append(f"event {event_id}: knowledge change references unknown character {character_id}")
            elif change.get("info_id") not in characters[character_id].get("knowledge_after", []):
                warnings.append(f"event {event_id}: {character_id} learns {change.get('info_id')} but it is absent from knowledge_after")
    for key, ids in event_orders.items():
        if key[1] is not None and len(ids) > 1:
            errors.append(f"duplicate event order in scene {key[0]} at {key[1]}: {', '.join(ids)}")

    graph = defaultdict(list)
    for event_id, event in events.items():
        for cause_id in event.get("cause_ids", []):
            if cause_id not in events:
                errors.append(f"event {event_id}: unknown cause_id {cause_id}")
                continue
            graph[cause_id].append(event_id)
            if cause_id in ranks and event_id in ranks and ranks[cause_id] >= ranks[event_id]:
                errors.append(f"event {event_id}: cause {cause_id} does not occur earlier")

    visiting, visited = set(), set()

    def visit(node):
        if node in visiting:
            errors.append(f"causality cycle detected at event {node}")
            return
        if node in visited:
            return
        visiting.add(node)
        for child in graph[node]:
            visit(child)
        visiting.remove(node)
        visited.add(node)

    for event_id in events:
        visit(event_id)

    for character_id, character in characters.items():
        before = set(character.get("knowledge_before", []))
        after = set(character.get("knowledge_after", []))
        lost = sorted(before - after)
        if lost:
            warnings.append(f"character {character_id}: knowledge disappears without explanation: {', '.join(lost)}")
        death_rank = None
        last_status_rank = None
        for record in character.get("status_history", []):
            event_id = record.get("event_id")
            if event_id not in events:
                errors.append(f"character {character_id}: status history references unknown event {event_id}")
                continue
            current_rank = ranks.get(event_id)
            if last_status_rank is not None and current_rank is not None and current_rank < last_status_rank:
                errors.append(f"character {character_id}: status history is not chronological at {event_id}")
            last_status_rank = current_rank
            if death_rank is not None and current_rank is not None and current_rank > death_rank and record.get("status") != "dead":
                errors.append(f"character {character_id}: returns from dead status at event {event_id}")
            if record.get("status") == "dead":
                death_rank = current_rank
        if death_rank is not None:
            for event_id, event in events.items():
                if ranks.get(event_id, (-1, -1)) > death_rank and character_id in event.get("participants", []) and event.get("mode", "present") == "present":
                    errors.append(f"character {character_id}: participates in present-time event {event_id} after death")

    continuity = data.get("continuity") or {}
    locations = _ids(continuity.get("locations", []), "location_id", "continuity.locations", errors)
    for prop_id, prop in _ids(continuity.get("props", []), "prop_id", "continuity.props", errors).items():
        destroyed_rank = None
        last_rank = None
        for record in prop.get("state_history", []):
            event_id = record.get("event_id")
            if event_id not in events:
                errors.append(f"prop {prop_id}: state history references unknown event {event_id}")
                continue
            rank = ranks[event_id]
            if last_rank is not None and rank < last_rank:
                errors.append(f"prop {prop_id}: state history is not chronological at {event_id}")
            last_rank = rank
            location_id = record.get("location_id")
            if location_id and location_id not in locations:
                errors.append(f"prop {prop_id}: unknown location_id {location_id}")
            holder_id = record.get("holder_id")
            if holder_id and holder_id not in characters:
                errors.append(f"prop {prop_id}: unknown holder_id {holder_id}")
            if destroyed_rank is not None and rank > destroyed_rank and record.get("status") != "destroyed":
                errors.append(f"prop {prop_id}: returns from destroyed state at event {event_id}")
            if record.get("status") == "destroyed":
                destroyed_rank = rank

    for promise_id, promise in promises.items():
        planted = promise.get("planted_event_id")
        payoff = promise.get("payoff_event_id")
        if planted not in events:
            errors.append(f"promise {promise_id}: unknown planted_event_id {planted}")
        if payoff:
            if payoff not in events:
                errors.append(f"promise {promise_id}: unknown payoff_event_id {payoff}")
            elif planted in ranks and ranks[payoff] <= ranks[planted]:
                errors.append(f"promise {promise_id}: payoff occurs before or at planting")
        if promise.get("status") == "paid_off" and not payoff:
            errors.append(f"promise {promise_id}: paid_off requires payoff_event_id")
        if payoff and promise.get("status") != "paid_off":
            warnings.append(f"promise {promise_id}: payoff_event_id exists but status is {promise.get('status')}")
        if promise.get("status") == "abandoned" and not promise.get("abandon_reason"):
            errors.append(f"promise {promise_id}: abandoned requires abandon_reason")

    ordered_scenes = sorted(scenes.values(), key=lambda item: item.get("order", 10**9))
    for left, right in zip(ordered_scenes, ordered_scenes[1:]):
        left_exit = left.get("exit_state") or {}
        right_entry = right.get("entry_state") or {}
        if isinstance(left_exit, dict) and isinstance(right_entry, dict):
            for key in sorted(set(left_exit) & set(right_entry)):
                if left_exit[key] != right_entry[key]:
                    warnings.append(f"scene handoff {left.get('scene_id')}->{right.get('scene_id')}: state '{key}' changes without an explicit bridge")

    return errors, warnings


def main():
    parser = argparse.ArgumentParser(description="Validate Creative Compiler Narrative IR V1.0")
    parser.add_argument("path")
    parser.add_argument("--foundation", help="Optional locked IP Foundation JSON for cross-contract checks")
    parser.add_argument("--foundation-handoff", help="Optional hashed S-1B handoff JSON for provenance checks")
    parser.add_argument("--warnings-as-errors", action="store_true")
    parser.add_argument("--json", action="store_true", dest="json_output")
    args = parser.parse_args()
    data = json.loads(Path(args.path).read_text(encoding="utf-8-sig"))
    foundation = json.loads(Path(args.foundation).read_text(encoding="utf-8-sig")) if args.foundation else None
    foundation_handoff = json.loads(Path(args.foundation_handoff).read_text(encoding="utf-8-sig")) if args.foundation_handoff else None
    errors, warnings = validate(data, foundation, foundation_handoff)
    failed = bool(errors or (warnings and args.warnings_as_errors))
    if args.json_output:
        print(json.dumps({"status": "FAIL" if failed else "PASS", "errors": errors, "warnings": warnings}, ensure_ascii=False, indent=2))
    else:
        print("FAIL" if failed else "PASS")
        for item in errors:
            print("ERROR:", item)
        for item in warnings:
            print("WARN:", item)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
