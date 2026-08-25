# Generation Budget V1.2

## Tiers
| Tier | Typical use | Max attempts | Human priority |
|---|---|---:|---|
| L | Background/static/transition | 2 | Low |
| M | Dialogue/simple acting | 3 | Normal |
| H | Complex action/camera | 4 | High |
| HERO | Climax/Sakuga/key marketing shot | 6 | Hero |

These are planning defaults, not hard model limits.

## Budget Fields
`budget_tier / expected_attempts / max_attempts / priority / cost_weight`

## Escalation
1. Local prompt repair
2. Retry same route
3. Fallback model
4. Human review
5. Shot redesign only if necessary

Do not spend HERO budget on an unresolved story or asset problem.
