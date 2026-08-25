# Story Craft V1.6

> 本文件解决“剧情为什么跳、角色为什么突然变、情绪为什么突然变、镜头为什么没有东西可拍”。

## 1. Story Contract
必须建立：`premise / story_question / theme / protagonist_want / protagonist_need / opposition / stakes / turning_points / climax_choice / consequence / resolution`。

## 2. Character Motivation
每个主要行为必须能追溯到：`want + need + relationship + immediate_trigger`。

禁止“剧情需要所以角色这样做”。

## 3. Beat Causality
每个 Beat：
`Trigger → Desire → Action → Resistance → Result → Choice/Cost → New State`。

四问：
- 为什么现在？
- 为什么他做？
- 为什么这样做？
- 做完以后改变了什么？

## 4. Scene Dynamics
`Goal → Conflict → Tactic → Complication → Turn → Exit State`。
Scene 必须改变至少一个状态变量。

## 5. Emotion Ladder
情绪变化必须有过渡节拍。15s 内最多 3 个主要情绪级跃迁；超过则拆 Beat。

## 6. Information Flow
每个信息点记录：`who_knows / when_known / withheld / reveal / payoff`。每个 WITHHOLD 必须有 REVEAL 或明确留悬念到后续 Scene。

## 7. Escalation
重复尝试必须提高至少一个：`risk / cost / time pressure / relationship consequence / choice difficulty`。

## 8. Relationship Arc
关系变化必须通过可观察行为体现：
`distance → attention → trust/distrust → choice → consequence`。
不要只写“关系升温”。

## 9. Story Risk List
新增：
- `RISK-05 EVENT_CHAIN`：只有事件没有角色选择。
- `RISK-06 MOTIVATION_GAP`：行为无即时动机。
- `RISK-07 STAKES_FLAT`：冲突不升级。
- `RISK-08 SCENE_TELEPORT`：场景切换没有空间/时间桥。
- `RISK-09 SHOT_DISCONTINUITY`：相邻镜头状态继承不足。
- `RISK-10 PAYOFF_MISSING`：伏笔没有回收。
- `RISK-11 RELATION_JUMP`：关系变化缺少可见节拍。

## 10. Gate 1 QA
- Story Contract 完整？
- 每 Beat 有因果链？
- 每 Scene 有 Turn？
- Stakes 升级？
- 角色有 Want/Need/Choice？
- 伏笔有 Payoff？
- 情绪有过渡？
- 信息点 ≤ 3/15s？
- 相邻镜头有 ≥3 个连续性锚点？
- 是否存在 Scene/Shot Teleport？


## 12. Ending Discipline
“结尾”必须是状态落点，不是视觉装饰。
先写 `exit_state`，再选 `ending_function`，最后写最后一帧。

### Ending Test
最后一个 Beat 如果只是：
- 熄灯
- 淡黑
- 拉远
- 背影
- 雨景
- 空镜
- 拥抱
- 看远方

且没有新的 `result / consequence / choice / information`，则判定 `ENDING_CLICHE`。

### Anti-Overclosure
普通 Shot 不得被写成“终章”。只有 Scene/Sequence/episode 结束才允许高强度 closure。
