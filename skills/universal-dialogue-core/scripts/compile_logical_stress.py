#!/usr/bin/env python3
"""Compile one DIALOGUE_CANON line into screenplay, Fountain, SSML, or plain prompt form."""
from __future__ import annotations
import argparse, json
from html import escape
from pathlib import Path

LEVEL_MAP={"light":"reduced","moderate":"moderate","strong":"strong"}
DISPLAY_MAP={"light":"轻","moderate":"中","strong":"强"}

def validate(line):
    errors=[];text=line.get("exact_text","");items=line.get("logical_stress",[])
    if len(items)>3: errors.append("logical_stress supports at most three spans")
    seen=[]
    for item in items:
        span=item.get("span","")
        if not span or span not in text: errors.append(f"stress span not found in exact_text: {span}")
        if span in seen: errors.append(f"duplicate stress span: {span}")
        seen.append(span)
        if item.get("strength") not in LEVEL_MAP: errors.append(f"invalid strength for {span}")
    return errors

def marked(text,items,style):
    for item in sorted(items,key=lambda x:len(x["span"]),reverse=True):
        span=item["span"]
        if style=="fountain": replacement=f"**_{span}_**" if item["strength"]=="strong" else f"_{span}_"
        else: replacement=f"<emphasis level=\"{LEVEL_MAP[item['strength']]}\">{escape(span)}</emphasis>"
        text=text.replace(span,replacement,1)
    return text

def compile_line(line,fmt):
    errors=validate(line)
    if errors: raise ValueError("; ".join(errors))
    text=line["exact_text"];items=line.get("logical_stress",[]);delivery=line.get("delivery",{});speaker=line.get("speaker","")
    if fmt=="fountain": return f"{speaker.upper()}\n{marked(text,items,'fountain')}"
    if fmt=="ssml":
        body=marked(escape(text),items,"ssml")
        before=int(delivery.get("pause_before_ms",0) or 0);after=int(delivery.get("pause_after_ms",0) or 0)
        if before: body=f"<break time=\"{before}ms\"/>{body}"
        if after: body=f"{body}<break time=\"{after}ms\"/>"
        attrs=[]
        if delivery.get("rate_percent") is not None: attrs.append(f"rate=\"{delivery['rate_percent']}%\"")
        if delivery.get("pitch_percent") is not None: attrs.append(f"pitch=\"{delivery['pitch_percent']:+}%\"")
        if delivery.get("volume_db") is not None: attrs.append(f"volume=\"{delivery['volume_db']:+}dB\"")
        if attrs: body=f"<prosody {' '.join(attrs)}>{body}</prosody>"
        return f"<speak>{body}</speak>"
    spans="、".join(f"“{x['span']}”({DISPLAY_MAP[x['strength']]})" for x in items) or "无额外重音"
    cue=delivery.get("visual_cue","")
    note=f"逻辑重音：{spans}"+(f"；可见动作：{cue}" if cue else "")
    if fmt=="screenplay": return f"{speaker}\n（{note}）\n{text}"
    return f"{speaker}说：“{text}” {note}。"

def main():
    parser=argparse.ArgumentParser();parser.add_argument("path");parser.add_argument("--format",choices=["screenplay","fountain","ssml","prompt"],default="screenplay");args=parser.parse_args()
    line=json.loads(Path(args.path).read_text(encoding="utf-8-sig"));print(compile_line(line,args.format));return 0
if __name__=="__main__": raise SystemExit(main())
