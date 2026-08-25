---
name: fafajing-prompt-writer
description: "用户明确指定 fafajing 时，将创意或 Video Prompt IR 编译为其中文 Basic/Full-reference 提示词，支持首帧、尾帧、首尾帧、编辑、续写和音频复用；不处理 H3 或 Seedance。"
---

# fafajing的提示词生成 (Fafajing Video Prompt Writer)

## Overview

Compile a user's rough idea, supplied assets, or a system Video Prompt IR into the Fafajing prompt format. This skill is the **Fafajing Adapter**: it owns Fafajing's Chinese body, exact templates, and Basic/Full-reference formatting, but does not define H3 or Seedance output. It covers **basic mode** (T2VA / I2VA / FL2VA / L2VA) and **full-reference mode** (multi-asset reference generation, video editing, video continuation, audio reuse/reference).

When invoked from `ai-video-prompt-production`, read `ai-video-prompt-production/references/video-prompt-ir.md` and preserve its mode, asset roles, frame anchors, dialogue, and sound relationships. For a direct Fafajing request without IR, perform the same determination locally using Step 1. Never export Fafajing's Chinese-language or length requirements as cross-engine rules.

Two bundled guides are the single source of truth for all format rules:

- `references/VIDEO_PROMPT_WRITING_GUIDE_base_en.md` — basic-mode rules: prompt structure, shot/cut format, camera-motion vocabulary, speaker IDs, dialogue `<d>` tags, soundscape and music sections, plus four worked cases.
- `references/VIDEO_PROMPT_WRITING_GUIDE_ref_en.md` — full-reference-mode rules: reference labels (`<Subject N>` / `<Picture N>` / `<Video N>` / `<Audio N>`), the six output sections, task-type prefixes, and retention-analysis markers.

Follow the workflow below in order. Do not skip Step 1 (mode determination).

## Step 1: Determine the Mode (Mandatory First Step)

Before writing anything, decide whether the task is **full-reference mode** or **basic mode**. Never guess silently when the evidence is ambiguous — ask the user to confirm.

### Basic mode signals

The task is basic mode when the only inputs are the user's text and at most simple keyframe images, with no request to reuse content across assets:

| Inputs | Sub-mode |
|---|---|
| Text only, no reference image | **T2VA** |
| One image used as the first frame (0.00 s) | **I2VA** |
| Two images, first frame + last frame | **FL2VA** |
| One image used as the last frame | **L2VA** |

### Full-reference mode signals

Treat the task as full-reference mode when ANY of the following holds:

- Multiple reference assets of mixed types (images + videos + audio) are provided.
- An existing source video must be **edited** or **continued/extended**.
- An audio asset must be **copied** (fully/partially) or **referenced** (timbre, music style, dialogue content, beat).
- Specific subjects (person, animal, object, scene, costume, style) from reference assets must be **tracked and reused** across shots.
- The user asks for a `subject_definitions` / `retention_analysis` style output, or mentions "全参考模式" / "full-reference mode" / "reference generation".
- A reference image serves as a storyboard / shot-planning anchor rather than a plain first frame.

### Full-reference mode without image assets

When the user explicitly requests Fafajing full-reference formatting without supplying images, define trackable subjects textually and keep labels consistent. Do not invent image bindings; note that real `<Picture N>` references can be added after assets are supplied.

**Reference-image sourcing rule (mandatory):** every `<Picture N>` must point to an actual reference image the user provided — in full-pipeline mode, only assets listed in the asset list produced by the asset-generation stage (characters / scenes / props / mood boards). Never reference or fabricate images outside the asset library. If a subject has no corresponding image in the library, either ask the user to add that asset first, or define the subject textually in `subject_definitions` without inventing a `<Picture N>`.

**Independent numbering rule (mandatory):** the asset list is a source of reference images only — it never fixes label numbers. In each prompt (each full six-section output), `<Subject N>` / `<Picture N>` numbering restarts at 1 and follows first-appearance order within that prompt; it does not continue the asset-list order or the numbering of any previous prompt.

