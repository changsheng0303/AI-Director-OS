#!/usr/bin/env python3
"""Generate a deterministic skill and license index from skills/*/SKILL.md."""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path


CATEGORIES = {
    "总控与IP": {"short-drama-system", "ai-2d-animation", "ip-foundation-engine", "ip-worldbuilding"},
    "剧本与对白": {"screenplay-master", "micro-drama-creation", "anime-series-scripting", "drama-script-iteration", "screenwriter-review", "universal-dialogue-core", "character-prediction-skill", "humanizer", "graded-anime-plot-writing"},
    "导演与分镜": {"director-mindset", "storyboard-script-spec", "ai-video-storyboard-compiler", "micro-expression-video-prompts", "design-disney-animation-prompts"},
    "图片与资产": {"character-design-director", "anime-scene-asset-design", "ai-image-assets", "series-image-director", "cinema-dna-21x9x3", "one-image-film-ad-director", "pop-visual-ad-director"},
    "视频提示词": {"ai-video-prompt-production", "h3-prompt-writing", "h3-video-prompt-workflow", "h3-video-prompt-iteration", "minimax-h3-video-prompt-pipeline", "ref2va-prompt-optimizer", "ref2va-batch-rewrite", "tag-h3", "seedance25-prompt-workflow", "fafajing-prompt-writer", "adult-adjacent-video-prompts"},
    "文档与音乐": {"project-documentation", "songwriting-and-ai-music"},
}


def clean(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        value = value[1:-1]
    return value.replace("|", "\\|").strip()


def frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"^---\r?\n([\s\S]*?)\r?\n---", text)
    if not match:
        return {}
    lines = match.group(1).splitlines()
    result: dict[str, str] = {}
    index = 0
    while index < len(lines):
        line = lines[index]
        field = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if not field:
            index += 1
            continue
        key, value = field.group(1), field.group(2).strip()
        if value in {"|", ">", "|-", ">-"}:
            block = []
            index += 1
            while index < len(lines) and (lines[index].startswith(" ") or not lines[index].strip()):
                block.append(lines[index].strip())
                index += 1
            result[key] = " ".join(item for item in block if item)
            continue
        result[key] = clean(value)
        index += 1
    return result


def detect_license(skill_dir: Path, meta: dict[str, str]) -> str:
    if meta.get("license"):
        return meta["license"]
    license_files = [path for path in (skill_dir / "LICENSE", skill_dir / "LICENSE.md", skill_dir / "license.txt") if path.is_file()]
    if not license_files:
        return "未声明（默认保留权利）"
    sample = license_files[0].read_text(encoding="utf-8-sig", errors="replace")[:3000].lower()
    if "mit license" in sample:
        return "MIT"
    if "apache license" in sample:
        return "Apache-2.0"
    return f"见 {license_files[0].name}"


def category(folder: str) -> str:
    for label, members in CATEGORIES.items():
        if folder in members:
            return label
    return "其他"


def build(repo_root: Path, stamp: str) -> str:
    skill_root = repo_root / "skills"
    rows = []
    for skill_dir in sorted(path for path in skill_root.iterdir() if path.is_dir()):
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.is_file():
            continue
        meta = frontmatter(skill_md.read_text(encoding="utf-8-sig"))
        rows.append({
            "category": category(skill_dir.name),
            "folder": skill_dir.name,
            "name": clean(meta.get("name", skill_dir.name)),
            "description": clean(meta.get("description", "未填写描述")),
            "license": clean(detect_license(skill_dir, meta)),
        })

    counts = Counter(row["license"] for row in rows)
    out = [
        "# AI Director OS Skill 与许可证索引",
        "",
        f"> 自动生成日期：{stamp}",
        f"> Skill 数量：{len(rows)}  ",
        "> 生成命令：`python scripts/generate_skill_index.py`",
        "",
        "本文件由脚本生成，请不要手工编辑。公开可见不等于获得统一许可；以每个目录的声明为准。",
        "",
        "## 许可证摘要",
        "",
        "| 声明 | 数量 |",
        "|---|---:|",
    ]
    for license_name, count in sorted(counts.items(), key=lambda item: (-item[1], item[0])):
        out.append(f"| {license_name} | {count} |")
    out.extend(["", "## Skill 清单", "", "| 分类 | 目录 | Skill | 说明 | 许可证 |", "|---|---|---|---|---|"])
    for row in sorted(rows, key=lambda item: (item["category"], item["folder"])):
        out.append(f"| {row['category']} | `{row['folder']}` | `{row['name']}` | {row['description']} | {row['license']} |")
    out.extend([
        "",
        "## 维护规则",
        "",
        "- 新增或删除 Skill 后重新运行生成脚本；",
        "- CI 或发布前运行 `python scripts/generate_skill_index.py --check`；",
        "- 未声明许可证的目录默认保留权利，不得推断为MIT或其他开源许可证；",
        "- 根目录 `LICENSE.md` 与 `NOTICE.md` 不覆盖子目录自己的许可证。",
        "",
    ])
    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path)
    parser.add_argument("--date")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    repo_root = args.repo.resolve()
    output = args.output.resolve() if args.output else repo_root / "docs" / "SKILL_INDEX.md"
    stamp = args.date
    if args.check and not stamp and output.is_file():
        existing = output.read_text(encoding="utf-8-sig")
        found = re.search(r"自动生成日期：([0-9]{4}-[0-9]{2}-[0-9]{2})", existing)
        stamp = found.group(1) if found else None
    generated = build(repo_root, stamp or date.today().isoformat())
    if args.check:
        if not output.is_file() or output.read_text(encoding="utf-8-sig") != generated:
            print(f"STALE: {output}")
            return 1
        print(f"PASS: {output}")
        return 0
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(generated, encoding="utf-8", newline="\n")
    print(f"WROTE: {output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
