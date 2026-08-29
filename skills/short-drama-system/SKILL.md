---
name: short-drama-system
description: "当用户明确要求完整项目流程、从剧本一路做到分镜/资产/视频提示词、继续现有项目或跨阶段回退时使用。只写或改剧本用 screenplay-master，只做分镜用 ai-video-storyboard-compiler。"
---

# Short Drama Director System · Simple Default

Act as the single director-facing entry point. Keep the user experience linear and readable while routing each stage to the smallest useful specialist set.

## Modes

- **全流程导演**：从创意或剧本走到交付。
- **小说改编制作**：从小说、故事或章节材料建立改编方案，再进入角色、美术、剧本与分镜；仍使用同一六步界面。
- **单点制作**：只做剧本、审稿、分镜、资产、故事板、提示词或交付中的一个阶段。
- **继续项目**：读取已有 `simple-project.json` 或已确认文件，从当前步骤继续。
- **回退修订**：切回用户指定的上游层，保留旧版本，只把真实受影响的下游标记为可能过期；未经确认不自动重做。
- **整片视觉导演**：口播、SRT、教程、评测或信息型宣传片需要画面职责分配与重点动态包装时，路由到 `reference-first-motion-director`。它拥有视觉总表和动效队列，不拥有剧情 Canon 或生产镜号。

Do not ask the user to choose internal S-stage names.

## Six-Step Flow

### 1. 项目与剧本

Turn the user's seed, reference material, or existing script into the smallest useful project direction and screenplay deliverable.

- Use `ip-foundation-engine` in lite form only when world/character foundations are missing.
- Use `screenplay-master` for general screenplay work and `micro-drama-creation` for a 50–100 episode vertical micro-drama.
- For source-novel or source-story adaptation, read [novel-adaptation-mode.md](references/novel-adaptation-mode.md). Preserve source evidence, settle cuts/merges/payoff placement before detailed episodes, and keep the result inside this same user-visible step.
- Infer low-impact details. Ask one consolidated Decision Packet only when format, core relationship, ending promise, duration, or non-negotiable Canon is genuinely ambiguous.

### 2. 审稿定稿

Use `screenwriter-review` for short-drama review. Use `universal-dialogue-core` only when dialogue is a material problem.

After approval, record Canon-lite: locked events, exact dialogue lines, locked characters, and prohibited changes. Do not require hashes or a full artifact graph.

### 3. 导演分镜

Use `ai-video-storyboard-compiler` as the sole production shot-table authority. `director-mindset` and `storyboard-script-spec` are optional lenses, not parallel outputs.

Maintain only a compact Story Map and Shot Table. Preserve dialogue and event Canon, source scene, duration, visible action, and adjacent start/end states.

For performance-critical dramatic scenes, let `ai-video-storyboard-compiler` apply its behavioral-performance reference. Performance direction may enrich visible behavior, listening, tactics, and beat changes, but it cannot change Canon dialogue or scene outcome.

When a scene has compact beat IDs, each beat must be claimed by exactly one production shot in source order. Beat claiming is an optional deterministic aid, not a requirement to expose Narrative IR.

For short-form and AI-video production, default to a **3–4 second average across the shot sequence**. This is a pacing target, never a per-shot timer. Cut only when emotion, information, subject, action phase, or eyeline/viewpoint changes; otherwise preserve the continuous shot even when it runs longer.

### 4. 视觉资产与故事板

Use `character-design-director` for approved main-character design, `ai-image-assets` for asset inventory and prompts, and `series-image-director` only for a coherent multi-image set. Add a storyboard/contact-sheet preview when it materially helps review.

Do not create full visual bibles for minor roles unless requested.

For a complete voice-over script, SRT, tutorial, review, product explanation, or other evidence-led information video, use `reference-first-motion-director` before local image generation. Its `visual-master-plan.md` decides whether each unit should remain A-roll, real evidence, screen recording, motion packaging, or a generated shot. Do not replace available evidence with decorative motion graphics.

For recurring scene and prop assets, record only useful consistency metadata: two to five recognizable anchors, production-used states, scale for props, and `variant_of` when an asset intentionally reuses a parent design. Do not force these fields onto one-off assets.

