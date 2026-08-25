# Screenplay Master Full Blueprint

This blueprint preserves the full development plan, task slicing, review pipeline, module design, validation logic, and delivery notes for the `screenplay-master` skill. Runtime use should load `SKILL.md` first and only open this file when maintaining or extending the skill.

## 1. Objective

Upgrade `screenplay-master` from a template stub into a maintainable Codex skill for creating, planning, revising, and evaluating short dramas, micro-dramas, vertical series, scripted short videos, dramatic ads, promo films, episode outlines, beat sheets, hooks, cliffhangers, character arcs, series bibles, and script-doctor reviews.

Design goals:

- Keep the production `SKILL.md` small and fast to load.
- Put detailed knowledge into `references/`.
- Put reusable output skeletons into `assets/`.
- Put deterministic validation into `scripts/`.
- Put forward-test prompts and scoring into `evals/`.
- Avoid long-lived sub-agents; use temporary, bounded batches for planning and review only.

## 2. Delivery Layout

```text
screenplay-master/
  SKILL.md
  agents/
    openai.yaml
  references/
    routing-and-output-modes.md
    format-1-3min-promo.md
    format-4-6min-short-film.md
    format-micro-series.md
    format-long-series.md
    platform-playbooks.md
    tree-structure-method.md
    hook-library.md
    character-arc-system.md
    genre-playbooks.md
    dialogue-and-scene-style.md
    continuity-system.md
    commercial-script-rules.md
    compliance-and-platform-risk.md
    review-checklists.md
    screenplay-master-full-blueprint.md
  assets/
    script-template.md
    episode-outline-template.md
    character-card-template.md
    series-bible-template.md
    beat-sheet-template.md
    review-report-template.md
  evals/
    evals.json
    scoring-rubric.md
  scripts/
    check_skill_package.py
    check_screenplay_text.py
```

Notes:

- `SKILL.md` is the production-grade compact skill file.
- This blueprint is the full human-readable design record.
- `references/` is the global shared knowledge library.
- `assets/` contains short reusable templates only.
- `evals/` is for maintenance testing, not mandatory runtime context.
- `scripts/` contains deterministic validators; it does not replace creative review.

## 3. Stage 1: Task Slicing and Responsibility Boundaries

The full development task is split into 30 standardized slices using a tree-like architecture. Temporary subtask batches may run in parallel, with a maximum of 20 groups per batch. In the current environment, the practical concurrency cap was 6, so execution used smaller batches while still staying below the requested cap.

All temporary subtasks are destroyed after completion. No long-lived agent is created. No subtask owns a private file context; all use the same shared project documents and global reference cache.

### 30 Task Slices

