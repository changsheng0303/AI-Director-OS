#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""H3 Ref2VA 提示词 detailed_description 词数校验（官方规范：350-500 英文词）
用法:
  python check_description_words.py <file1> [file2 ...]     # 指定文件
  python check_description_words.py "G:/path/*.txt"         # glob
  python check_description_words.py                         # 扫描当前目录 EP1_段*.txt / *Ref2VA*.txt
返回: 每文件 词数/图数/Subject数/镜数/台词数 + PASS/FAIL；有 FAIL exit 1。
"""
import re, glob, sys, os

MIN_WORDS, MAX_WORDS = 350, 550

def analyze(path):
    t = open(path, encoding="utf-8").read()
    m = re.search(r"detailed_description:\s*(.*?)(?:\noverall_soundscape:|\Z)", t, re.S)
    body = m.group(1) if m else ""
    words = len(re.findall(r"[A-Za-z]+", body))
    pics = len(set(re.findall(r"<Picture (\d+)>", t)))
    subs = len(set(re.findall(r"<Subject (\d+)>", t)))
    shots = len(re.findall(r"\[Shot \d+\]", t))
    dlg = len(re.findall(r"<d>", t))
    ok = "PASS" if MIN_WORDS <= words <= MAX_WORDS else "FAIL"
    return words, pics, subs, shots, dlg, ok

def main():
    args = sys.argv[1:]
    files = []
    for a in args:
        files.extend(glob.glob(a))
    if not files:
        files = sorted(glob.glob("EP1_段*.txt")) + sorted(glob.glob("*Ref2VA*.txt"))
    if not files:
        print("无文件可检查。用法: python check_description_words.py <file|glob> [...]")
        return 2

    rows = [(*analyze(f), os.path.basename(f)) for f in files]
    print(f"{'文件':<36} {'词数':>5} {'图':>3} {'Subj':>4} {'镜':>3} {'台词':>3} {'状态':>4}")
    print("-" * 76)
    for w, p, s, sh, d, ok, name in sorted(rows, key=lambda r: r[6]):
        print(f"{name:<36} {w:>5} {p:>3} {s:>4} {sh:>3} {d:>3} {ok:>4}")
    fails = [r for r in rows if r[5] != "PASS"]
    print("-" * 76)
    print(f"达标 {len(rows) - len(fails)} / 失败 {len(fails)} / 总计 {len(rows)}")
    return 1 if fails else 0

if __name__ == "__main__":
    sys.exit(main())
