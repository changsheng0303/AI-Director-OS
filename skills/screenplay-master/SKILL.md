---
name: screenplay-master
description: "创建、规划、修改或评估中英文影视剧本，包括短剧、微短剧、竖屏剧、剧情短视频、剧情广告、宣传片、分集大纲、节拍、钩子、反转、人物弧和剧本诊断。仅用于剧本化内容，不用于普通散文、非剧情广告文案、新闻、学术或纯市场/法律分析。"
---

# Screenplay Master

Use this skill to turn a premise, product, draft, IP outline, campaign goal, or series concept into a shootable screenplay or review report. Keep `SKILL.md` lean: read only the references needed for the current task.

## Workflow

1. Classify the task: quick concept, outline, full script, episode development, review/rewrite, genre strengthening, or compliance check.
2. Use the simplified intake below before choosing an output mode. Read [complex-project-intake.md](references/complex-project-intake.md) only when the user explicitly asks for a formal production brief.
3. Collect or infer: theme, audience, platform, duration, screen orientation, genre, cast size, production constraints, commercial goal, region, release channel, and risk limits.
4. State concise assumptions and proceed for both simple and complex projects. Consolidate only direction-changing unknowns into one short Decision Packet.
   When invoked by `short-drama-system` for user step 1, use Project Starter Module mode instead: consume the Foundation draft/audit, infer noncritical gaps as proposals, and return a Story Contract draft plus episode-count-independent architecture to the orchestrator without a separate confirmation gate.
5. Read the routed references below. Do not load the full reference set by default.
6. Define the logline, core hook, and ending payoff before expanding the middle.
7. Build the tree structure: soil, root, opening, ending, trunk, branches, leaves, fruit.
8. Define characters through desire, wound, flaw, secret, obstacle, relationship reversal, cost, and final choice.
9. Draft a beat sheet with information, conflict escalation, emotional change, reversal, visual action, CTA, or cliffhanger.
10. Generate the smallest useful output mode. Avoid oversized templates unless the user asks for a full deliverable.
11. Self-review with the six-gate pipeline: structure, character, hook/rhythm, dialogue, format, and continuity. For dialogue-heavy scenes, character-voice risk, hidden-information scenes, or production handoff, route the dialogue pass through `universal-dialogue-core` and consume its `DIALOGUE_CANON`.
12. For an IP project, consume any available Foundation-lite facts, cast, relationships, scope, and prohibited assumptions. After screenplay approval, create Canon-lite: version, locked events, exact dialogue IDs/text, locked characters, and prohibited changes. Full Foundation Hash, SCRIPT_CANON hash, and Narrative IR handoff are optional and only used in explicitly requested full engineering mode.

## Simplified Intake

Classify before drafting:

- **Simple request**: a logline, a short outline, one scene, a dialogue rewrite, or a task whose output form, duration, and core constraints are already explicit. State assumptions briefly and proceed.
- **Production project**: longer, episodic, existing-IP, storyboard, animation, or AI-video work. Project length alone does not activate a heavier contract.

For a production project:

1. Extract facts already supplied in the conversation; do not ask for them again.
2. Ask one consolidated Decision Packet only when missing fields would change the genre, central relationship, ending promise, duration, or downstream engine.
3. If the user says “you decide”, choose compact defaults and record them as assumptions; do not require another preliminary approval.
4. Proceed directly to the smallest useful screenplay output.
5. After approval, record Canon-lite. Do not require a formal `PROJECT_BRIEF` or hashed `SCRIPT_CANON` unless full engineering mode was explicitly requested.

**Orchestrated step-1 override:** when the parent is `short-drama-system` building `PROJECT_STARTER_PACKAGE`, do not run an independent confirmation message and do not wait for approval between project brief, Story Contract draft, and episode architecture. Return all preliminary material to the orchestrator as `ai_proposal`; the orchestrator owns the single user confirmation point. This override does not permit a formal screenplay or `SCRIPT_CANON` before approval.

The confirmation should cover only what can materially change the work: deliverable, duration/format, audience/tone, non-negotiable canon, and downstream production use. Never turn this gate into a generic questionnaire.

## Reference Routing

