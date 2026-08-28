---
name: ip-foundation-engine
description: "从创意种子建立简化 IP Foundation：确认事实、世界边界、主要阵容、关键关系、禁止假设和待确认提案，并交给剧本系统。完整事实溯源、Hash 与机器交接仅在用户明确要求时启用。"
---

# IP Foundation Engine

Build the static world and character Canon that story, screenplay, Narrative IR, and production layers can safely inherit.

## Boundary

This skill owns durable identity and world truth. It does not own episode-level location, costume, mood, current knowledge, or scene events; those belong to Narrative IR and Project State.

Use the installed `$character-design-director` only after Cast Architecture identifies which main characters deserve Bible or production depth. Do not create full bibles for every minor role by default.

## Default Lite Mode

All ordinary and orchestrated projects use Foundation-lite: creative seed, confirmed facts, compact world boundary, main cast, key relationships, prohibited assumptions, and pending proposals. Return it inside the project/script package rather than creating a separate approval stage.

Do not require `ip-foundation.json`, Foundation Hash, entity registry, full Character Bible, or `FOUNDATION_LOCKED` in the default mode. Use the full schema, validator, renderer, and handoff builder only when the user explicitly asks for complete engineering traceability.

## Workflow

1. Parse the seed into atomic facts. For every fact, preserve `origin`, `authority`, `confidence`, and evidence. Never convert an inference or proposal into locked Canon without an explicit approval record.
2. Read [foundation-contract.md](references/foundation-contract.md) before creating, auditing, or handing off a foundation package.
3. Run `scripts/question_router.py` on the current package or equivalent extracted facts. Convert all returned blocking fields into one stage-level Decision Packet; do not ask them one at a time and do not re-ask known facts. Every question must contain exactly four choices: A/B/C are three concrete, mutually exclusive proposals with their direct impact, and D is `补充内容／自定义`. If a field is low impact or the user delegates it, create an `ai_proposal` instead of asking.
4. Create a Foundation Draft: a minimal world skeleton, entity registry, cast architecture, relationship graph, constraints, and unresolved-question list. World modules are conditional on narrative relevance; do not write encyclopedic lore with no downstream use.
5. For film projects that need a narrative character bible or bounded world rules, read [film-character-and-world-bible.md](references/film-character-and-world-bible.md). Expand only the approved main cast. Separate identity, behavior, voice, visual identity, and relationship function. Keep current state outside this package.
6. In lite mode, check only confirmed-versus-proposed facts, cast duplication, key relationship contradictions, and story relevance. In explicit full mode, run `scripts/validate_ip_foundation.py` and fix deterministic errors before semantic review.
7. Perform one focused semantic audit: role duplication, voice/behavior overlap, unsupported world rules, relationship ambiguity, and production relevance. Offer repairs as proposals rather than silent edits.
8. When called by `short-drama-system`, return Foundation-lite and the compact story handoff inside user-visible step 1; do not stop for a separate Foundation review.
9. Only in explicit full mode, lock after there are no critical unresolved fields, render Markdown, and generate the canonical hash and S-1B contract.
10. Lite handoff contains confirmed facts, cast, key relationships, allowed scope, prohibited assumptions, and pending proposals. Full handoff additionally contains Foundation ID/version/hash and stable entity IDs.

## Output Modes

- Seed Triage: known facts, assumptions, top questions, and no expanded lore.
- Foundation Draft: world skeleton, cast function cards, proposals, and blockers.
- Character Bible: only for a named main character or an approved main cast.
- Foundation Audit: deterministic errors, semantic findings, repair proposals, and lock readiness.
- Production Handoff: `ip-foundation.json`, rendered Markdown, audit report, and S0/S1 contract.
- Project Starter Module: Foundation Draft + audit + story-handoff seed, returned to `short-drama-system` as one section of the first-step package rather than separate user-facing files.

## Non-Negotiable Rules

- `origin` and `authority` are separate axes. A fact proposed by AI may become locked only after acceptance is recorded.
- `authority: pending` or `rejected` facts must not appear in Canon's locked fact list.
- Relationships are directed; do not invent reciprocity. Model asymmetry explicitly.
- Do not use numeric affinity scores unless a later simulation layer explicitly requires them.
- Lock fewer facts with clear provenance instead of many ungrounded details.
- A Foundation interview is batched by stage. After a Decision Packet is answered, do not open a new detail-by-detail interview unless the answer creates a new critical contradiction or branch.
- In orchestrated project startup, Foundation Draft and Foundation Audit are internal substeps of one user-visible first step. Never pause between them or require the user to say “continue”.