### 5. 视频提示词与生成

Ask for the target engine only if it is not already known:

- MiniMax H3: `h3-video-prompt-workflow` for one item, `minimax-h3-video-prompt-pipeline` for multi-shot work, with official `h3-prompt-writing` as format authority.
- Seedance: `seedance25-prompt-workflow`; add `micro-expression-video-prompts` only for performance-critical shots.
- Fafajing: `fafajing-prompt-writer` only when explicitly selected.

Validate format and references without exposing the full internal validator stack when everything passes.

For Seedance shots whose failure risk is mainly first-frame occupancy, spatial blocking, eyeline, landmark distance, prop handling, physical motion, or light direction, use the single-shot physical-control reference inside `seedance25-prompt-workflow`. Do not import obsolete engine syntax from another workflow.

### 6. 成片交付

Return the generated or generation-ready files, shot order, editing notes, audio/subtitle requirements, material warnings, and a concise next action. External submission, publishing, purchases, or paid generation still require the user's authorization.

## Simplified Base

Read [simple-production-base.md](references/simple-production-base.md) when starting or continuing a project.

Default internal record: `simple-project.json`, which acts as the Project Store and is validated by `scripts/validate_simple_project.py`.

It contains only:

- Canon-lite;
- thin Scene Contract;
- runtime character/prop/scene state;
- Shot Table, with optional compact beat claims and generation segment IDs;
- asset list, with optional anchors/states/variants for recurring assets;
- prompt jobs;
- one of six current steps;
- material warnings.

Optional revision records preserve upstream changes and identify only the downstream outputs that may be stale. A stale mark is a review state, not permission to delete or regenerate an output.

Before a director, prompt adapter, or reviewer handles one scene, run `scripts/select_relevant_context.py` and supply only that scene's Canon events, dialogue, runtime state, assets, and shots. After state changes, compute `scripts/state_delta.py` in code; the delta is not an LLM workflow step.

Run `scripts/validate_simple_project.py` after structural edits. It checks ordinary references and duration plus any optional source facts, beat claims, segment grouping, and asset consistency metadata that are present. A missing optional layer is not an error.

When source review, validation, user feedback, or actual generated media exposes a concrete failure, read [production-failure-loop.md](references/production-failure-loop.md) and record evidence in the project or repository failure registry. Repair the current project first. Do not turn one model failure or one creative preference into a universal rule; promote repeated failures only with evidence and a regression fixture.

Foundation Hash, Narrative IR, Shot IR, Artifact Registry, State Diff, and multi-stage lock files are not required by default, including for long or multi-episode projects.

## Interaction Rules

1. Never pause between internal drafting, audit, formatting, or validation.
2. Never ask again for information already present in conversation or project files.
3. Combine all material unknowns for the current user-visible step into one Decision Packet.
4. When the user delegates a decision, choose a sensible default and record it as an assumption.
5. Show only: current step, deliverable, material warnings, and next action.
6. Load one primary specialist and at most two supporting specialists per step.
7. Allow direct entry at any user-requested stage when the supplied material is sufficient; do not force unrelated upstream work.
8. On an upstream revision, version the changed artifact, record the impact, and wait for the user's rebuild choice before changing downstream deliverables.

Read [integrated-routing-map.md](references/integrated-routing-map.md) when deciding between narrative production, information-video editorial planning, performance enrichment, and single-shot engine control.
Read [imported-ai-studio-film-suite-map.md](references/imported-ai-studio-film-suite-map.md) when maintaining or auditing the imported nine-Skill film-suite integration.
Read [screenplay-storyboard-node-bridge.md](references/screenplay-storyboard-node-bridge.md) when a confirmed screenplay flows into production storyboards or an upstream revision invalidates only part of the shot graph.

## Optional Full Engineering Reference

Do not enable the former full compiler automatically. Read [full-orchestrator-v5.2.md](references/full-orchestrator-v5.2.md) only when the user explicitly requests “完整工程模式”, “严格溯源模式”, or equivalent audit-grade traceability.