- Task and output-mode selection: read [routing-and-output-modes.md](references/routing-and-output-modes.md).
- 1-3 minute promo, dramatic ad, brand short: read [format-1-3min-promo.md](references/format-1-3min-promo.md), [commercial-script-rules.md](references/commercial-script-rules.md), [platform-playbooks.md](references/platform-playbooks.md), and [compliance-and-platform-risk.md](references/compliance-and-platform-risk.md).
- 4-6 minute complete short film: read [format-4-6min-short-film.md](references/format-4-6min-short-film.md), [character-arc-system.md](references/character-arc-system.md), [dialogue-and-scene-style.md](references/dialogue-and-scene-style.md), and [review-checklists.md](references/review-checklists.md).
- Vertical micro-drama series: read [format-micro-series.md](references/format-micro-series.md), [tree-structure-method.md](references/tree-structure-method.md), [hook-library.md](references/hook-library.md), [continuity-system.md](references/continuity-system.md), and [compliance-and-platform-risk.md](references/compliance-and-platform-risk.md).
- Long-series development: read [format-long-series.md](references/format-long-series.md), [tree-structure-method.md](references/tree-structure-method.md), [character-arc-system.md](references/character-arc-system.md), and [continuity-system.md](references/continuity-system.md).
- Existing script review or rewrite: read [review-checklists.md](references/review-checklists.md), [hook-library.md](references/hook-library.md), [dialogue-and-scene-style.md](references/dialogue-and-scene-style.md), and [compliance-and-platform-risk.md](references/compliance-and-platform-risk.md).
- Guided project development from premise through two outline directions and a reusable project dossier: read [project-development-v2.md](references/project-development-v2.md). Use its seven-stage decisions selectively; skip the legacy opening self-test and confirmation ceremony.
- Complex production intake, one-turn confirmation, `PROJECT_BRIEF`, and fast-start exceptions: read [complex-project-intake.md](references/complex-project-intake.md).
- Expand an approved outline into a full screenplay: read [screenplay-writing-v1.md](references/screenplay-writing-v1.md), especially its format, rhythm-mode matrix, episodic switch, batching, and continuity rules. Treat slash commands as user-intent aliases, not required product commands.
- Roundtable-style script diagnosis: read [roundtable-script-doctor.md](references/roundtable-script-doctor.md) only when the user requests multi-perspective consultation, competing stakeholder views, or a diagnostic panel. Keep viewpoints evidence-based and do not invent real credentials.
- Dialogue-only generation, diagnosis, or rewrite: route to `universal-dialogue-core` as the dialogue authority. Preserve plot and scene result unless the user expands the task. Use [dialogue-doctor-seven-dimensions.md](references/dialogue-doctor-seven-dimensions.md) only as an optional diagnostic lens, not as a second competing rewrite authority.
- Anti-cliche ignition, first-person POV direction, visualized action writing, ending alternatives, structure reshaping, seed/payoff tracking, or a single hard editorial question: read [shanyin-writing-kernel.md](references/shanyin-writing-kernel.md) and select only the relevant module. Treat its named personas and rigid JSON/HTML formats as optional lenses, not mandatory role-play.
- Genre strengthening: read [genre-playbooks.md](references/genre-playbooks.md), then add character, hook, or review references only as needed.
- Full implementation blueprint: read [screenplay-master-full-blueprint.md](references/screenplay-master-full-blueprint.md) only when maintaining or extending this skill.

## Output Modes

- Quick Concept: assumptions, project type, audience/platform, logline, hook, ending payoff, 3 title directions, 3 risks.
- Outline: assumptions, tree structure, character table, main line, subplots, beat sheet, scene/episode outline, self-check.
- Full Script: assumptions, production specs, beat sheet, timecoded script, visual/action cues, sound/subtitle cues, CTA or cliffhanger, self-check.
- Review and Rewrite: diagnosis, severity-ranked issues, rewrite strategy, revised version, change rationale, unresolved risks.
- Compliance Check: region/platform assumptions, obvious risks, rewrite points, disclosure advice, AI/copyright notes, non-legal-advice disclaimer.
- Production Handoff: approved screenplay plus Canon-lite and compact Story Map. Include Foundation/script hashes, Narrative IR, Shot IR, and formal change IDs only when the user explicitly selected full engineering mode.
- Project Starter Module: logline, hook, ending promise, Story Contract draft, four-phase story spine, and episode-count-independent architecture; returned to the orchestrator inside user step 1 and marked provisional.

## Templates

Use short assets when the user asks for a structured deliverable:

- [script-template.md](assets/script-template.md)
- [episode-outline-template.md](assets/episode-outline-template.md)
- [character-card-template.md](assets/character-card-template.md)
- [series-bible-template.md](assets/series-bible-template.md)
- [beat-sheet-template.md](assets/beat-sheet-template.md)
- [review-report-template.md](assets/review-report-template.md)

## Validation

For skill maintenance, validate against [evals/evals.json](evals/evals.json), score with [evals/scoring-rubric.md](evals/scoring-rubric.md), run `scripts/check_skill_package.py`, and use `scripts/check_screenplay_text.py` on representative outputs. Release only when the total score is at least 90, trigger accuracy, compliance/risk, and dramatic effectiveness each pass the gate, and the non-trigger tests do not misfire.
