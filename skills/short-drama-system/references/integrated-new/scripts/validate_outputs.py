#!/usr/bin/env python3
"""Validate staged shortdrama-studio-lite project outputs."""

from __future__ import annotations

import argparse
import json
import re
import tempfile
from pathlib import Path
from typing import Any


TABLES = {
    "01-角色表.md": ["角色ID", "角色名称", "别名/称谓", "重要级别", "出现分集", "年龄", "变体数", "当前变体", "性格", "角色弧光", "声音描述", "角色生成提示词", "音色生成提示词", "依据/状态"],
    "02-场景表.md": ["场景ID", "场景名称", "出现分集/场次", "内外景", "时间/天气", "剧情功能", "空间拓扑", "变体数", "当前变体", "出场角色", "关键道具", "光线/色彩/材料", "连续性锚点", "场景生成提示词", "依据/状态"],
    "03-道具表.md": ["道具ID", "道具名称", "出现分集/场次", "归属角色", "类别/尺度", "剧情功能", "变体数", "当前变体", "材质/颜色/磨损", "使用方式/持握", "连续性锚点", "道具生成提示词", "依据/状态"],
}
PROMPT_FILES = ["04-资产索引.md", "05-分镜脚本.md", "06-Seedance视频提示词.md", "07-即梦生成计划.json"]
SECTIONS = ["【整体参考锁定】", "【统一连续性】", "【声音】", "【关键限制】", "【组间交接】"]
GROUP_RE = re.compile(r"^##\s+(G\d+)[｜|].*?[｜|](\d+)s[｜|]\s*Seedance\s+(2\.0|2\.5)\s*$", re.M)
IMAGE_SLOT = re.compile(r"@图片(\d+)")
AUDIO_SLOT = re.compile(r"@音频(\d+)")


def table_header(text: str) -> list[str] | None:
    for line in text.splitlines():
        if line.lstrip().startswith("|") and line.rstrip().endswith("|"):
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if cells and not all(set(cell) <= {"-", ":", " "} for cell in cells):
                return cells
    return None


def validate_tables(root: Path, errors: list[str], warnings: list[str]) -> None:
    for name, expected in TABLES.items():
        path = root / name
        if not path.is_file():
            errors.append(f"missing: {name}")
            continue
        text = path.read_text(encoding="utf-8")
        header = table_header(text)
        if header != expected:
            errors.append(f"{name}: table columns do not match the required ordered schema")
        data_lines = [line for line in text.splitlines() if line.startswith("|")]
        if len(data_lines) < 3:
            errors.append(f"{name}: no data row")
        if re.search(r"(?:同上|待填写|待补充|\[角色名\]|\[场景名\]|\[道具名\])", text):
            errors.append(f"{name}: unresolved placeholder or context-dependent value")
        if "依据/状态" not in text:
            errors.append(f"{name}: evidence/status field missing")


def slots(pattern: re.Pattern[str], text: str) -> set[int]:
    return {int(value) for value in pattern.findall(text)}


def duration_limit(model: str) -> int | None:
    if model == "seedance2.5":
        return 30
    if model.startswith("seedance2.0"):
        return 15
    return None


def read_plan(path: Path, errors: list[str]) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        errors.append(f"invalid 07-即梦生成计划.json: {exc}")
        return None
    if not isinstance(value, dict) or not isinstance(value.get("requests"), list) or not value["requests"]:
        errors.append("07-即梦生成计划.json: requests must be a non-empty list")
        return None
    return value


