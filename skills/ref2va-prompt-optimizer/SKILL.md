---
name: ref2va-prompt-optimizer
description: "MiniMax H3 Full-reference Ref2VA 单条优化与校验 Overlay。格式权威来自官方 h3-prompt-writing；本Skill处理媒体关系、保真策略、修复和本地校验。多文件升级用 ref2va-batch-rewrite。"
---

# MiniMax H3 Ref2VA Prompt Optimizer

Transform an underspecified request plus reference media into a precise Ref2VA prompt. Preserve the user's intent while making only conservative, shootable additions.

## Load official upstream, then local overlay

Read `../h3-prompt-writing/SKILL.md` and `../h3-prompt-writing/references/ref-en.txt` completely before generating, rewriting, or auditing a prompt. They are the read-only official schema and format authority.

Then read [references/ref2va-spec.md](references/ref2va-spec.md) as a local operational overlay for conservative completion and validator behavior. It may clarify workflow but cannot add, remove, rename, or reorder official fields, modes, labels, timing notation, or relationship markers. On conflict, the installed official skill wins.

`references/official-ref2va-spec.txt` is a legacy absorbed snapshot and is no longer authoritative. Do not edit or consult it for current format decisions; upstream provenance is recorded by `minimax-h3-video-prompt-pipeline/references/upstream-lock.json`.

Read [references/multi-reference-fidelity.md](references/multi-reference-fidelity.md) whenever the request involves **two or more reference pictures** (character + scene + props). It is the 2026-08 user-calibrated rule set for **all-picture fidelity (v2)**: every uploaded reference picture must be recognizably preserved — one task per picture (attribute-domain separation), every picture needs at least one named appearance point in `detailed_description`, `weak_reference` is disabled by default, max 4 pictures per segment (split the segment when over — never degrade a picture), first-appearance anchor sentences, outfit-change anti-drift formula, and design-sheet view selection.

Read [references/examples.md](references/examples.md) when the request has ambiguous asset relationships, dialogue, video editing, audio reuse, or multiple shots. Use examples as patterns, not templates to copy blindly.

## Choose the operation

- **Create or optimize:** Produce a submission-ready prompt from the request and references.
- **Repair:** Keep all valid intent and wording, changing only what violates the schema or conflicts with the media relationship.
- **Audit:** Report concrete violations and their fixes. Do not rewrite unless asked.
- **Explain:** Explain the structure in the user's language, but keep any displayed final Ref2VA prompt in the required English format.

## Workflow

1. Inspect every supplied image, video, and audio asset that is relevant to the request. Never infer unseen media contents.
2. Read target duration from the request or calling environment; default to 5.00 seconds only when absent.
3. Number assets independently by type and attachment order: `<Picture N>`, `<Video N>`, and `<Audio N>`.
4. Build a private asset-role map containing: source asset, target subject, exact borrowed attributes, frame/structure role, audio role, and expected retention strength. Do not expose this map unless the user asks.
5. Select the narrowest truthful relationship:
   - Appearance, object, setting, wardrobe, or style from a picture → define it through `<Subject N>`; do not independently define the picture.
   - Actual first, key, last, editing, composition, or storyboard frame → independently define `<Picture N>` and use `keyframe completion`.
   - Motion, camera, editing rhythm, or visual reference from a video without modifying it → `reference generation`.
   - Direct modification of a source video → `video editing`.
   - Generation extending the source video's ending → `video continuation`.
   - Same audio signal retained in whole or part → `audio reuse`.
   - Only timbre, delivery, beat, style, content, or texture borrowed → `audio reference`.
6. Allocate stable `<Subject N>` labels to visible content units and `(S1)`, `(S2)` speaker IDs by first actual vocal event. A media file is not a subject.
7. Plan one coherent event across the requested duration. Give every cut a reason and ensure all later shot timestamps increase and remain within the duration.
8. Write the six required sections in order. Keep explicit dialogue, lyrics, and visible text exactly as supplied.
9. Run the silent checks in the standard. When the result is saved to a file, also run:

```powershell
python scripts/validate_ref2va_prompt.py <prompt-file> --duration <seconds>
```

10. Correct every validator error before delivery. Treat warnings as review prompts, not automatic failures.

## Output contract

For **create**, **optimize**, or **repair**, output only the finished prompt unless the user explicitly requests commentary. Do not add a title, rationale, negative prompt, parameters, Markdown fence, or translation around it.

The output must contain exactly these headings in this order:

```text
subject_definitions:
summary:
retention_analysis:
detailed_description:
overall_soundscape:
non_diegetic_music:
```

Write all six sections in English. Preserve the original language only inside dialogue, lyrics, or truly visible on-screen text.

For **audit**, lead with `PASS` or `FAIL`, then list only actionable findings with the corrected form. Do not claim to have inspected media that was not available.

If a missing asset or target duration would materially change the result, ask one concise question. If the gap is nonessential, choose a conservative default and continue.

## Non-negotiable behavior

- Never turn a mere motion or camera reference into `video editing`.
- Never claim `audio reuse` when only characteristics are referenced.
- Never create an independent `<Picture N>` definition when the image only supplies subject appearance.
- Never change explicit dialogue, lyrics, visible text, tag identity, or speaker identity.
- Never fabricate brands, characters, dialogue, lyrics, text, or reference relationships.
- Never omit a defined trackable label from `retention_analysis` or invent an undefined label later.
- Never use shot timestamps outside the actual target duration.