### When ambiguous

If the inputs could fit either mode (e.g., several images that might be keyframes or subject references), present the determination briefly and ask the user to confirm before proceeding. State the inferred mode and the reason in one or two sentences.

## Step 2: Collect Inputs

Gather the following from the user's message and uploaded files. Ask only for what is genuinely missing and blocking.

1. **Initial prompt** — the user's raw idea, plot, or shot notes (required).
2. **Assets and their roles** — for each uploaded file, establish its role:
   - Image: first frame / last frame / keyframe / subject reference / scene or style reference / storyboard.
   - Video: edit source / continuation base / camera-rhythm-structure reference / subject source.
   - Audio: full or partial copy / voice-timbre reference / music-style reference / dialogue source.
   - Full-reference mode with no image assets: derive subjects from the script or storyboard, define them textually, and note that real `<Picture N>` bindings can be added later.
3. **Target duration** — required for cut timestamps and for FL2VA/L2VA alignment instructions (`S.SS` with exactly two decimals). Ask if missing; propose a sensible default (e.g., 5–10 s) when the user has no preference.
4. **Dialogue / lyrics** — exact original words and language, verbatim. Never translate or rewrite spoken content. Ask for the exact lines when the user only paraphrases.
5. **On-screen text** — signs, banners, subtitles visible in frame, verbatim.
6. **Style and sound preferences** — visual style (e.g., cinematic, live-action, 2D-animated, 3D CG), ambience, and whether non-diegetic music exists (`N/A` if none).

Read image assets with the Read tool to extract style, subjects, composition, clothing, colors, and spatial anchors before writing. For video/audio assets, rely on the user's description of their content and role unless a tool is available to inspect them.

## Step 3: Load the Applicable Guide(s)

- Always read `references/VIDEO_PROMPT_WRITING_GUIDE_base_en.md` first — its shot, camera, speaker, dialogue, and sound rules apply to BOTH modes.
- In full-reference mode, additionally read `references/VIDEO_PROMPT_WRITING_GUIDE_ref_en.md` and follow its label, summary, and retention-analysis rules exactly.

## Step 4: Write the Output

Write the entire prompt in Chinese (简体中文). Keep every format element unchanged: section field names (`subject_definitions:` / `summary:` / `retention_analysis:` / `detailed_description:` / `overall_soundscape:` / `non_diegetic_music:` and the basic-mode fields `integrated_multimodal_description:`), shot/cut markers (`[Shot 1]`, `[Shot N] At MM:SS.mmm`), reference labels (`<Subject N>` / `<Picture N>` / `<Video N>` / `<Audio N>`), speaker IDs (`(S1)`, `(S2)`), the camera-motion vocabulary, the fixed relationship markers, and the I2VA / FL2VA / L2VA instruction templates. The English examples in the guides show the format structure only — the actual body text must be written in Chinese. Preserve the original language only inside `<d>` dialogue/lyric blocks and for text visibly present in the scene.

### Basic mode output structure

```text
<image-alignment instruction line — required for I2VA / FL2VA / L2VA, omitted for T2VA>

integrated_multimodal_description: [Shot 1] ... [Shot 2] At MM:SS.mmm, ...

overall_soundscape: ...

non_diegetic_music: ...
```

- Use the exact instruction templates from the base guide §2.1 for I2VA / FL2VA / L2VA, with `N` = actual final shot index and `S.SS` = effective duration to two decimals.
- Follow the recommended narrative structure per sub-mode (base guide §3): I2VA = first-frame anchor → action onset → development → result; FL2VA = first-frame state → intermediate changes → narrowing differences → last-frame state; L2VA = plausible preceding state → transition path → convergence → last-frame landing.

### Full-reference mode output structure

Produce all six sections in order:

```text
subject_definitions: ...
summary: [<task types joined with +>] ...
retention_analysis: ...
detailed_description: ...
overall_soundscape: ...
non_diegetic_music: ...
```

