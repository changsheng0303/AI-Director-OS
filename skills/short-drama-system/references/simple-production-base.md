# Simplified Production Base V1.0

This is the default contract for every project until the user explicitly requests a different architecture.

## User-visible flow

```text
1. 项目与剧本
2. 审稿定稿
3. 导演分镜
4. 视觉资产与故事板
5. 视频提示词与生成
6. 成片交付
```

The user chooses only among: full workflow, one stage, or continue project. Internal technical names are hidden unless a concrete error requires explanation.

## Project Store and minimum records

- `Canon-lite`: the approved events, exact dialogue, locked characters, and prohibited changes.
- `Scene Contract`: premise projection plus scene objective, involved characters, required Canon events/dialogue, spatial lock, tone, assets, and entry/exit state.
- `Shot Table`: source scene, duration, visible subject/action, start/end state, dialogue IDs, and asset references. It may also claim compact scene beats and carry a generation segment ID.
- `Runtime State`: current character, prop, and scene state stored as data rather than prompt prose.
- `Project Progress`: current one of six steps.
- `Revision Log` (optional): versioned upstream changes, their scope, and the downstream IDs they may affect.
- `Stale Outputs` (optional): review-only markers for outputs that may no longer match the latest approved upstream version. A marker never authorizes deletion or regeneration.
- `Basic Validation`: IDs, duration, dialogue references, asset references, adjacent shot state, and any optional beat/asset consistency fields that are present.

For source adaptation, read [novel-adaptation-mode.md](novel-adaptation-mode.md). Optional source evidence, scene beats, shot claims, and recurring-asset anchors improve verification without activating a full IR. Their absence is not a validation failure.

Do not require Foundation Hash, Narrative IR, Shot IR, Artifact Registry, State Diff, or multi-stage lock files in the default workflow. Existing full schemas remain reference material and are not automatically activated for long or multi-episode work.

Before a model works on one scene, run `scripts/select_relevant_context.py` and pass only the resulting Relevant Context View. Do not inject the complete Project Store.

After a shot or scene changes runtime state, run `scripts/state_delta.py`. The delta is infrastructure output for continuity checks; do not ask an LLM to narrate or regenerate it.

## Interaction policy

- Infer low-impact details and label assumptions briefly.
- Ask one consolidated Decision Packet only when unknowns would change genre, core relationship, ending, duration, engine, or paid/external action.
- Do not pause between internal drafting, audit, and formatting steps.
- Show current step, delivered files, material warnings, and the next action; omit internal validator names when everything passes.
- Allow direct entry at a later stage when equivalent user-approved inputs exist.
- When an upstream change occurs, preserve the old version, record the impact, and ask for one rebuild decision only after the revised upstream artifact is ready.

## Escalation

Full compiler contracts may be used only when the user explicitly asks for “完整工程模式”, “严格溯源模式”, or an equivalent requirement. Project length alone does not trigger escalation.
