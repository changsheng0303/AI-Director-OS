#!/usr/bin/env python3
"""Return blocking fields for one stage-level foundation decision packet.

The script selects fields rather than writing user-facing questions. The model
must present all returned blocking fields together, with exactly four choices
per question: A/B/C concrete mutually exclusive proposals and D custom input.
Known fields are never re-asked.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def known_paths(package):
    return {
        item.get("path")
        for item in package.get("facts", [])
        if isinstance(item, dict) and item.get("authority") != "rejected" and item.get("path")
    }


def route(package, limit):
    paths = known_paths(package)
    project = package.get("project", {})
    seed = package.get("seed", {})
    cast = package.get("cast", {}).get("members", [])
    entities = package.get("entities", [])
    raw = str(seed.get("raw_input", "")).lower()
    questions = []

    def add(field, priority, question, reason, condition=True):
        if condition:
            questions.append({"field": field, "priority": priority, "question": question, "reason": reason})

    add(
        "project.format",
        100,
        "你希望把它做成什么形式：短片、竖屏短剧、番剧、长剧集，还是先作为长期 IP？",
        "形式决定世界规模、角色深度与后续生产约束。",
        not project.get("format"),
    )
    add(
        "story.premise",
        95,
        "观众最先应跟随谁，并看到她/他们面对什么核心问题或冲突？",
        "没有核心人物或冲突，世界设定无法判断叙事相关性。",
        "story.premise" not in paths and "story.protagonist" not in paths,
    )
    add(
        "world.setting",
        85,
        "这个故事最主要发生在怎样的世界或地点？一句话即可。",
        "需要最低可用的时空与活动范围来建立世界骨架。",
        not any(item.get("entity_type") == "world" for item in entities),
    )
    add(
        "cast.architecture",
        75,
        "除了主角外，你目前希望有哪些主要人物或关系位置？不知道名字也可以先说角色功能。",
        "只有在现有输入无法形成阵容时，才询问角色结构。",
        not cast,
    )
    add(
        "world.tone",
        60,
        "你希望这个世界整体更偏轻松、浪漫、悬疑、热血、现实，还是其他气质？",
        "调性影响世界规则、角色行为和视觉系统，但不阻塞最小草案。",
        "world.tone" not in paths,
    )
    nonhuman_hint = any(word in raw for word in ("魔法", "妖", "怪", "精灵", "机器人", "科幻", "异世界", "动物", "宠物"))
    add(
        "cast.non_human_plan",
        40,
        "这个世界是否需要宠物、动物、机器人、超自然生物或其他非人角色参与主要剧情？",
        "种子显示非人元素可能影响角色分类与世界规则。",
        nonhuman_hint and "cast.non_human_plan" not in paths,
    )
    questions.sort(key=lambda item: item["priority"], reverse=True)
    blocking = [item for item in questions if item["priority"] >= 75]
    return {
        "packet_mode": "single_stage_batch",
        "option_contract": {
            "A_B_C": "three concrete mutually exclusive proposals with direct impact",
            "D": "补充内容／自定义",
        },
        "max_questions": limit,
        "questions": blocking[:limit],
        "known_paths": sorted(paths),
    }


def main():
    parser = argparse.ArgumentParser(description="Build one batched IP Foundation decision packet")
    parser.add_argument("path")
    parser.add_argument("--limit", type=int, default=6)
    args = parser.parse_args()
    package = json.loads(Path(args.path).read_text(encoding="utf-8-sig"))
    print(json.dumps(route(package, max(1, min(args.limit, 6))), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