- Assign each tracked asset a label (`<Subject N>` / `<Picture N>` / `<Video N>` / `<Audio N>`) per ref guide §2 and reuse it consistently everywhere.
- In Fafajing full-reference mode without reference images, define subjects textually and still emit all six sections; every later `<Subject N>` must be defined, and retention markers still apply.
- Only reference images actually supplied by the user (or listed in the asset library) may receive a `<Picture N>` label; never fabricate a `<Picture N>` for an unknown image. Missing assets must be flagged for the user to provide, not guessed.
- Numbering is local to each prompt: labels always restart at `<Subject 1>` / `<Picture 1>` in first-appearance order; never inherit numbering from the asset list or from an earlier prompt.
- Choose `summary` task types strictly from the ref guide §3 table (`keyframe completion`, `reference generation`, `video editing`, `video continuation`, `audio reuse`, `audio reference`).
- Use only the fixed relationship markers in `retention_analysis`: `fully_preserved` / `partially_preserved` / `attribute_transfer` / `weak_reference` for visible content; `fully_copy` / `partially_copy` / `reference` / `weak_reference` for audio.
- Keep `detailed_description` at roughly 350–500 Chinese characters (汉字字数) for generation tasks (ref guide §5.2).

### Formatting rules that apply to both modes

- `[Shot 1]` carries no timestamp; later shots start with `[Shot N] At MM:SS.mmm,` and strictly increasing cut times within the video duration.
- Write camera motion using only the guide's fixed English vocabulary (motion type + optional `with small/large amplitude` + optional `at slow/fast speed`), embedded naturally within the Chinese body text; do not translate or rename these motion terms.
- Assign stable speaker IDs `(S1)`, `(S2)` in order of first vocal event; write dialogue as `<d>[Language] verbatim words</d>`; use `says in an off-screen voiceover` plus a "lips remain closed" statement for voiceover; use `<scenetrans>` / `<cutoff>` for dialogue crossing cuts or truncated by the ending.
- Put visible on-screen text in English double quotation marks, verbatim.
- `overall_soundscape`: 1–4 sentences, ambience + physical sounds only, no dialogue/music. `non_diegetic_music`: 1–3 sentences on instrumentation, tempo, dynamics; `N/A` when absent.

## Step 5: Verify Before Delivering

Check the draft against this list, fix any violation, then present the final prompt in a single code block:

- [ ] Body text is written in Chinese (简体中文) while every format element (field names, shot/cut markers, labels, speaker IDs, camera-motion terms, fixed markers, instruction templates) remains in its fixed English form.
- [ ] Mode (basic sub-mode vs full-reference) matches the confirmed determination.
- [ ] Instruction line (I2VA/FL2VA/L2VA) uses the exact template, with correct shot index and `S.SS` duration.
- [ ] All required sections are present, in order, with exact field names.
- [ ] Cut timestamps are strictly increasing and within the duration.
- [ ] Dialogue is verbatim, in the original language, inside `<d>` with a language tag.
- [ ] Speaker IDs are stable and consistent across shots and sections.
- [ ] Full-reference mode: every label in later sections was defined in `subject_definitions`; no new labels appear later; `(Sx)` never appears in `retention_analysis`.
- [ ] Keyframe consistency: identity, clothing, colors, props, and spatial relations from reference images are preserved explicitly.
- [ ] `overall_soundscape` contains no dialogue or music; `non_diegetic_music` describes only audience-only score (or `N/A`).

Deliver the final prompt as a copyable code block, optionally with a one-paragraph summary of the mode and key decisions in the user's language.

## Resources

### references/

- `VIDEO_PROMPT_WRITING_GUIDE_base_en.md` — the authoritative basic-mode specification (T2VA / I2VA / FL2VA / L2VA): structure, camera vocabulary, speakers, dialogue, sound, and four complete cases. Read for every task.
- `VIDEO_PROMPT_WRITING_GUIDE_ref_en.md` — the authoritative full-reference-mode specification: reference labels, six-section output, task types, retention markers, and a complete example. Read when Step 1 determines full-reference mode.
