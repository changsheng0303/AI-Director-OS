# Lira Image Production Method

Use this reference for production-grade character, scene, prop, or image-editing work where consistency and failure prevention matter. It supplements the asset inventory; it does not authorize redesigning approved story or character Canon.

## Diagnose before prompting

Identify:

- the exact asset type and intended downstream use;
- whether the task is generation, controlled edit, texture cleanup, or viewpoint change;
- the approved identity, geometry, material, light, text, and composition constraints;
- the target tool and any UI-only settings;
- the smallest missing facts that would materially change the result.

Proceed directly when the request is specific. For ambiguous high-risk work, ask no more than three focused questions.

## Route by operation

- **Character identity sheet:** use a consistent multi-view photographic layout only when the target tool supports it. Lock the same real person, stable proportions, face, hair, marks, and clothing across panels. Do not add generic composition rules that conflict with a neutral identity sheet.
- **Scene/environment:** lead with camera viewpoint and spatial anchor, then architecture/nature, material, motivated light, depth layers, color behavior, and atmosphere.
- **Prop:** use an isolated product-photography view with explicit scale, material, wear state, functional parts, and exact text when text is required. Different physical states should be separate assets or explicit variants.
- **Controlled edit:** change one intended element at a time. State the replacement or removal and describe what fills the vacated area.
- **Texture cleanup:** change surface quality only; preserve identity, geometry, layout, light, color, and object placement.
- **Viewpoint change:** treat it as a new camera position. Re-map every important object's screen position and visible/occluded surfaces; do not assume the tool will infer a correct reverse angle.

Do not hard-code a historical model ranking. Use the user's selected tool, a currently available tool, or a verified capability. Keep aspect ratio, resolution, version, sampler, and other UI controls outside the reusable content prompt unless the target interface explicitly requires them in text.

## Prompt construction

- Prefer coherent natural language over keyword piles.
- Keep only details that control identity, geometry, material, light, color, text, or camera.
- Describe the desired positive state first. Use removal/negative language only when the operation genuinely edits an existing image or prevents a demonstrated failure.
- Derive color proportions from approved references or narrative purpose; do not invent a fixed palette merely to fill a template.
- Use concrete light sources, directions, ratios, falloff, and material response instead of vague “cinematic” adjectives.
- Treat role/character identity as a combination of approved reference assets and stable textual anchors; text alone is not a substitute for a supported identity mechanism.
- Translate a real-person or filmmaker reference into observable traits when direct naming would create rights, safety, or tool-policy problems.

## Surgical edit contract

For a controlled edit, use a compact change block plus an explicit preservation block:

```text
【更改】
Only the named element and its physically necessary local consequences.

【精确保留】
Identity; body and object geometry; clothing and props not named for change; camera position; composition; background structure; existing shadows; color and texture outside the edit area.

【唯一更改】
Restate the one intended change. Everything else remains unchanged.
```

If the user reports excessive drift, reduce the change scope and strengthen the preservation list. Do not solve local drift by redrawing the entire image.

## Asset output

For each asset, record:

- asset ID and type;
- approved source or reference basis;
- recognizable anchors;
- production state or variant relationship;
- intended generation/edit tool;
- reusable content prompt;
- separate tool settings;
- review status.

Do not produce performance blocks or final video prompts inside the asset deliverable.