def validate_prompts(root: Path, errors: list[str], warnings: list[str]) -> None:
    for name in PROMPT_FILES:
        if not (root / name).is_file():
            errors.append(f"missing: {name}")
    if any(not (root / name).is_file() for name in PROMPT_FILES):
        return

    asset_index = (root / "04-资产索引.md").read_text(encoding="utf-8")
    storyboard = (root / "05-分镜脚本.md").read_text(encoding="utf-8")
    prompt = (root / "06-Seedance视频提示词.md").read_text(encoding="utf-8")
    plan = read_plan(root / "07-即梦生成计划.json", errors)
    if plan is None:
        return

    if not re.search(r"^#{2,4}\s+镜头?\d+", storyboard, re.M):
        errors.append("05-分镜脚本.md: no numbered shot")
    forbidden = {
        "JSON code fence": r"```\s*json",
        "CLI/request field": r'"(?:modelVersion|submit_id|gen_status|duration|resolution)"\s*:',
        "internal metadata": r"(?:内部推理|审核评分|请求指纹|任务状态)\s*[：:]",
        "unresolved marker": r"待确认|待填写",
    }
    for label, pattern in forbidden.items():
        if re.search(pattern, prompt, re.I):
            errors.append(f"06-Seedance视频提示词.md contains {label}")

    matches = list(GROUP_RE.finditer(prompt))
    if not matches:
        errors.append("06-Seedance视频提示词.md: no valid group heading")
    group_chunks = re.split(r"(?=^##\s+G\d+[｜|])", prompt, flags=re.M)[1:]
    for index, chunk in enumerate(group_chunks, start=1):
        for section in SECTIONS:
            if section not in chunk:
                errors.append(f"prompt group {index}: missing {section}")
        if not re.search(r"镜头\d+.*?(?:组内|全片).*?\d{2}:\d{2}", chunk, re.S):
            warnings.append(f"prompt group {index}: shot timing is not clearly detectable")

    requests = plan["requests"]
    ids: list[str] = []
    for index, request in enumerate(requests, start=1):
        if not isinstance(request, dict):
            errors.append(f"request {index}: must be an object")
            continue
        request_id = request.get("id")
        model = request.get("modelVersion")
        duration = request.get("duration")
        command = request.get("command")
        if not isinstance(request_id, str) or not request_id:
            errors.append(f"request {index}: missing id")
        else:
            ids.append(request_id)
        if command not in {"text2video", "image2video", "frames2video", "multimodal2video", "multiframe2video"}:
            errors.append(f"request {request_id or index}: unsupported command")
        if not isinstance(model, str) or duration_limit(model) is None:
            errors.append(f"request {request_id or index}: unsupported or missing modelVersion")
        if not isinstance(duration, int):
            errors.append(f"request {request_id or index}: duration must be an integer")
        elif isinstance(model, str):
            limit = duration_limit(model)
            if limit is not None and not 4 <= duration <= limit:
                errors.append(f"request {request_id or index}: duration {duration}s exceeds 4-{limit}s contract")
        prompt_value = request.get("prompt")
        if not isinstance(prompt_value, str) or not prompt_value.strip():
            errors.append(f"request {request_id or index}: inline prompt missing")
    if len(ids) != len(set(ids)):
        errors.append("generation plan request ids are not unique")
    if matches and len(matches) != len(requests):
        errors.append("formal prompt group count differs from generation plan request count")
    for match in matches:
        group_id, seconds, family = match.groups()
        expected_model = "seedance2.5" if family == "2.5" else "seedance2.0"
        matching = [item for item in requests if isinstance(item, dict) and item.get("id") == group_id]
        if len(matching) != 1:
            errors.append(f"{group_id}: no unique matching request")
            continue
        if matching[0].get("modelVersion") != expected_model:
            errors.append(f"{group_id}: model differs between formal prompt and plan")
        if matching[0].get("duration") != int(seconds):
            errors.append(f"{group_id}: duration differs between formal prompt and plan")

    used_images = slots(IMAGE_SLOT, prompt)
    indexed_images = slots(IMAGE_SLOT, asset_index)
    if used_images - indexed_images:
        errors.append(f"image slots absent from asset index: {sorted(used_images - indexed_images)}")
    used_audio = slots(AUDIO_SLOT, prompt)
    indexed_audio = slots(AUDIO_SLOT, asset_index)
    if used_audio - indexed_audio:
        errors.append(f"audio slots absent from asset index: {sorted(used_audio - indexed_audio)}")
    for label, values in (("image", indexed_images), ("audio", indexed_audio)):
        if values and values != set(range(1, max(values) + 1)):
            errors.append(f"{label} slots in asset index are not contiguous from 1")
    if re.search(r"\b(?:OS|VO)\b|画外音|播报", prompt, re.I) and not re.search(r"(?:闭口|嘴部.*闭合|不生成口型)", prompt):
        errors.append("OS/VO exists without a closed-mouth constraint")