| Group | Responsibility | Write Scope | Read Dependencies |
|---|---|---|---|
| 01 | Project skeleton and build sequence | Blueprint, directory plan | Full plan |
| 02 | 30 task slices, permissions, isolation, scheduling | Blueprint task chapter | Full plan |
| 03 | `SKILL.md` frontmatter and trigger boundary | `SKILL.md` | Blueprint, sources |
| 04 | `SKILL.md` workflow and output modes | `SKILL.md` | Reference routing |
| 05 | `agents/openai.yaml` UI metadata and default prompt | `agents/openai.yaml` | `SKILL.md` |
| 06 | Reference routing table | `references/routing-and-output-modes.md` | `SKILL.md` |
| 07 | 1-3 minute promo format | `references/format-1-3min-promo.md` | Commercial and risk rules |
| 08 | 4-6 minute short film format | `references/format-4-6min-short-film.md` | Character, dialogue, review |
| 09 | Vertical micro-series format | `references/format-micro-series.md` | Tree, hooks, continuity |
| 10 | Long-series development format | `references/format-long-series.md` | Tree, character arcs |
| 11 | Tree structure method | `references/tree-structure-method.md` | Core story modules |
| 12 | Hook and cliffhanger library | `references/hook-library.md` | Platform heuristics |
| 13 | Character arc system | `references/character-arc-system.md` | Review perspectives |
| 14 | Genre playbooks | `references/genre-playbooks.md` | Core style boundary |
| 15 | Dialogue and scene style | `references/dialogue-and-scene-style.md` | Shootability rules |
| 16 | Continuity system | `references/continuity-system.md` | Series formats |
| 17 | Commercial script rules | `references/commercial-script-rules.md` | Compliance and platform risk |
| 18 | Platform playbooks | `references/platform-playbooks.md` | Trigger and platform context |
| 19 | Compliance and risk | `references/compliance-and-platform-risk.md` | Regulation, ads, copyright, AI |
| 20 | Review checklists | `references/review-checklists.md` | Review perspectives |
| 21 | Full script template | `assets/script-template.md` | Output modes |
| 22 | Episode outline template | `assets/episode-outline-template.md` | Micro-series format |
| 23 | Character, series bible, beat sheet, review templates | `assets/*.md` | Asset plan |
| 24 | Eval prompt set | `evals/evals.json` | Release gates |
| 25 | Scoring rubric | `evals/scoring-rubric.md` | Scoring dimensions |
| 26 | Release gates and test process | `evals/` | Evals and rubric |
| 27 | Non-trigger and boundary tests | `evals/evals.json` | Trigger boundaries |
| 28 | Optional scripts and deterministic validators | `scripts/` | Validation needs |
| 29 | Global consistency review | Blueprint, targeted fixes | All files |
| 30 | Final release review and delivery checklist | Blueprint, final checklist | All files |

### Permission Rules

- `SKILL.md`: only groups 01, 03, 04, 29, 30.
- `agents/openai.yaml`: only groups 05, 29, 30.
- `references/`: each group owns only its reference file.
- `assets/`: each group owns only its template file.
- `evals/`: only groups 24-27, 29, 30.
- `scripts/`: only group 28, then reviewed by 29/30.
- Blueprint: only groups 01, 02, 29, 30.

Isolation rules:

1. Do not cross-edit another group's file.
2. Keep every reference one hop from `SKILL.md`.
3. Keep assets short and reusable.
4. Keep evals out of runtime context unless testing.
5. Do not put creative roles in `agents/openai.yaml`.
6. Treat internal review perspectives as self-checks, not real persistent agents.
7. Record unresolved risks when a slice cannot fully decide an issue.

## 4. Stage 2: Cross-Review Pipeline

Every substantial module passes six review gates. A module with a hard failure returns to the responsible slice for rewrite. Passing all gates allows the module to move forward.

| Gate | Weight | Checks |
|---|---:|---|
| Structure | 20 | Logline, hook, ending payoff, main line, branch logic, runtime fit |
| Character | 15 | Desire, obstacle, wound, flaw, secret, final choice, motive consistency |
| Hook / Rhythm | 20 | First 3-10 seconds, conflict escalation, reversal, emotional payoff, cliffhanger |
| Dialogue | 15 | Oral short lines, conflict function, low exposition, differentiated voices |
| Format | 15 | Correct output mode, timecode/scene/episode fields, no bloated template |
| Continuity | 15 | Names, relationship, timeline, setups/payoffs, platform and risk assumptions |

Hard returns:

- Mis-triggering ordinary prose, news, slogan, code, legal, or market tasks.
- Missing compliance risk for medical, finance, education, health, beauty, minors, AI, commercial placement, copyright, or IP.
- Copying distinctive existing plots, lines, character settings, or set pieces.
- Producing an output unusable by writer, director, editor, or reviewer.

## 5. Stage 3: Module Content

### Runtime and Output Routing

`routing-and-output-modes.md` decides whether to produce quick concept, outline, full script, review/rewrite, or compliance check. It also contains trigger and non-trigger boundaries.

### Core Formats

