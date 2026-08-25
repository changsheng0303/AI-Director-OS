# Model Capability Matrix V1.2

模型名称不是规则；能力是规则。

## Capability Vector
Score each candidate 0-5:
- character_consistency
- reference_adherence
- i2i
- i2v
- motion_complexity
- camera_control
- start_end_frame
- style_stability
- latency
- cost_efficiency

## Routing
`Shot Requirement → Weighted Capability Score → Primary → Fallback`

Suggested weights by shot:
- Character-heavy: consistency 30, reference 20, style 15.
- Action-heavy: motion 30, camera 20, start/end 15.
- Hero: style 25, motion 25, camera 20, reference 15.
- Simple dialogue: consistency 30, latency 20, cost 20.

## Rules
- Missing capability is a hard risk, not a reason to distort creative intent.
- If two candidates are close, prefer lower expected cost/latency.
- Record scores and rationale with each Route Plan.
