---
name: ai-video-storyboard-compiler
description: "将已确认剧本或场景编译为连续性安全、可供 AI 视频生成的分镜片段，包含时长、机位、运动、表演、声音、参考图和镜头衔接。用于剧本转 AI 视频分镜；不写纯剧本或最终 H3/Ref2VA 提示词。"
---

# AI Video Storyboard Compiler

Compile dramatic text into the smallest useful set of shots an AI video pipeline can execute without losing story, emotion, or continuity.

## Routing

- For a conventional director's shot table without AI-generation fields, use the dedicated director/storyboard method instead.
- For final model-specific H3 or Ref2VA syntax, hand the approved storyboard to the relevant prompt optimizer.
- Use this skill when the missing layer is the structured bridge between screenplay and generation prompt.
- This skill is the sole production authority for shot numbering, duration, and the simplified Shot Table; it also owns optional full Shot IR when explicitly requested. `director-mindset` may inform creative choices and `storyboard-script-spec` may audit continuity, but neither should emit a parallel production shot table.

## Workflow

1. Confirm the source scene, intended duration, aspect ratio, visual medium, available reference images, and whether dialogue, voice-over, subtitles, or music are allowed. Infer safe defaults when they do not materially change the result.
2. Read [full-ai-video-storyboard-method.md](references/full-ai-video-storyboard-method.md) completely. Use its phase system, field definitions, continuity rules, and audiovisual translation library selectively; do not force its legacy self-check ritual or command syntax on the user.
3. Treat the approved screenplay as `SCRIPT_CANON`. When `universal-dialogue-core` produced a separate `DIALOGUE_CANON`, consume its line IDs and exact text as read-only. Compute or record source hashes and never silently change plot, dialogue, named entities, or scene order.
4. Default to a compact Story Map: premise, protagonist, objective, conflict, emotional change, and scene entry/exit summaries. Narrative IR is optional and must not be generated automatically unless the user explicitly requests full engineering mode.
5. Build Runtime Map and Scene Geography before asset generation: lock entrances, exits, anchors, axis, screen direction, light, weather, and initial blocking. Emit asset requirements from this locked geography.
6. Consume the approved visual asset list. Do not redesign a character, scene, or prop inside the Shot Table.
7. Divide the scene into generation-sized segments based on action and transition logic, not an arbitrary fixed shot count. For short-form and AI-video work, target a **3–4 second average across the sequence**, but never cut merely because a timer reached that range.
8. Cut only when at least one primary condition changes: emotion, information, subject, action phase, or eyeline/viewpoint. For each shot, emit the simplified Shot Table fields: shot ID, source scene, duration, primary `cut_motivation`, subject, visible action, start/end state, dialogue IDs, and asset references. The first shot of a scene may use `scene_entry`. Emit full Shot IR, provenance, and renderer blocks only in explicit full engineering mode.
9. Maintain screen direction, eyelines, action matching, prop state, lighting, costume, geography, and emotional carry-over. Add a handoff card between independently generated segments.
10. Run a final film-in-the-head pass and basic validation: IDs, total duration, exact dialogue references, asset references, and adjacent start/end states. Full Narrative/Shot IR gates are optional.
11. If human review or actual generated media exposes a reproducible storyboard failure, return the affected shot/segment IDs, observed evidence, repair, and regression target to the orchestrator's failure registry. Do not generalize a single aesthetic preference into a global cutting rule.

## Output Contract

- Lead with a short scene and continuity map, followed by the storyboard table and cross-segment handoffs.
- Preserve `DIALOGUE_CANON.exact_text` verbatim. Design pauses, interruptions, reactions and optional micro-actions around it; any wording change requires an approved Dialogue Change Request rather than an inline rewrite.
- Treat the 3–4 second average as an advisory sequence metric. Allow shorter inserts and reactions, and longer dialogue, silence, continuous blocking, establishing, or emotional holds when the content has not yet completed. Reject timer-only cuts.
- Mark missing references explicitly; never pretend an unattached image was inspected.
- Keep model-specific suffixes separate from dramatic shot content.
- In default mode, update `simple-project.json`. In explicit full engineering mode, add source hashes, Narrative IR, Shot IR, renderer adapter, and approved change IDs.