- `format-1-3min-promo.md`: percentage structure, runtime conversion, product integration, CTA.
- `format-4-6min-short-film.md`: complete short story with irreversible character choice.
- `format-micro-series.md`: 20-80 episode vertical micro-series, first 3 episodes, season table.
- `format-long-series.md`: long-series bible, main/subplots, season/episode structure, ending.

### Structural and Creative Knowledge

- `tree-structure-method.md`: soil, root, opening, ending, trunk, branches, leaves, fruit.
- `hook-library.md`: opening hooks, cliffhangers, reversals, title directions, prohibitions.
- `character-arc-system.md`: character card fields, conflict dimensions, arc checks.
- `genre-playbooks.md`: sweet romance, comeback, suspense, revenge, family, workplace, social issue, comedy, horror, costume.
- `dialogue-and-scene-style.md`: dialogue compression, visual cues, shootability.
- `continuity-system.md`: motive, setup/payoff, timeline, relationship, change log.

### Platform, Business, and Risk

- `commercial-script-rules.md`: product placement, CTA, disclosure, claims, regulated categories.
- `platform-playbooks.md`: Douyin, Kuaishou, WeChat Channels, Xiaohongshu, TikTok, YouTube Shorts, Reels, short-drama apps.
- `compliance-and-platform-risk.md`: source pointers, risk levels, China micro-drama draft status, AI labeling, commercial disclosure, copyright/IP, platform content risk.

### Review and Validation

- `review-checklists.md`: six-gate review and return rules.
- `evals/evals.json`: eight prompts, including trigger and non-trigger cases.
- `evals/scoring-rubric.md`: 100-point scoring system and release gates.
- `scripts/check_skill_package.py`: package structure validator.
- `scripts/check_screenplay_text.py`: lightweight output signal validator.

## 6. Stage 4: Engineering Simplification

Engineering decisions:

- The production `SKILL.md` keeps only trigger description, workflow, reference routing, output modes, template pointers, and validation pointers.
- Detailed knowledge is removed from `SKILL.md` and stored in `references/`.
- Reusable templates are stored in `assets/`.
- Evals are stored outside runtime references.
- Validation scripts are deterministic and small.
- No redundant README, installation guide, quick reference, or unrelated docs are added.

Deduplication:

- Hook/rhythm logic lives in `hook-library.md` and is referenced by review and format files.
- Character logic lives in `character-arc-system.md`.
- Commercial risk lives in `commercial-script-rules.md` and cross-links conceptually to `compliance-and-platform-risk.md`.
- Platform heuristics live in `platform-playbooks.md`.
- Detailed review gates live in `review-checklists.md`.

## 7. Stage 5: Two-File Standard Delivery

Final delivery has two primary files:

1. Full blueprint MD: `references/screenplay-master-full-blueprint.md`
   - Human-readable.
   - Preserves planning, architecture, task slices, review pipeline, module map, validation design, and release notes.

2. Production compact skill file: `SKILL.md`
   - Runtime entrypoint.
   - Contains trigger metadata, concise workflow, direct reference routing, template pointers, and validation pointers only.

Support files are part of the working skill package but are not the two primary delivery documents.

## 8. Source and Risk Notes

The skill includes current official source pointers for:

- NRTA micro-drama public-comment draft, June 24, 2026.
- CAC AI-generated synthetic content labeling measures notice, March 14, 2025.
- FTC social media influencer disclosure guidance.
- TikTok branded content promotion guidance.
- YouTube paid product placement, sponsorship, and endorsement disclosure guidance.

Operational rule:

- Treat regulatory and platform material as volatile.
- When a user asks for current release compliance, verify official sources live.
- Do not present creative risk checks as legal advice or platform approval.

## 9. Final Checklist

- `SKILL.md` has valid YAML frontmatter.
- `description` covers trigger and non-trigger boundaries.
- `agents/openai.yaml` includes `$screenplay-master`.
- All references are directly linked from `SKILL.md`.
- Assets are concise templates.
- Evals include trigger and non-trigger cases.
- Scripts run without missing-package dependencies.
- `SKILL.md` remains compact enough for routine invocation.
