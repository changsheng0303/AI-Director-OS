# Project Starter Package Contract

Use this contract when a user starts an IP/short-film project or asks to continue an unfinished preproduction stage.

## User-facing outcome

The entire early-development chain is one user-visible step. Internal modules may write separate machine artifacts, but the user receives one consolidated package and one confirmation point.

## Required modules

1. **Known facts**: every user-confirmed creative and production fact, with provenance. For source adaptation, optional `canon_lite.fact_basis` records decisive excerpts without turning the package into a full evidence graph.
2. **AI proposals**: low-impact details the system filled without questioning the user.
3. **Foundation Draft**: minimum world skeleton, main cast functions, relationship structure, rules and exclusions.
4. **Foundation Audit**: contradictions, role overlap, realism, production relevance and repair proposals.
5. **Story Contract Draft**: logline, season objective, audience promise, opening engine, ending promise, main causal spine and key branches.
6. **Episode Architecture**: phase functions and repeatable 16-minute or project-specific episode unit; keep it episode-count-independent when total count is unknown.
7. **Decision Packet**: include only genuine blockers. Every question has A/B/C concrete choices and D custom input. Omit this module when no blocker exists.

## Execution rules

- Do not stop after any module or ask the user to say “continue”.
- Do not generate four nearly duplicate human-facing files by default. Prefer one readable package with internal sections; split machine artifacts only when downstream validators require it.
- Platform, names, minor roles, prop details, medical granularity and exact episode count do not block the starter package unless the user's stated delivery goal makes one of them structurally decisive.
- Preserve `user_locked`, `ai_proposal`, and `open_noncritical` boundaries.
- Run deterministic and semantic checks internally. Report only consolidated findings.
- Status after generation is `STARTER_DRAFT_READY`. It is not `FOUNDATION_LOCKED`, `STORY_LOCKED`, or `SCRIPT_CANON`.

## Approval transition

One user confirmation or consolidated set of modifications upgrades accepted Foundation facts, records proposal acceptance, reruns validation, and prepares formal Story Contract work. Never request separate approvals for the Foundation draft, audit, Story Contract draft, and episode architecture.
