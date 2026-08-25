# IP Foundation Contract V1.0

## Position in the pipeline

```text
USER STEP 1: PROJECT_STARTER_PACKAGE
  [S-1A Foundation Draft + Foundation Audit
   + S0 Creative Brief Seed
   + S1 Story Contract Draft
   + episode-count-independent architecture]
  -> one user confirmation
  -> S-1B Foundation Lock
  -> USER STEP 2: formal Story Contract + screenplay
  -> Narrative IR
```

S-1A may produce a Foundation Draft. S-1B produces the only Foundation Package that downstream work may treat as Canon.

When orchestrated by `short-drama-system`, S-1A, the semantic audit, the Creative Brief seed, Story Contract draft, and flexible episode architecture are internal modules of one user-visible first step. They may be separate machine artifacts, but they must be presented as one `PROJECT_STARTER_PACKAGE` with one confirmation point.

## Static versus dynamic

Foundation owns durable facts:

- world rules, locations, organizations, culture, and story scope;
- character identity, role, values, behavior model, voice DNA, visual anchors;
- pet identity and trigger-response behavior;
- relationship structure and enduring tensions;
- approved creative and production constraints.

Narrative IR or Project State owns dynamic facts:

- current location, outfit, mood, knowledge, possession, health, and relationship change;
- scene events, episode objectives, promises, and chronological state;
- generated assets, prompts, and takes.

## Fact model

Every meaningful fact is atomic and traceable:

```yaml
fact_id: FACT-001
path: character.CH-001.behavior.under_pressure
value: "先确认他人安全，再压低声音给出指令"
layer: static
origin: user
authority: locked
confidence: high
evidence:
  - "用户说她是成熟、照顾型的核心角色"
```

`origin`: `user`, `imported`, `llm_extraction`, `ai_proposal`, or `derived`.

`authority`: `locked`, `pending`, or `rejected`.

Only locked static facts can enter Canon. An `ai_proposal` may be locked only when its `accepted_by` is recorded.

## Interview policy

The deterministic router ranks missing fields by blocker severity, downstream fan-out, and whether the fact is already known. The model turns the returned blocking fields into one stage-level Decision Packet rather than a sequence of single-question turns.

- Include all current blocking fields in the same packet; skip already-known facts, including facts extracted from free text.
- Every question has exactly four choices: A/B/C are concrete, mutually exclusive and state their direct downstream impact; D is `补充内容／自定义`.
- Ask for cast counts only when absent and necessary for cast architecture.
- Ask about non-human roles only when the seed, genre, or existing cast indicates they may matter.
- Treat noncritical uncertainty as `ai_proposal` and present it later in one assumptions/proposals card.
- When the user delegates details to the model, stop asking at that level and produce proposals.
- A second packet is allowed only when the first answer creates a new critical contradiction, branch, or authorization need; never drip-feed detail questions.

## Foundation handoff

Before lock, the bundled starter handoff contains:

```yaml
starter_status: STARTER_DRAFT_READY
known_user_facts:
ai_proposals:
foundation_draft:
foundation_audit:
story_handoff_seed:
open_noncritical:
decision_packet:
```

`decision_packet` is omitted when there are no true blockers. A noncritical blank never stops creation of the starter package.

`FOUNDATION_LOCKED` requires:

```yaml
foundation_id:
foundation_version:
content_hash:
locked_fact_ids:
entity_registry:
cast_manifest:
relationship_graph:
world_constraints:
allowed_story_scope:
prohibited_assumptions:
open_noncritical_questions:
```

S0 may add audience, platform, duration, or commercial constraints. If those contradict a locked foundation fact, create a Foundation Change Request; do not silently overwrite the foundation.

S1 Story Contract must record `foundation_id`, `foundation_version`, and `foundation_hash`. Narrative IR then references stable character, location, rule, and relationship IDs.

## Validation split

Code validates IDs, references, fact authority, static/dynamic separation, cast counts, relationships, locked Canon, relevance references, and unresolved critical fields.

Model judgment validates dramatic relevance, character differentiation, voice distinction, visual distinction, semantic contradiction, and repair choices.
