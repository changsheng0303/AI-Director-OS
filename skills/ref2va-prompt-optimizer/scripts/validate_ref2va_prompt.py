#!/usr/bin/env python3
"""Validate structural invariants of a MiniMax H3 Ref2VA prompt."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


SECTIONS = (
    "subject_definitions",
    "summary",
    "retention_analysis",
    "detailed_description",
    "overall_soundscape",
    "non_diegetic_music",
)

TASK_TYPES = {
    "keyframe completion",
    "reference generation",
    "video editing",
    "video continuation",
    "audio reuse",
    "audio reference",
}

VISUAL_MARKERS = {
    "fully_preserved",
    "partially_preserved",
    "attribute_transfer",
    "weak_reference",
}

AUDIO_MARKERS = {"fully_copy", "partially_copy", "reference", "weak_reference"}

TAG_RE = re.compile(r"<(Subject|Picture|Video|Audio)\s+(\d+)>")
HEADER_RE = re.compile(r"(?m)^([a-z_]+):\s*$")
DEFINITION_RE = re.compile(r"(?m)^(<(?:Subject|Picture|Video|Audio)\s+\d+>)\s+.+$")
RETENTION_RE = re.compile(
    r"(?m)^(<(Subject|Picture|Video|Audio)\s+\d+>)(?:\s+\([^\n]*\))?:\s+"
    r"([a-z_]+)\s+-\s+.+$"
)
SHOT_RE = re.compile(r"\[Shot\s+(\d+)\](?:\s+At\s+(\d{2}):(\d{2})\.(\d{3}),)?")


def split_sections(text: str) -> dict[str, str]:
    matches = list(HEADER_RE.finditer(text))
    result: dict[str, str] = {}
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        result[match.group(1)] = text[start:end].strip()
    return result


def seconds_from_parts(minutes: str, seconds: str, millis: str) -> float:
    return int(minutes) * 60 + int(seconds) + int(millis) / 1000


def validate(text: str, duration: float | None = None) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    normalized = text.replace("\r\n", "\n").strip()

    if "```" in normalized:
        errors.append("Remove Markdown code fences from the submission-ready prompt.")

    headers = [match.group(1) for match in HEADER_RE.finditer(normalized)]
    if headers != list(SECTIONS):
        errors.append(
            "Use exactly these section headings in order: " + ", ".join(SECTIONS) + "."
        )

    sections = split_sections(normalized)
    for name in SECTIONS:
        if not sections.get(name, "").strip():
            errors.append(f"Section '{name}' is missing or empty.")

    definitions_text = sections.get("subject_definitions", "")
    defined_tags = DEFINITION_RE.findall(definitions_text)
    if len(defined_tags) != len(set(defined_tags)):
        errors.append("Each independently tracked label must have exactly one definition line.")

    all_defined = set(defined_tags)
    source_tags = {
        match.group(0) for match in TAG_RE.finditer(definitions_text)
    } - all_defined
    later_text = "\n".join(sections.get(name, "") for name in SECTIONS[1:])
    later_tags = {match.group(0) for match in TAG_RE.finditer(later_text)}
    undefined_later = sorted(later_tags - all_defined - source_tags)
    if undefined_later:
        errors.append("Labels used later but never introduced in subject definitions: " + ", ".join(undefined_later))

    retention_text = sections.get("retention_analysis", "")
    retention_rows = RETENTION_RE.findall(retention_text)
    retention_counts: dict[str, int] = {}
    for tag, kind, marker in retention_rows:
        retention_counts[tag] = retention_counts.get(tag, 0) + 1
        allowed = AUDIO_MARKERS if kind == "Audio" else VISUAL_MARKERS
        if marker not in allowed:
            errors.append(f"Retention marker '{marker}' is invalid for {tag}.")

    for tag in defined_tags:
        count = retention_counts.get(tag, 0)
        if count != 1:
            errors.append(f"{tag} must have exactly one retention row; found {count}.")

    extra_retention = sorted(set(retention_counts) - all_defined)
    if extra_retention:
        errors.append("Retention rows use undefined labels: " + ", ".join(extra_retention))

    summary = sections.get("summary", "")
    prefix_match = re.match(r"^\[([^\]]+)\]", summary)
    if not prefix_match:
        errors.append("Summary must begin with a bracketed task-type prefix.")
    else:
        tasks = [part.strip() for part in prefix_match.group(1).split("+")]
        unknown = [task for task in tasks if task not in TASK_TYPES]
        if unknown:
            errors.append("Unknown summary task type(s): " + ", ".join(unknown))
        if len(tasks) != len(set(tasks)):
            errors.append("Do not repeat task types in the summary prefix.")
        if "video editing" in tasks:
            remainder = summary[prefix_match.end():].lstrip()
            if not remainder.startswith("The target video is an edited version of <Video 1>."):
                errors.append(
                    "A video-editing summary must begin with: "
                    "The target video is an edited version of <Video 1>."
                )

    detail = sections.get("detailed_description", "")
    for tag in sorted(source_tags):
        if tag.startswith("<Picture ") and re.search(
            rf"(?:begins from|keyframe corresponds to|ends on)\s+{re.escape(tag)}",
            detail,
            flags=re.IGNORECASE,
        ):
            errors.append(
                f"{tag} is used as a frame anchor but has no independent definition line."
            )

    shots = list(SHOT_RE.finditer(detail))
    if not shots:
        errors.append("Detailed description must contain [Shot 1].")
    else:
        shot_numbers = [int(match.group(1)) for match in shots]
        if shot_numbers != list(range(1, len(shots) + 1)):
            errors.append("Shot numbers must start at 1 and increase without gaps.")
        if shots[0].group(2) is not None:
            errors.append("[Shot 1] must not have a timestamp.")

        prior = -1.0
        for match in shots[1:]:
            if match.group(2) is None:
                errors.append(f"[Shot {match.group(1)}] must include an At MM:SS.mmm timestamp.")
                continue
            value = seconds_from_parts(match.group(2), match.group(3), match.group(4))
            if value <= prior:
                errors.append("Later-shot timestamps must be strictly increasing.")
            if duration is not None and value >= duration:
                errors.append(
                    f"[Shot {match.group(1)}] starts at {value:.3f}s, outside target duration {duration:.3f}s."
                )
            prior = value

    if detail.count("<d>") != detail.count("</d>"):
        errors.append("Dialogue tags <d> and </d> are unbalanced.")
    for dialogue in re.findall(r"<d>(.*?)</d>", detail, flags=re.DOTALL):
        if not re.match(r"\[[^\]]+\]\s+\S", dialogue.strip()):
            errors.append("Every <d> block must begin with a language tag such as [Chinese].")

    independent_picture_tags = {
        tag for tag in all_defined if tag.startswith("<Picture ")
    }
    summary_tasks = prefix_match.group(1) if prefix_match else ""
    if independent_picture_tags and "keyframe completion" not in summary_tasks:
        warnings.append("Independently defined pictures usually require 'keyframe completion'.")

    return errors, warnings


def run_self_test() -> int:
    valid = """subject_definitions:
