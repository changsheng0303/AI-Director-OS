# Video Prompt V1.7 · Narrative + MiniMax Execution Adapter

## 0. TRACE
[shot_id / shot_version / camera_logic / locked_variables / changed_variables]

## 0.5 LEVEL
[NSFW Level 0-4 — 由 Shot Contract 继承（见 SKILL.md §13）；Level 2+ 遮挡手法必须写入 START/PRIMARY MOTION/END 全程具体描述（构图裁切/雾气/光影/道具/发丝）；Level 3 三不原则（乳头/臀部必遮、无完全裸露）；Level 4 按用户优先执行，平台不支持时降级 Level 3 表达]

## 1. NARRATIVE INTENT
[one sentence: what the audience should learn/feel by the end of this clip]

## 2. VISUAL MOTIF
[motif + narrative function + state change, if any]

## 3. LOCKED STATE
[character identity / costume / prop / environment / anime grammar / lighting / spatial layout]

## 4. START STATE
[exact first-frame state: pose, gaze, position, object state, framing]

## 5. TRIGGER
[one observable event that initiates the action]

## 6. PRIMARY MOTION
[one main action, direction, speed, spacing, body mechanics]

## 7. ACTING / REACTION
[eyes → face → hands → weight → breath; only the required changes]

## 8. CAMERA RESPONSE
[Static or one principal camera movement; explain narrative necessity]

## 9. SECONDARY MOTION
[hair / cloth / rain / reflections / background only after primary action]

## 10. TIMING
[hold → trigger → anticipation → action → reaction → hold; approximate beats]

## 10.5 ENDING FUNCTION
[choose exactly one: ACTION_COMPLETE / REACTION_LANDING / REVEAL_LANDING / CHOICE_LANDING / CONSEQUENCE_LANDING / PROP_PAYOFF / RELATIONSHIP_LANDING / MOTION_CONTINUE / DIALOGUE_BUTTON / COMEDY_BUTTON / SUSPENSE_HOLD / TRANSITION_BRIDGE]

## 10.6 EXIT STATE
[what has changed at the end of this clip; do not summarize the entire story]

## 10.7 ENDING REASON
[one sentence explaining why this ending is required by the Beat/Scene. Required only for FADE_TO_BLACK / LIGHTS_DIM / SILHOUETTE / PULL_BACK / EMPTY_STREET or other strong closure devices.]

### Ending Anti-Cliche
Do not default to:
fade to black, lights dim, silhouette embrace, pull back to wide, empty street, rain continuing, character walking away, final piano note, looking into distance.
These are allowed only when explicitly justified by the upstream Story/Scene Contract.

## 11. END STATE
[exact final pose / gaze / position / prop state / camera framing; must connect to next shot]

## 12. CONTINUITY
[screen direction / axis / lighting / weather / prop / character state]

## 13. GUARDRAILS
[only known risks: identity drift, extra limbs, direction flip, environment morph, unwanted camera motion, style drift]

## MiniMax style rule
Use explicit sequential actions, clear spatial references, restrained camera movement, and one main action per clip. Do not ask the model to solve an entire multi-shot sequence inside one generation.

## Anime style rule (default, mandatory)
Default output style is 2D anime (SKILL.md §0.1). Every video prompt MUST carry explicit anime style markers: `2D anime style, cel shading, anime character design` (or the user-specified preset's markers). Never default to photoreal/live-action/3D render unless the user explicitly requested that style. Describe characters in anime terms (silver hair, crimson eyes, mature anime office lady) — no real-world age, ethnicity, or photoreal anatomy.

