# Prompt Compiler V1.7

## 原则
Prompt 是编译结果，不是第二个编剧。

### 输入优先级
1. Story Contract
2. Scene Contract
3. Beat Chain
4. Spatial Plan
5. Shot Adjacency
6. Shot Contract
7. Model Adapter

## Video Prompt Formula
`Context Lock → Subject State → Single Primary Action → Secondary Motion → Camera Response → Environment Motion → Audio Cue → Exit State → Constraint`

## 动作顺序
每个视频 Clip 优先一个主动作，最多两个相互依赖的次动作。
动作写成：
`start → trigger → action → reaction → settle`

## 不允许
- 自动添加新剧情
- 自动增加新角色
- 自动改变地点
- 自动添加“熄灯/淡黑/剪影/拉远”作为结尾
- 用 8K、masterpiece、cinematic 等形容词替代可执行动作

## MiniMax/短时视频
优先：
- 明确主语
- 明确起止状态
- 顺序动作
- 单一镜头运动
- 明确空间锚点
- 少量环境动态

复杂动作拆片，而不是把所有动作堆进一个 Prompt。

## Prompt Trace
每条 Prompt 记录：
`story_id / scene_id / beat_id / shot_id / source_version / locked_variables / changed_variables / ending_function / model_adapter / assumptions`