<Subject 1> is the woman whose appearance comes from <Picture 1>.

summary:
[reference generation] The target video shows <Subject 1> greeting the morning.

retention_analysis:
<Subject 1> (appears in [Shot 1]): fully_preserved - Her identity remains consistent.

detailed_description:
The target uses realistic photography and warm daylight.
[Shot 1] <Subject 1> smiles beside a window.

overall_soundscape:
Quiet room tone and distant traffic.

non_diegetic_music:
N/A"""
    invalid = valid.replace("[reference generation]", "[video edit]").replace(
        "fully_preserved", "fully_copy"
    )
    valid_errors, _ = validate(valid, duration=5.0)
    invalid_errors, _ = validate(invalid, duration=5.0)
    if valid_errors or len(invalid_errors) < 2:
        print("SELF-TEST FAILED")
        print("valid errors:", valid_errors)
        print("invalid errors:", invalid_errors)
        return 1
    print("SELF-TEST PASSED")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prompt_file", nargs="?", help="UTF-8 prompt file; omit to read stdin")
    parser.add_argument("--duration", type=float, help="Target duration in seconds")
    parser.add_argument("--self-test", action="store_true", help="Run built-in regression tests")
    args = parser.parse_args()

    if args.self_test:
        return run_self_test()

    if args.prompt_file:
        text = Path(args.prompt_file).read_text(encoding="utf-8")
    else:
        text = sys.stdin.read()

    errors, warnings = validate(text, args.duration)
    for message in errors:
        print(f"ERROR: {message}")
    for message in warnings:
        print(f"WARNING: {message}")

    if errors:
        print(f"FAIL: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"PASS: 0 errors, {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
