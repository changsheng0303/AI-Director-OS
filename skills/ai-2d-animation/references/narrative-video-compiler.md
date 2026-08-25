# Narrative Video Compiler V1.6

## 目标
把导演层的“叙事意图”编译成模型层可执行的 Video Prompt。模型层不得重新发明剧情。

## 两层结构
### Director Layer
`Story Function → Beat Change → Audience/Character Knowledge → Information Gap → Emotional Objective → Visual Motif → Camera Logic → Camera Necessity → Ending Function → Exit State`

### Execution Layer
`Locked Subject/Environment → Exact Start State → Trigger → Primary Motion → Acting/Reaction → Camera Response → Secondary Motion → Timing → Ending Function → Exact End State → Continuity → Guardrails`

## 编译原则
1. 一个片段只保留一个主动作与一个主要镜头变化。
2. 动作按时间顺序写，不使用“同时发生很多事”的并列长句。
3. 主动作优先于次级动作；角色表演优先于装饰效果。
4. Camera Response 必须对应 Camera Logic。
5. End State 必须可直接成为下一 Shot 的 Starting State。
6. 视觉意象必须写明其叙事功能，例如“雨遮挡信息”“玻璃制造隔离”。
7. Negative/Guardrails 只列已知风险。

## MiniMax Adapter
针对 Hailuo 类模型：
- 优先使用明确的动作动词和空间关系。
- 用短段落或标签式顺序表达，不用长篇文学隐喻。
- 复杂镜头拆成多个 6–10 秒片段再剪辑；官方资料显示 Hailuo 2.3 支持文本/图像到视频并提供 6/10 秒档位。
- 若使用 Start/End Frame，Start/End 必须分别锁定，Prompt 只描述两者之间的可观察变化。
- 不把音乐、对白、复杂音效当作视觉模型必须执行的核心动作；声音进入后期或独立音频流程。


## Ending Compiler Rules V1.6
1. Never invent an ending visual before reading `exit_state`.
2. `ending_function` is selected from `references/story-ending.md`.
3. The last frame must visualize the state change, not summarize the whole story.
4. A clip that continues into another shot should prefer `ACTION_COMPLETE`, `REACTION_LANDING`, `REVEAL_LANDING`, `MOTION_CONTINUE`, or `BRIDGE`.
5. `FADE_TO_BLACK`, `LIGHTS_DIM`, `SILHOUETTE`, `PULL_BACK`, `EMPTY_STREET`, `RAIN_CONTINUE`, and similar closure motifs are opt-in only.
6. If a prompt contains one of those motifs without an explicit `ending_reason`, compiler must replace it with a state-derived landing.
7. Do not add a final music note, breath, wind, rain, or atmospheric hold merely to make the prompt feel cinematic.
8. The prompt must not resolve a story problem that the upstream Story Contract leaves unresolved.
