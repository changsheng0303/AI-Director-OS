# Adaptive Human Gates

## Principle

Use the fewest creative approval points that prevent expensive rework. Internal artifacts and validators never create a user-facing checkpoint by themselves.

## Gate count

- **2 gates** when the user supplies an approved screenplay or requests a fast proof of concept: production direction, final master.
- **3 gates by default**: project direction, screenplay canon, final master.
- **4 gates only when necessary**: add a director/production-package gate when visual medium, engine, budget, reference assets or generation strategy has material alternatives.

## Remove or fold

For a single episode or short film, do not create separate human-facing Foundation Draft, Foundation Audit, Story Contract pre-draft, episode architecture, episode outline, Scene Lock, Beat Lock, Spatial Lock, asset plan and multi-part Shot documents. Fold them into:

1. `PROJECT_BRIEF` — direction, canon, exclusions.
2. `SCRIPT_CANON` — final screenplay and dialogue.
3. `PRODUCTION_PACKAGE` — internal Narrative IR, validated JSON Shot IR, text visual anchors, Video Prompt IR, engine plan.
4. `FINAL_MASTER` — final cut and delivery metadata.

Only produce a separate artifact when a validator, collaborator or downstream tool consumes it. Human-readable summaries belong in the nearest parent package.

## Conditional processes

- Competitive research: only when the user asks for market validation or commercial positioning.
- Season architecture and episode outline: only for multi-episode scope.
- Full IP Foundation: only when durable world/character canon will be reused beyond one short.
- Image asset generation: only when the selected video workflow uses references or the user requests images.
- Detailed asset registry: omit when `asset_mode=text_reference_only`; embed visual anchors in the production package.
- Narrative IR and Shot IR: keep for AI-video production, but internal and machine-readable.
- Distribution and learning: only when publication or performance analysis is in scope.

## Escalation

Add a checkpoint only when the pending decision changes story canon, visual medium, cost, external side effects or irreversible work. Otherwise infer a reasonable default, record it, and continue.
