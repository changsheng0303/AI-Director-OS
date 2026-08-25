---
name: series-image-director
description: "把主提示词、参考图、角色、产品、Logo、IP 或品牌规范发展为视觉 DNA 锁定的系列套图，管理变化、提示词、生成顺序、一致性、选片和修复；不用于单张无关图片或简单润色。"
---

# Series Image Director

Design a family of images that clearly belong together while giving each image a distinct compositional job.

## Workflow

1. Determine the task type, number and purpose of outputs, target channels, aspect ratios, generation model, and available master/reference assets.
2. Read [full-series-image-method.md](references/full-series-image-method.md) completely. Treat named legacy tools as capability descriptions; use only tools actually available in the current environment.
3. Extract the visual mother system: subject locks, palette, lighting, material language, composition grammar, camera behavior, typography/logo rules, and prohibited drift.
4. Separate invariants from controlled variables. Each image should change only the dimensions assigned to it: scene, action, camera, crop, prop, mood, or message.
5. Build a series matrix that states each image's role, retained anchors, allowed variation, prompt, references, aspect ratio, and acceptance criteria.
6. Generate or deliver prompts in an order that establishes the strongest identity anchor first. Reuse approved anchors rather than rewriting them inconsistently.
7. Compare the set as a whole, reject outliers, repair only the failed dimensions, and upscale after selection rather than before.

## Output Contract

- Present the master-style lock and variation matrix before individual prompts.
- Distinguish source facts, inferred design rules, and creative additions.
- Preserve exact brand and character assets; do not invent logos, text, or product claims.
- When the user requests images rather than prompts, use the available image-generation workflow and return the generated assets with a brief consistency report.
