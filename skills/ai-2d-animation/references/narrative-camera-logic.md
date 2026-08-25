# Narrative Camera Logic V1.3

## 目标
镜头不是装饰性的摄影动作，而是控制“观众现在知道什么、角色知道什么、什么被隐藏、何时重新解释信息”的叙事工具。

## 决策链
`Story Function → Audience Knowledge → Character Knowledge → Information Gap → Emotional Objective → Spatial Relationship → Composition → Shot Size → Camera Motion → Lens/Effects`

不得反向以“酷镜头”寻找剧情理由。

## 核心字段
- `visual_question`：这个镜头让观众观察/思考什么？
- `audience_knowledge`：镜头结束时观众应该知道什么？
- `character_knowledge`：角色此刻知道什么？
- `information_withheld`：有意不让观众知道什么？
- `reveal_point`：信息何时/通过什么视觉动作揭示？
- `emotional_landing`：镜头结束后观众应该落在哪种情绪上？
- `camera_strategy`：控制信息的总体摄影策略。
- `camera_logic`：`ESTABLISH / OBSERVE / WITHHOLD / ALIGN / ESCALATE / REVEAL / MISDIRECT / RECONTEXTUALIZE / CONTRAST / RELEASE`
- `camera_necessity`：如果删掉镜头运动，观众会失去什么？只能回答“信息 / 情绪 / 空间认知 / none”。

## Camera Logic 定义
| Logic | 用途 |
|---|---|
| ESTABLISH | 建立空间、人物关系、尺度 |
| OBSERVE | 让观众观察表演而不干预 |
| WITHHOLD | 主动隐藏关键视觉信息 |
| ALIGN | 将观众视角与角色视线/主观认知对齐 |
| ESCALATE | 逐步增加压力、信息密度或运动能量 |
| REVEAL | 通过构图/运动揭示此前隐藏的信息 |
| MISDIRECT | 让观众形成暂时错误判断 |
| RECONTEXTUALIZE | 新信息重新解释前面镜头 |
| CONTRAST | 通过景别/空间/运动反差制造意义 |
| RELEASE | 在高潮后释放信息与情绪压力 |

## Anti-Decoration Rule
每一次非必要运镜必须通过以下问题：
1. 删除它，观众是否失去信息？
2. 删除它，观众是否失去情绪变化？
3. 删除它，空间关系是否变得不可理解？

如果三项均为“否”，默认改为 `Static`。

## 信息差原则
高阶镜头语言优先寻找：
- 观众知道、角色不知道
- 角色知道、观众不知道
- 双方都不知道，但镜头先发现
- 观众与角色共同误判，再通过空间/道具/反应重新解释

## 常见高级结构
`Observe → Withhold → Align → Misdirect → Reveal → Recontextualize → Release`

## QA
- Camera Logic 是否服务 Beat？
- Information Withheld 是否真实存在？
- Reveal Point 是否可观察？
- Misdirect 是否有后续重新解释？
- Camera Motion 是否有叙事必要性？
- 连续镜头是否避免重复同一种 Logic？


## V1.4 Camera Necessity Scoring
对非 Static 镜头执行三项评分：
- Information Gain：镜头是否新增、隐藏或重排信息？
- Emotion Gain：镜头是否改变观众情绪强度或落点？
- Spatial Gain：镜头是否建立/重建空间关系？

建议评分 0–2：
- 0 = 无变化
- 1 = 有帮助
- 2 = 不可替代

总分 < 2：默认 Static；总分 ≥ 2：允许保留运镜。Hero Shot 可由导演 Override，但必须记录原因。

## V1.4 Shot Atomicity
单个 AI 视频片段优先只承担：
1. 一个主动作变化（例如“抬头”）；
2. 一个主要镜头变化（例如“slow push-in”）；
3. 一个情绪落点。

若同时包含“人物走路 + 转身 + 双人互动 + 大幅运镜 + 场景揭示”，优先拆成多个可拼接 Shot。

## V1.4 Information Beat Ordering
Video Prompt 内部动作顺序优先写成：
`Start State → Trigger → Primary Action → Reaction → Camera Response → Secondary Motion → Hold → End State`
不要把多个动作并列堆在同一句。模型应先完成主动作，再执行次级动作。
