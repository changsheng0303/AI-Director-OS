#!/usr/bin/env python3
"""Regression checks for screenplay/storyboard entrypoint clarity and routing."""
from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read(path):
    return (ROOT / path).read_text(encoding="utf-8-sig")

def require(text, terms, label, failures):
    missing=[term for term in terms if term not in text]
    if missing: failures.append(f"{label} missing: {', '.join(missing)}")

def main():
    failures=[]
    storyboard=read("skills/ai-video-storyboard-compiler/SKILL.md")
    screenplay=read("skills/screenplay-master/SKILL.md")
    require(storyboard,["用户说分镜","拆镜","镜头表","怎么拍","Shot","Clip Group"],"storyboard entry",failures)
    require(screenplay,["用户说写剧本","改剧本","小说改编","审稿","screenplay-node-graph.md"],"screenplay entry",failures)
    if "full-ai-video-storyboard-method.md" in storyboard: failures.append("storyboard entry still auto-loads legacy 2480-line method")
    if "### /start" in screenplay or "输入 /plan" in screenplay: failures.append("screenplay entry still requires slash-command ceremony")
    explicit=["director-mindset","storyboard-script-spec","drama-script-iteration","screenwriter-review"]
    for name in explicit:
        metadata=read(f"skills/{name}/agents/openai.yaml")
        if "allow_implicit_invocation: false" not in metadata: failures.append(f"{name} must be explicit-only")
    require(read("skills/ai-2d-animation/SKILL.md"),["只写剧本时用 screenplay-master","只做分镜时用 ai-video-storyboard-compiler"],"2D routing",failures)
    require(read("skills/seedance25-prompt-workflow/SKILL.md"),["只做生产分镜时使用 ai-video-storyboard-compiler"],"Seedance routing",failures)
    require(read("skills/universal-dialogue-core/SKILL.md"),["logical-stress-contract.md","逻辑重音属于 `DIALOGUE_CANON`"],"logical stress authority",failures)
    require(read("skills/screenplay-master/schemas/screenplay-graph.schema.json"),["logical_stress","corrective_focus","delivery"],"screenplay logical stress schema",failures)
    require(read("skills/ai-video-prompt-production/references/video-prompt-ir.md"),["logical_stress","delivery_plan","不重新推断"],"video prompt logical stress handoff",failures)
    if failures:
        print("FAIL")
        for item in failures: print("ERROR:",item)
        return 1
    print("CREATIVE_ENTRYPOINT_REGRESSION_PASS")
    return 0

if __name__=="__main__": raise SystemExit(main())
