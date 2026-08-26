# Production Failure Feedback Loop

Use this process only for observed failures from source review, deterministic validation, user feedback, or actual generated media. Do not log imagined failures as facts.

## Flow

```text
Observed failure
→ structured record
→ local repair
→ regression candidate
→ repeated evidence
→ validator or Skill rule promotion
```

## Evidence levels

| evidence_type | Meaning |
|---|---|
| `source_logic` | A contradiction is directly visible in the supplied source or approved script |
| `validator_failure` | Deterministic code produced a reproducible failure |
| `user_feedback` | The user identified a concrete failure in an artifact |
| `generation_output` | An actual generated image/video/audio artifact demonstrates the failure |

Never label a prompt-writing concern as `generation_output` without an artifact path.

## Promotion policy

1. Repair the current project immediately when the failure is real and in scope.
2. One project failure may become a project warning, not a universal rule.
3. A candidate cross-project rule needs at least two independent occurrences.
4. A core deterministic gate normally needs three occurrences across at least two projects plus a regression fixture.
5. Safety, data loss, exact reference integrity, or externally mandated format failures may be promoted sooner when the invariant is objective.
6. Creative dislike, style preference, or one model's temporary behavior must not become a global prohibition.

## Registry

The repository registry is `quality/failure-registry.jsonl`. Validate it with:

```powershell
python "skills/short-drama-system/scripts/validate_failure_registry.py" "quality/failure-registry.jsonl" --summary
```

Store project-local private paths outside the public registry. Public evidence should use a sanitized project-relative artifact path or a concise observation.
