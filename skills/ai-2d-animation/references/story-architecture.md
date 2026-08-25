# Story Architecture V1.7

## 目标
把“有创意”变成“有动力、有选择、有后果、有回收”的故事，而不是事件列表。

### Story Spine
`Premise → Story Question → Theme → Want/Need → Opposition → Stakes → Inciting Incident → Turning Points → Climax Choice → Consequence → Resolution`

### Character Engine
每个主要角色至少定义：
`Want / Need / Fear / Flaw-or-Belief / Strength / Contradiction / Relationship Objective / Arc`

Want 是角色主动追求的外部目标；Need 是角色真正需要完成的内部改变。两者最好存在张力。

### Conflict Engine
每个核心冲突至少包含：
`Goal / Obstacle / Tactic / Resistance / Cost`
禁止只写“发生冲突”，必须说明谁想得到什么、谁阻止、怎么阻止、失败付出什么。

### Escalation Ladder
`Problem → Attempt → Complication → Costlier Attempt → Point of No Return → Climax`
连续 Beat 如果没有改变 Stakes、选择难度或关系代价，则标记 `REPETITIVE_BEAT`。

### Choice Rule
高潮优先来自角色选择。偶然事件可以改变局势，但不能替角色完成核心选择。

### Theme Rule
主题不是一句漂亮话。它必须影响：
`Character Belief → Choice → Consequence → Resolution`。

### Foreshadow/Payoff
重要道具、台词、动作、视觉母题至少遵循：
`Seed → Reinforcement → Payoff`。
Payoff 应该让观众产生“原来如此”，而不是“作者突然想到了”。

### Information Design
每个信息点记录：
`who_knows / when_known / withheld / reveal_method / payoff_effect`。
15 秒短片建议 2–3 个核心信息点；超过时优先删除或合并，而不是加镜头。

### Story Density
短视频不是把长故事压缩得更快，而是减少故事变量。
优先保留：
`1 个核心目标 + 1 个核心阻力 + 1 个关键选择 + 1 个结果`。

### Story QA
- 是否有主角目标？
- 是否有阻力？
- 是否有 Stakes？
- 是否有因果链？
- 是否有角色选择？
- 是否有状态变化？
- 是否有升级？
- 是否有结局回收？
- 是否存在纯事件堆叠？
- 是否存在“为了镜头而增加剧情”的反向创作？


## Ending Architecture V1.7
故事结尾、Scene Exit 与单个 Video Clip End State 必须分离。
- Clip End：完成当前动作/反应，不承担整场戏总结。
- Scene Exit：体现 Scene Turn 后的状态。
- Sequence/Ending：才承担主题或情绪回收。

每个 Scene/Sequence 必须定义：
`ending_function / exit_state / observable_consequence / next_state`

禁止把“电影感结尾”当作默认剧情解决方案。Ending 必须由 `result / choice / consequence / information_delta / relationship_delta` 中至少一个推出。

## Ending Anti-Template
除非剧情明确需要，不得默认使用：
`lights_dim / fade_to_black / silhouette / pull_back / empty_street / rain_continue / character_walks_away / final_music_note / embrace`.

如果模型生成这些模板化结尾，Story QA 标记 `ENDING_CLICHE`，重新选择 Ending Function，而不是继续润色描述。

## Scene Landing Rule
每个 Scene 最后一个 Beat 不等于“画面变漂亮”，而是：
`Turn → Consequence → Exit State`.
最后一镜优先展示 consequence 或 next action。

## Story Prompt Rule
剧情提示词不得预设“最后一镜”。必须先生成故事状态，再由 Storyboard Artist 选择 Ending Function。
