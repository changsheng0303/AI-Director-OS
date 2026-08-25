# Scoring Rubric

Release target: 90/100 or higher.

| Dimension | Points | Passing Standard |
|---|---:|---|
| Skill structure | 15 | `SKILL.md`, `references`, `assets`, `agents/openai.yaml`, `evals`, and scripts have clear roles. |
| Trigger accuracy | 15 | Description covers script tasks and excludes prose, news, slogans, pure legal/market/coding tasks. |
| Progressive loading | 15 | `SKILL.md` is lean, references are directly linked, and details are not duplicated in the main file. |
| Dramatic effectiveness | 20 | Hook, conflict, character choice, rhythm, payoff, and series cliffhangers work. |
| Platform and commercial fit | 10 | Output adapts to platform, orientation, runtime, audience, and commercial goal. |
| Compliance and risk | 10 | Regulatory, ad disclosure, copyright, AI label, sensitive content, and platform risks are flagged. |
| Output usability | 10 | The result is structured, not bloated, and usable by writer, director, editor, or reviewer. |
| Validation loop | 5 | Evals, scoring gates, non-trigger checks, and iteration rules exist. |

## Gates

- Total score must be at least 90.
- Trigger accuracy, dramatic effectiveness, and compliance/risk must each reach at least 80% of their category.
- At least 6 of 8 eval prompts should score 90 or higher.
- Non-trigger tests must not invoke the screenplay workflow unless the user asks for script conversion.

## Failure Response

- If a problem comes from `SKILL.md`, tighten workflow or routing.
- If a problem comes from domain detail, update the relevant reference.
- If a template is unusable, revise only the affected asset.
- If repeated deterministic checks are needed, add or update scripts.
