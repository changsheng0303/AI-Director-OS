# Story Ending & Scene Landing V1.6

## 目标
解决 AI 动画中“每个 Prompt 最后都熄灯、淡黑、远景、雨停、人物背影、剪影拥抱”的模板化结尾问题。

核心原则：
> **结尾不是一个漂亮画面，而是一个状态变化被观众看见的瞬间。**

## 一、先区分三种 Ending
### 1. Clip Landing
单个 4–10 秒视频片段的结束。只负责把当前动作/反应落稳，并把 End State 交给下一镜。
- 默认不解决整个 Scene。
- 默认不制造“终局感”。
- 不需要 fade out。
- 不需要总结主题。

### 2. Scene Exit
一个 Scene 的结束。必须体现 `scene_turn / exit_state`，例如：
- 角色做出下一步行动；
- 信息被确认/隐藏；
- 关系发生可观察变化；
- 目标失败/转移；
- 新地点被决定。

### 3. Sequence / Episode Resolution
只有在真正的段落、场次或集尾才允许承担完整的情绪/主题回收。

## 二、Ending Selection Pipeline
每个 Ending 必须按以下顺序生成：
`Story Change → Exit State → Ending Function → Observable Action/Image → Last Frame`

Ending Function 从以下类型中选择一个：
1. `ACTION_COMPLETE`：动作完成，直接落在结果。
2. `REACTION_LANDING`：人物反应成为最后信息。
3. `REVEAL_LANDING`：新信息刚被看见。
4. `CHOICE_LANDING`：角色做出选择，画面停在选择后的第一状态。
5. `CONSEQUENCE_LANDING`：选择/动作的后果出现。
6. `PROP_PAYOFF`：道具/视觉母题完成回收。
7. `RELATIONSHIP_LANDING`：关系状态出现可观察变化。
8. `MOTION_CONTINUE`：动作/运动向下一镜继续，不强行停。
9. `DIALOGUE_BUTTON`：一句关键对白后的表情/反应落点。
10. `COMEDY_BUTTON`：笑点或反差完成后的反应。
11. `SUSPENSE_HOLD`：信息故意不揭示，停在一个可解释的未知状态。
12. `TRANSITION_BRIDGE`：用视线、动作、声音、形状或空间把下一镜引入。

## 三、反模板规则
以下结尾不得作为默认答案：
- 熄灯 / 灯光变暗
- Fade to black
- 人物剪影
- 远景人物背影
- 雨继续下 / 雨停
- 风吹头发
- 镜头拉远
- 空镜停留
- 人物离开画面
- 两人拥抱作为万能收束
- “看向远方”
- “城市灯光闪烁”
- “音乐最后一个音符”
- 任何仅因为“电影感”而加入的视觉句号

这些表达只有在 `ending_function` 明确要求且故事已有因果铺垫时才能使用。

## 四、Ending Diversity
同一 Scene 内连续两个 Shot 不得使用同一种 Ending Function。
同一 Sequence 内不得超过 1 次 `FADE_TO_BLACK`，且必须是段落真正结束。
如果最近 3 个 Prompt 中出现相同的 ending motif，下一 Prompt 必须优先换用：
`ACTION / REACTION / REVEAL / CHOICE / CONSEQUENCE / PROP / DIALOGUE / SUSPENSE / BRIDGE`。

## 五、Ending 必须来自故事，而不是来自美术
最后一帧必须能回答：
- 发生了什么变化？
- 谁的状态改变了？
- 下一镜从哪里接？
- 这个画面为什么必须是最后一帧？

如果只能回答“这样更有电影感”，则 FAIL。

## 六、开放式结尾
开放结尾不是“什么都没发生”。
必须留下一个具体未决变量：
`unanswered question / unresolved goal / pending action / changed relationship / visible consequence`。

## 七、短视频特殊规则
4–10 秒视频：
`Start State → Trigger → Primary Action → Reaction/Result → Landing`
不要在一个片段里同时完成“冲突 + 高潮 + 主题总结 + 淡出”。

## 八、Ending QA
- ending_function 是否明确？
- ending 是否由 Beat/Scene 的状态变化推出？
- 是否出现模板化结尾？
- 是否需要 fade/dim？如果是，为什么？
- 最后一帧是否可作为下一镜 Start State？
- 是否把一个普通 Shot 错误地拍成“全片大结局”？
