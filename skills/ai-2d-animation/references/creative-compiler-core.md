# Creative Compiler Core V1.0

Use this reference when a project needs traceable screenplay-to-shot compilation, canon protection, persistent artifact state, or deterministic continuity validation.

## Canonical Pipeline

```text
IP FOUNDATION (optional for standalone scenes; required for IP projects)
  -> Creative Brief
  -> SCRIPT_CANON
  -> Story Contract
  -> Narrative IR
  -> Director Interpretation
  -> Shot Contract / Shot IR
  -> Renderer Adapter
  -> Prompt / Generation / Editorial
```

Each arrow is an artifact boundary. A downstream stage may interpret its input, but it may not silently rewrite an upstream canonical fact.

## Authority Boundaries

- `IP FOUNDATION`: approved static world, character, relationship, and production constraints. It has no episode-level state authority.
- `SCRIPT_CANON`: approved plot, dialogue, named entities, scene order, and factual actions; it inherits the Foundation ID/version/hash.
- Story Contract: dramatic architecture and ending obligation.
- Narrative IR: machine-readable scenes, events, causality, character knowledge/state, promises, and continuity ledger.
- Director Interpretation: visual concept, blocking, information control, rhythm, and editing logic.
- Shot IR: executable camera, action, timing, continuity, provenance, and renderer requirements.
- Renderer Adapter: model-specific prompt syntax and technical limits. It has no story authority.

## Narrative IR Gate

Create Narrative IR after the screenplay or Story Contract is approved and before final shot planning. Use `schemas/narrative-ir.schema.json`.

Required invariants:

1. `source.source_hash` identifies the exact screenplay bytes used for extraction.
2. For an IP project, `foundation_ref` identifies the locked Foundation ID/version/hash and stable entity/rule IDs used by the screenplay.
3. `canon.locked=true` and `plot_change_allowed=false`.
4. Every scene has an entry state, exit state, objective, conflict, turn, emotional delta, and ordered event list.
5. Every event has a stable ID, earlier causes, observable action, consequence, and valid participants.
6. Character knowledge changes cite how the information was acquired.
7. Promise payoff never precedes planting.
8. Dead characters and destroyed props cannot reappear in present-time action without an explicit legal mode or approved change.

Run:

```powershell
python scripts/validate_narrative_ir.py path/to/narrative-ir.json
```

For an IP project, also pass the locked S-1B handoff:

```powershell
python scripts/validate_narrative_ir.py path/to/narrative-ir.json `
  --foundation-handoff path/to/ip-foundation-handoff.json
```

Use `--warnings-as-errors` only at a release gate; warnings are useful during drafting.

## Shot IR Gate

The existing `shot-contract.schema.json` is the canonical Shot IR. V1.7 adds three optional backward-compatible blocks:

- `source_ref`: script hash, Narrative IR ID/version, scene, and beat.
- `canon`: plot/dialogue modification policy and approved change IDs.
- `render`: renderer adapter, exact duration, constraints, and prompt artifacts.

New production packages should include all three even though older V1.6 records remain readable.

Run:

```powershell
python scripts/validate_shot_ir.py path/to/shot-ir.json `
  --narrative-ir path/to/narrative-ir.json `
  --strict-provenance `
  --strict-continuity
```

CSV storyboards continue to use `validate_storyboard.py`; JSON Shot IR uses `validate_shot_ir.py`.

## Canon Change Protocol

When a locked upstream artifact must change:

1. Create a change request with ID, scope, reason, and status.
2. Obtain user approval before changing canonical content.
3. Write the approved change ID into the new artifact registry record.
4. Increment the artifact version and recompute SHA-256.
5. Run `state_diff.py` against before/after project states.
6. Mark every unchanged descendant `INVALIDATED`, or rebuild it with a new version and hash.
7. Persist the resulting invalidation event only after reviewing the plan.

Never treat a downstream rewrite suggestion as approval to modify canon.

## State Diff

`project-state.schema.json` V1.6 adds:

- `change_requests`
- `artifact_registry`
- `invalidation_log`

Run:

```powershell
python scripts/state_diff.py before-project-state.json after-project-state.json
```

The script is read-only. It reports changed roots, affected descendants, rebuilt artifacts, missing invalidations, and canon violations.

## Deterministic vs Semantic Work

Use code for:

- required fields and ID uniqueness;
- SHA-256 and version linkage;
- scene/event/shot references;
- duration totals;
- cause order and cycles;
- promise plant/payoff order;
- character death and prop destruction contradictions;
- parent/child invalidation and state diff.

Use model judgment for:

- dramatic effectiveness;
- character motivation;
- visual concept and blocking;
- emotional and information rhythm;
- shot motivation;
- selecting the least damaging repair.

Lower call counts are not success if the final artifact fails these gates.
