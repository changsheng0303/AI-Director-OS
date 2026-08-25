#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Read-back spec verification for a batch of Ref2VA prompt files.

Run AFTER the files were written, read-back style (never trust the write buffer),
and iterate until every file PASSes. Complements validate_ref2va_prompt.py
(single-prompt syntax) with batch conformance + word-count checks.

Per-file checks:
  1. six official sections appear once, in the required order
  2. summary starts with a bracketed task-type prefix, e.g. [reference generation]
  3. [Shot N] timestamps strictly increase and each cut lies inside the duration
  4. every retention_analysis line targets a <Subject N> with a legal marker
  5. no 'weak_reference' anywhere (multi-reference fidelity: disabled by default)
  6. no standalone '<Picture N>' definition line (pictures cited inside subjects only)
  7. optional caller-supplied style fragment is present
  8. dialogue lines carry a speaker ID ('<Subject N> (Sx) ... <d>[Lang] ...</d>')
     and match expected verbatim text when expectations are supplied
  9. detailed_description English word count within [--min-words, --max-words]

Word count method: whitespace tokens in the detailed_description section that
contain at least one ASCII letter. Chinese <d> dialogue is ~1 token per line and
does not inflate the count.

Usage:
  python verify_ref2va_batch.py FILE [FILE ...] \
      [--duration N]                  # one shared duration (seconds) for all files
      [--durations-json '{"01":7}']   # per-segment durations keyed by 段NN in filename
      [--expect-json '{"EP1_段04_x.txt": ["台词1"]}']  # verbatim dialogue keyed by basename
      [--min-words 350] [--max-words 500] [--require-style TEXT]
      [--require-style 'streak hair highlights']
Exit code 0 = all PASS, 1 = any FAIL.
"""
import argparse
import io
import json
import os
import re
import sys

SECS = ["subject_definitions:", "summary:", "retention_analysis:",
        "detailed_description:", "overall_soundscape:", "non_diegetic_music:"]
MARKERS = {"fully_preserved", "partially_preserved", "attribute_transfer", "weak_reference"}


def parse_args():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("files", nargs="+", help="prompt files to verify")
    p.add_argument("--duration", type=float, default=None,
                   help="shared target duration in seconds for all files")
    p.add_argument("--durations-json", default=None,
                   help="per-segment durations, e.g. '{\"01\":7}' keyed by 段NN in filename")
    p.add_argument("--expect-json", default=None,
                   help="verbatim dialogue expectations keyed by basename, e.g. "
                        "'{\"seg04.txt\": [\"唉！\"]}'")
    p.add_argument("--min-words", type=int, default=350)
    p.add_argument("--max-words", type=int, default=500)
    p.add_argument("--require-style", default=None,
                   help="optional project-specific style fragment; no style is forced by default")
    return p.parse_args()


def seg_key(path):
    name = os.path.basename(path)
    m = re.search(r"段(\d+)", name)
    if not m:
        m = re.search(r"(?:^|[_-])(?:H3[_-]?)?(\d{1,4})(?:[_-]|\.)", name, re.I)
    return m.group(1) if m else None


def check_file(path, durations, expect, minw, maxw, style):
    txt = io.open(path, encoding="utf-8").read()
    issues = []

    counts = [len(re.findall(rf"^{re.escape(s)}\s*$", txt, re.M)) for s in SECS]
    idx = [txt.find(s) for s in SECS]
    if any(c != 1 for c in counts):
        issues.append(f"each official section must appear exactly once; counts={counts}")
    elif any(idx[i] >= idx[i + 1] for i in range(5)):
        issues.append("six sections out of order")

    sm = re.search(r"^summary:\s*\n\s*(\[[^\]]+\])", txt, re.M)
    if not sm:
        issues.append("summary missing bracketed task-type prefix")

    dd = re.search(r"detailed_description:\n(.*?)\noverall_soundscape:", txt, re.S)
    en = None
    if not dd:
        issues.append("detailed_description section missing")
    else:
        body = dd.group(1).strip()
        dur = durations.get(seg_key(path), durations.get("__all__", 5.0))

        shot_matches = re.findall(r"\[Shot (\d+)\](?: At (\d+):(\d+)\.(\d+))?", body)
        prev, ts_ok = 0.0, bool(shot_matches)
        expected_shot = 1
        for n, h, m_, ms in shot_matches:
            if int(n) != expected_shot:
                ts_ok = False
            expected_shot += 1
            if n == "1":
                if h != "":
                    ts_ok = False
                continue
            if h == "":
                ts_ok = False
                continue
            t = int(h) * 60 + int(m_) + int(ms) / 1000.0
            if t <= prev or t >= dur:
                ts_ok = False
            prev = t
        if not ts_ok:
            issues.append(f"shots must be sequential; Shot 1 has no timestamp; later timestamps increase inside {dur}s")

        ret = re.findall(r"^<([^>]+)> \(appears in \[Shot [^\]]+\](?:, \[Shot [^\]]+\])*\): ([a-z_]+) -",
                         txt, re.M)
        if not ret:
            issues.append("no retention_analysis subject lines found")
        for label, marker in ret:
            if not label.startswith("Subject"):
                issues.append(f"retention line targets non-subject label <{label}>")
            if marker not in MARKERS:
                issues.append(f"retention line uses illegal marker '{marker}'")

        definitions_body = re.search(r"subject_definitions:\s*\n(.*?)\nsummary:", txt, re.S)
        if definitions_body:
            defined_subjects = re.findall(r"^<(Subject \d+)>", definitions_body.group(1), re.M)
            retained_subjects = [label for label, _ in ret if label.startswith("Subject")]
            if len(defined_subjects) != len(set(defined_subjects)):
                issues.append("duplicate Subject definition")
            if sorted(defined_subjects) != sorted(retained_subjects):
                issues.append(f"Subject definitions/retention mismatch: defined={defined_subjects}, retained={retained_subjects}")

        if "weak_reference" in txt:
            issues.append("contains weak_reference (disabled by default)")

        if re.search(r"^<Picture \d+>", txt, re.M):
            issues.append("standalone <Picture N> definition present (should be cited inside a subject)")

        if style and style not in body:
            issues.append(f"style sentence fragment '{style}' not found in detailed_description")

        got = re.findall(r"<Subject \d+> \((S\d+)\) .*?<d>\[[A-Za-z]+\] (.+?)</d>", body)
        exp = expect.get(os.path.basename(path))
        if exp is not None:
            got_texts = [d for _, d in got]
            if got_texts != exp:
                issues.append(f"dialogue mismatch: got {got_texts}, expected {exp}")

        en = len([t for t in body.split() if re.search(r"[A-Za-z]", t)])
        if not (minw <= en <= maxw):
            issues.append(f"detailed_description word count {en} outside [{minw},{maxw}]")

    return issues, en


def main():
    args = parse_args()
    durations = {}
    if args.durations_json:
        durations = {k: float(v) for k, v in json.loads(args.durations_json).items()}
    if args.duration is not None:
        durations = {"__all__": args.duration}

    expect = json.loads(args.expect_json) if args.expect_json else {}

    allpass = True
    for path in args.files:
        issues, en = check_file(path, durations, expect,
                                args.min_words, args.max_words, args.require_style)
        status = "PASS" if not issues else "FAIL"
        if issues:
            allpass = False
        suffix = f" | words={en}" if en is not None else ""
        print(f"[{status}] {path}{suffix}")
        for i in issues:
            print(f"    - {i}")
    sys.exit(0 if allpass else 1)


if __name__ == "__main__":
    main()
