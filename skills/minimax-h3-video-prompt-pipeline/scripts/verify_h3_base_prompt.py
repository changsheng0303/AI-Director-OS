#!/usr/bin/env python3
"""Validate the official H3 base-mode field layout and shot timing."""

import argparse
import io
import re
import sys

FIELDS = ["integrated_multimodal_description:", "overall_soundscape:", "non_diegetic_music:"]
REF_FIELDS = ["subject_definitions:", "summary:", "retention_analysis:", "detailed_description:"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prompt")
    parser.add_argument("--mode", required=True, choices=["T2VA", "I2VA", "FL2VA", "L2VA"])
    parser.add_argument("--duration", required=True, type=float)
    args = parser.parse_args()
    text = io.open(args.prompt, encoding="utf-8").read()
    errors = []

    if not 4 <= args.duration <= 15:
        errors.append("official H3 base duration must be within 4-15 seconds")
    counts = [len(re.findall(rf"^{re.escape(field)}", text, re.M)) for field in FIELDS]
    positions = [text.find(field) for field in FIELDS]
    if counts != [1, 1, 1]:
        errors.append(f"base prompt must contain each core field exactly once; counts={counts}")
    elif not positions[0] < positions[1] < positions[2]:
        errors.append("base prompt fields are out of order")
    if any(re.search(rf"^{re.escape(field)}", text, re.M) for field in REF_FIELDS):
        errors.append("Ref2VA-only top-level fields found in a base-mode prompt")
    if "```" in text:
        errors.append("Markdown fences are not allowed in a submission-ready prompt")

    first_nonempty = next((line.strip() for line in text.splitlines() if line.strip()), "")
    if args.mode == "T2VA":
        if not first_nonempty.startswith("integrated_multimodal_description:"):
            errors.append("T2VA must begin with integrated_multimodal_description")
    elif args.mode == "I2VA":
        if not first_nonempty.startswith("For the target video, at 0.00 seconds"):
            errors.append("I2VA must begin with the official first-frame alignment instruction")
    else:
        if not first_nonempty.startswith("How the reference pictures align with the target video"):
            errors.append(f"{args.mode} must begin with the official frame-alignment instruction")

    body_match = re.search(r"integrated_multimodal_description:\s*(.*?)(?:\noverall_soundscape:)", text, re.S)
    if not body_match:
        errors.append("integrated_multimodal_description body missing")
    else:
        body = body_match.group(1)
        shots = re.findall(r"\[Shot (\d+)\](?: At (\d+):(\d+)\.(\d+))?", body)
        if not shots:
            errors.append("no shots found")
        previous = 0.0
        for expected, (number, minute, second, millis) in enumerate(shots, start=1):
            if int(number) != expected:
                errors.append("shot numbers must be sequential")
                break
            if expected == 1:
                if minute:
                    errors.append("Shot 1 must not have a timestamp")
                continue
            if not minute:
                errors.append(f"Shot {expected} requires a timestamp")
                continue
            value = int(minute) * 60 + int(second) + int(millis) / 1000.0
            if value <= previous or value >= args.duration:
                errors.append(f"Shot {expected} timestamp must increase and remain inside duration")
            previous = value

    for error in errors:
        print(f"[ERROR] {error}")
    if errors:
        print(f"FAIL: {len(errors)} error(s)")
        return 1
    print(f"PASS: mode={args.mode}, duration={args.duration}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
