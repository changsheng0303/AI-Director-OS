# Story Engine V1.7

## 1. 核心目标
从“事件列表”升级为“选择驱动的状态变化系统”。

### Story Equation
`Character Goal × Opposition × Stakes × Choice → State Change`

如果一个 Beat 没有改变目标、信息、关系、风险、时间或空间中的至少一项，则优先删除，而不是增加镜头。

## 2. Story Spine
`Premise → Dramatic Question → Theme → Character Want/Need → Opposition → Stakes → Inciting Incident → Progressive Complications → Midpoint Reframe → Crisis/Second Turn → Climax Choice → Consequence → Resolution`

短片可以压缩节点，但不能把“选择”和“后果”永久删除。

## 3. Character Engine
主角：
- Want：主动追求的外部结果
- Need：必须完成的内部改变
- Fear：会阻止行动的恐惧
- Belief：当前错误/局限性信念
- Strength：解决问题的有效能力
- Flaw：导致失败的习惯/盲点
- Contradiction：角色内部的矛盾
- Relationship Objective：对关键关系想得到什么
- Arc：从旧状态到新状态的可观察变化

## 4. Conflict Engine
每个核心冲突写成：
`Goal → Obstacle → Tactic → Resistance → Cost → New Tactic`

冲突不是“有人反对”，而是角色的当前策略无法低成本实现目标。

## 5. Escalation Ladder
每次升级至少改变一个维度：
- Stakes 更高
- 时间更少
- 阻力更强
- 信息更不完整
- 关系代价更高
- 可选方案更少
- 选择更不可逆

禁止连续三个 Beat 仅通过“更激烈的情绪”表示升级。

## 6. Midpoint Reframe
中点不是简单的“剧情过半”。必须至少发生一项：
- 目标重新定义
- 观众重新解释已知信息
- 对手关系改变
- 主角策略改变
- Stakes 从外部转向内部或反之

## 7. Crisis → Climax
Crisis：所有低成本方案失败。
Climax：角色必须选择一个有代价的方案。
Consequence：选择改变世界/关系/信息状态。

## 8. Scene Architecture
每场 Scene：
`Entry State → Objective → Tactic → Obstacle → Escalation → Turn → Consequence → Exit State`

Scene 不得只承担“展示设定”功能，除非展示本身改变观众知识或角色选择空间。

## 9. Scene Archetype Router
先判断场景的主叙事机制：
- `DISCOVERY`：发现信息
- `CONFRONTATION`：目标正面冲突
- `PURSUIT`：追逐/逃避
- `DUEL`：技能/意志对抗
- `JOURNEY`：移动中改变关系或信息
- `REUNION`：关系状态重置
- `DECISION`：选择与代价
- `REVEAL`：秘密揭示
- `COMEDY_SETUP_PAYOFF`：预期→误导→笑点→反应
- `ATMOSPHERE`：氛围，但必须承载信息/关系/主题变化

Archetype 只决定叙事问题，不直接规定镜头。

## 10. Audience Delta
每个 Shot 必须定义：
`audience_knows_before / audience_knows_after / delta`

如果 delta 为空：
- 允许作为纯情绪/节奏镜头，但必须说明 `rhythm_function`；
- 若连续两个以上无 delta，必须检查是否可合并。

## 11. Promise Registry
所有重要悬念、承诺、未解决问题记录：
`promise_id / seed / expected_payoff_window / payoff / status`

## 12. State Ledger
持续追踪：
- character_state
- relationship_state
- knowledge_state
- prop_state
- location_state
- time_state
- risk_state

任何 Shot 只能从当前 ledger 的状态出发。

## 13. Ending Diversity
结尾不是“漂亮画面”，而是状态落点。优先从：
`ACTION_COMPLETE / REACTION / REVEAL / CHOICE / CONSEQUENCE / PROP_PAYOFF / DIALOGUE_BUTTON / MOTION_CONTINUE / SUSPENSE_HOLD / TRANSITION`
中选择。

## 14. Story QA 红线
- 角色无目标
- 行为无动机
- 冲突无阻力
- 升级无代价
- 高潮无选择
- 选择无后果
- 伏笔无回收
- 场景只换地点不换状态
- 镜头为炫技增加事件
- 结尾用模板代替剧情
