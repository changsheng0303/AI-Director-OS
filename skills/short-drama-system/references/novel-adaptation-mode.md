# Novel Adaptation Mode

Use this mode only when the project adapts a supplied novel, story, chapter set, synopsis, or other source narrative. Keep it inside the ordinary six-step director flow.

## Compact workflow

1. Read only the source material actually supplied. Never infer plot from a title or reputation.
2. Record decisive source facts in optional `canon_lite.fact_basis` entries. Use `source_evidence` with a short exact excerpt when a cut, merge, identity, relationship, or payoff decision depends on the source. Use `ai_proposal` for creative additions that the user has not approved.
3. Build a fast adaptation skeleton before detailed episodes: core promise, retained line, removed line, merged roles, main payoff placement, recurring locations, and narrative props.
4. Ask for one consolidated decision only when cuts, merges, ending promise, format, or duration would materially change the adaptation. Do not stop for minor names, decoration, or prop styling.
5. After direction is settled, let existing specialists do their own jobs:
   - `screenplay-master` or `micro-drama-creation`: adaptation structure and screenplay;
   - `character-design-director`: approved main-character depth and visual identity;
   - `anime-scene-asset-design` / `ai-image-assets`: recurring scene and prop assets;
   - `ai-video-storyboard-compiler`: production shots and continuity;
   - official H3 or selected engine adapter: final prompt format.
6. Keep machine handoffs compact. Add optional scene beats only when downstream shot coverage needs mechanical verification. Add asset anchors/states only to recurring production assets.
7. Run the simple-project validator after changes. Fix broken IDs, missing beat coverage, duplicated claims, invalid variants, or segment discontinuity in code. Use semantic review for whether the adaptation is dramatically good.

## Boundaries

- Do not install or invoke parallel `novel-*` skills merely because the source is a novel.
- Do not create a full lorebook, Narrative IR, Shot IR, dependency graph, or hash chain by default.
- Do not treat timing heuristics, hook placement, cut length, cast limits, or visual styles as universal rules. Apply platform or engine profiles only when the project actually selects them.
- Do not maintain a private H3 format here. The installed official H3 skill remains authoritative.

## Optional data additions

Use only what the project needs:

- `canon_lite.fact_basis[]`: `fact_id`, `value`, `authority`, optional `evidence`;
- `story_map.scenes[].beats[]`: `beat_id`, `kind`, `summary`, optional `dialogue_id`;
- `shots[].beat_refs`: beat IDs claimed by that shot, in source order;
- `shots[].segment_id`: groups consecutive shots intended for one generation call;
- recurring `assets[]`: optional `anchors`, `states`, `variant_of`, and `scale`.

These fields are a compact verification layer, not a second user-facing workflow.
