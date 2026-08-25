#!/usr/bin/env python3
"""Report detailed_description word counts and quick spec checks for Ref2VA prompt files.

Batch-rewrite companion: after rewriting N Ref2VA files, run this over them to
report each file's detailed_description word count (official target 350-500
English words for generation tasks) and spot-check schema compliance.

Usage:
    python count_dd_words.py <prompt-file> [<prompt-file> ...] [--duration N]

--duration N  target video length in seconds; enables the timestamp-inside-
              duration check (default: off).
"""
import re
import sys

WORDS_RE = re.compile(r"[A-Za-z][A-Za-z'\-]*")
SHOT_RE = re.compile(r"\[Shot (\d+)\](?: At ([\d:.]+))?")
DD_RE = re.compile(r"detailed_description:\n(.*?)\noverall_soundscape:", re.S)


def analyze(path):
    with open(path, encoding="utf-8") as fh:
        txt = fh.read()
    m = DD_RE.search(txt)
    dd = m.group(1).strip() if m else ""
    return txt, dd


def main():
    args = sys.argv[1:]
    duration = None
    if "--duration" in args:
        i = args.index("--duration")
        duration = float(args[i + 1])
        del args[i:i + 2]
    if not args:
        print(__doc__)
        return 1
    for path in args:
        txt, dd = analyze(path)
        n = len(WORDS_RE.findall(dd))
        shots = SHOT_RE.findall(dd)
        # NOTE: re.findall returns '' (not None) for unparticipating optional
        # groups, so Shot 1's missing timestamp arrives as ''. Check `ts != ""`.
        ts_ok, prev = True, 0.0
        for num, ts in shots:
            num = int(num)
            if num == 1 and ts != "":
                ts_ok = False
            if num > 1:
                if ts == "":
                    ts_ok = False
                else:
                    p = ts.split(":")
                    secs = int(p[0]) * 60 + float(p[1])
                    if secs <= prev or (duration is not None and secs >= duration):
                        ts_ok = False
                    prev = secs
        # Speaker check: every <d>[Chinese] dialogue tag must be preceded by
        # "<Subject N> (Sx) says". Segments with NO dialogue pass automatically
        # (all() over an empty sequence is True).
        spk_ok = all(
            re.search(r"\(S\d\) says", txt[max(0, m.start() - 160):m.start()])
            for m in re.finditer(r"<d>\[Chinese\]", txt)
        )
        checks = {
            "word_count_350_500": 350 <= n <= 500,
            "summary_prefix_[reference generation]": "[reference generation]" in txt,
            "style_has_streak_hair_highlights": "streak hair highlights" in dd,
            "timestamps_ok": ts_ok,
            "no_weak_reference": "weak_reference" not in txt,
            "speaker_(Sx)_says_before_<d>": spk_ok,
        }
        status = "PASS" if all(checks.values()) else "FAIL " + str(
            [k for k, v in checks.items() if not v]
        )
        print(f"{path}: {n} words  {status}")


if __name__ == "__main__":
    sys.exit(main())
