# AI 2D Animation Skill V1.7

V1.7 的核心升级不是增加更多镜头模板，而是解决 AI 动画最常见的两个问题：**剧情事件链跳跃**与**相邻镜头跳脱**。

## 核心生产链
`Brief → Story Contract → Character/Relationship Arc → Scene Contract → Beat Chain → Spatial Plan → Shot Adjacency → Shot Contract → Narrative Camera → Video Compiler → Model Adapter → Generate → QA → Repair → Edit`

## V1.7 五个核心升级
1. **Story Architecture Engine**：Want/Need、Stakes、Turning Points、Choice、Consequence、Theme、Foreshadow/Payoff。
2. **Beat Chain**：每个 Beat 必须由 Trigger → Action → Result → New State 驱动，避免事件流水账。
3. **Scene Contract**：每场戏锁定 Goal/Conflict/Turn/Exit State 与空间地理。
4. **Shot Adjacency Contract**：每镜必须知道上一镜发生了什么、自己从哪里开始、结束后下一镜怎么接。
5. **Spatial Continuity Engine**：空间锚点、视线、方向、动作阶段、道具、光向共同防止“镜头跳脱”。

## 最重要的原则
> **不要用 Prompt 修复剧情问题；不要用运镜修复空间问题；不要用 Close-up 掩盖缺少 Establishing 的问题。**

问题定位顺序固定为：
`Story Causality → Scene Geography → Beat Transition → Shot Adjacency → Camera → Prompt`

内容分级与安全规则保持原 Skill 的既有内容，不在本次版本中调整。


## V1.7 重点升级
- Story Ending Architecture：区分 Clip Landing / Scene Exit / Sequence Resolution
- Ending Function + Exit State + Ending Reason
- Ending Anti-Cliche：禁止把熄灯、淡黑、剪影、拉远、空镜、雨景等当作默认结尾
- Ending Diversity QA
- Prompt Compiler 不得自行发明结尾
- 保留 V1.5 的 Story Contract、Beat Chain、Spatial Continuity、Shot Adjacency

## V1.7 Research Basis
V1.7 adds a public GitHub methodology benchmark covering AI storyboard, director, screenwriter, end-to-end AI video production, scene routing, persistent story state, per-clip QA and prompt compilation. See `references/github-benchmark-v1.7.md`.