def validate_generated(root: Path, errors: list[str], warnings: list[str]) -> None:
    audit_path = root / "08-生成审计.json"
    if not audit_path.is_file():
        errors.append("missing: 08-生成审计.json")
        return
    try:
        audit = json.loads(audit_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        errors.append(f"invalid 08-生成审计.json: {exc}")
        return
    requests = audit.get("requests") if isinstance(audit, dict) else None
    if not isinstance(requests, list) or not requests:
        errors.append("08-生成审计.json: requests must be a non-empty list")
        return
    for index, item in enumerate(requests, start=1):
        if not isinstance(item, dict):
            errors.append(f"audit request {index}: must be an object")
            continue
        request_id = item.get("id", index)
        if not item.get("requestFingerprint"):
            errors.append(f"audit {request_id}: requestFingerprint missing")
        if not item.get("submit_id"):
            errors.append(f"audit {request_id}: submit_id missing")
        if item.get("gen_status") != "success":
            errors.append(f"audit {request_id}: gen_status is not success")
        outputs = item.get("outputFiles")
        if not isinstance(outputs, list) or not outputs:
            errors.append(f"audit {request_id}: outputFiles missing")
            continue
        for raw in outputs:
            path = Path(raw).expanduser()
            if not path.is_absolute():
                path = (root / path).resolve()
            if not path.is_file() or path.stat().st_size == 0:
                errors.append(f"audit {request_id}: missing or empty output {path}")
        if not item.get("ffprobe"):
            warnings.append(f"audit {request_id}: ffprobe metadata missing")


def validate(root: Path, stage: str) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    validate_tables(root, errors, warnings)
    if stage in {"prompts", "generated"}:
        validate_prompts(root, errors, warnings)
    if stage == "generated":
        validate_generated(root, errors, warnings)
    status = "PASS" if not errors and not warnings else "PASS_WITH_WARNINGS" if not errors else "FAILED"
    return {"status": status, "stage": stage, "root": str(root), "errors": errors, "warnings": warnings}


def self_test() -> int:
    with tempfile.TemporaryDirectory(prefix="shortdrama-studio-lite-") as raw:
        root = Path(raw)
        for name, columns in TABLES.items():
            identifier = "CHAR-001" if name.startswith("01") else "SCENE-001" if name.startswith("02") else "PROP-001"
            values = [identifier] + ["已锁定" for _ in columns[1:]]
            root.joinpath(name).write_text(
                "# smoke\n\n| " + " | ".join(columns) + " |\n| " + " | ".join(["---"] * len(columns)) + " |\n| " + " | ".join(values) + " |\n",
                encoding="utf-8",
            )
        root.joinpath("04-资产索引.md").write_text("# 资产\n\n人物：@图片1\n", encoding="utf-8")
        root.joinpath("05-分镜脚本.md").write_text("# 分镜\n\n## 镜头01｜00:00-00:15\n动作完成。\n", encoding="utf-8")
        group_prompt = """## G001｜全片 00:00-00:15｜组内 00:00-00:15｜15s｜Seedance 2.0

【整体参考锁定】
人物：@图片1锁定身份。
【统一连续性】
轴线与光线锁定。
镜头01｜组内 00:00-00:15｜全片 00:00-00:15｜建立
35mm中景，人物完成动作。
【声音】
环境声，无音乐。
【关键限制】
身份不漂移。
【组间交接】
末帧保持人物站立。
"""
        root.joinpath("06-Seedance视频提示词.md").write_text(group_prompt, encoding="utf-8")
        root.joinpath("07-即梦生成计划.json").write_text(json.dumps({
            "schemaVersion": 1,
            "kind": "video",
            "project": "smoke",
            "modelFamily": "seedance2.0",
            "requests": [{
                "id": "G001",
                "command": "text2video",
                "modelVersion": "seedance2.0",
                "duration": 15,
                "ratio": "16:9",
                "resolution": "720p",
                "prompt": group_prompt,
                "referenceImages": [],
                "referenceVideos": [],
                "referenceAudio": [],
                "outputDir": "09-视频/G001",
            }],
        }, ensure_ascii=False), encoding="utf-8")
        positive = validate(root, "prompts")
        prompt_25 = group_prompt.replace("00:15", "00:30").replace("15s", "30s").replace("Seedance 2.0", "Seedance 2.5")
        root.joinpath("06-Seedance视频提示词.md").write_text(prompt_25, encoding="utf-8")
        plan_25 = json.loads(root.joinpath("07-即梦生成计划.json").read_text(encoding="utf-8"))
        plan_25["modelFamily"] = "seedance2.5"
        plan_25["requests"][0]["modelVersion"] = "seedance2.5"
        plan_25["requests"][0]["duration"] = 30
        plan_25["requests"][0]["prompt"] = prompt_25
        root.joinpath("07-即梦生成计划.json").write_text(json.dumps(plan_25, ensure_ascii=False), encoding="utf-8")
        positive_25 = validate(root, "prompts")
        root.joinpath("06-Seedance视频提示词.md").write_text(group_prompt, encoding="utf-8")
        invalid_plan = json.loads(root.joinpath("07-即梦生成计划.json").read_text(encoding="utf-8"))
        invalid_plan["modelFamily"] = "seedance2.0"
        invalid_plan["requests"][0]["modelVersion"] = "seedance2.0"
        invalid_plan["requests"][0]["prompt"] = group_prompt
        invalid_plan["requests"][0]["duration"] = 30
        root.joinpath("07-即梦生成计划.json").write_text(json.dumps(invalid_plan, ensure_ascii=False), encoding="utf-8")
        negative = validate(root, "prompts")
        passed = (
            positive["status"] in {"PASS", "PASS_WITH_WARNINGS"}
            and positive_25["status"] in {"PASS", "PASS_WITH_WARNINGS"}
            and negative["status"] == "FAILED"
        )
        print(json.dumps({"status": "PASS" if passed else "FAILED", "accepts15s2_0": positive, "accepts30s2_5": positive_25, "rejectsOverlong2_0": negative}, ensure_ascii=False, indent=2))
        return 0 if passed else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, nargs="?")
    parser.add_argument("--stage", choices=("tables", "prompts", "generated"), default="tables")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    if args.root is None:
        parser.error("root is required unless --self-test is used")
    root = args.root.expanduser().resolve()
    result = validate(root, args.stage)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] in {"PASS", "PASS_WITH_WARNINGS"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
