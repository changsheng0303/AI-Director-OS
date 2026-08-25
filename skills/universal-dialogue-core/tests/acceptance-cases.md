# Universal Dialogue Core v2.1 — Acceptance Cases

目标：验证**不加载任何 Genre Adapter**时，Core 是否能稳定覆盖多种台词机制。

重大修改后至少跑 T01–T08；正式版本建议跑全部。

## T01 — Voice Separation

3 个稳定人格、关系和表达方式不同的人面对同一事件。

要求：去掉角色名后，主要台词仍能凭信息选择、策略、句式、节奏区分。

失败：`VOICE_COLLAPSE`。

## T02 — Knowledge Boundary

A 知道秘密；B 完全不知道；C 只有怀疑。

要求：B 不泄漏事实；C 只能使用怀疑强度的语言；A 即使撒谎也不能调用未知事实。

失败：`KNOWLEDGE_LEAK`。

## T03 — Conflict Without Shouting

两人目标正面冲突，但人物都克制。

要求：冲突通过边界、重构问题、条件与策略变化成立，不依赖大喊。

## T04 — Concealment

A 想隐藏真实原因，B 问了一个必须回应的问题。

要求：A 使用可追踪的隐藏策略；B 的怀疑变化来自实际回应，而非作者暗示。

## T05 — Interrogation Fairness

提问者通过细节验证说法。

要求：每轮问题缩小未知；结论强度不超过证据；无凭空推理。

## T06 — Negotiation

双方都有底线和可交换项。

要求：至少一次策略变化与一次有代价的让步；不能靠一句大道理达成一致。

## T07 — Intimacy Without Genre

两人关系靠一次有限度的自我暴露发生变化。

要求：不依赖恋爱套路；重点是风险、边界、回应和关系距离。

## T08 — Reconciliation

关系受损后尝试修复。

要求：修复具体问题；解释不替代责任；不强制立即原谅。

## T09 — Exposition Compression

输入中包含大量观众必须知道但人物部分已知的信息。

要求：只保留当前行动所需最小事实；利用问题、纠正、任务和反应释放信息。

## T10 — Casual Exchange Value

熟人围绕一件小事互动。

要求：没有大冲突也要存在微目标、关系习惯或微状态变化；不是寒暄流水账。

## T11 — Emotional Turn

角色一开始克制，受到明确刺激后控制方式失效。

要求：情绪变化有触发因果；高情绪不自动等于长演讲。

## T12 — Group Dialogue Asymmetry

4 人群戏。

要求：发言量不平均；至少有 driver / resistor；联盟或注意力发生变化；沉默者可通过反应参与。

## T13 — Tactic Shift

人为让角色第一次请求失败。

要求：第二次不能只换近义词，必须改变策略。

失败：`TACTIC_FLATLINE`。

## T14 — False Subtext Guard

要求生成“有潜台词”的普通对话。

要求：潜台词必须来自关系风险与行为目的，不得使用无原因的含糊句制造高级感。

失败：`FALSE_SUBTEXT`。

## T15 — Author Speak Guard

场景主题明显但角色本人并不善于抽象表达。

要求：不得突然说出作者总结或主题宣言。

失败：`AUTHOR_SPEAK`。

## T16 — Rewrite Locality

只植入一个 Voice 问题。

要求：只改语言层，不重做场景目标和 Beats。


## T17 — Functional Proportionality

角色只需要完成一个简单确认或任务交接。

要求：允许直接、简洁；不得强行加入秘密、冲突、情绪高潮或多层潜台词。

失败：`OVERDRAMATIZATION`。

## T18 — Interactive Micro-Change

熟人围绕小事互动，有轻微注意力差异但无重大冲突。

要求：只产生微关系/习惯变化，不升级成争吵或告白级别。

## T19 — Listener Model / Second-Order Knowledge

A 知道秘密 X；B 不知道 X，但 A 错误地以为 B 已经知道一部分。

要求：A 的策略基于自己的错误判断，而不是基于客观真相；B 的回应不能凭空拥有 X。

失败：`LISTENER_MODEL_BREAK`。

## T20 — Turn Coupling

两人立场明确但不允许写成轮流演讲。

要求：每一轮都能指出它回应、拒绝、修正、转移或挑战了上一轮的什么 move。

失败：`TURN_DECOUPLING`。

## T21 — Deliberate Non-Answer

A 问必须回应的问题，B 有意不正面回答。

要求：不回答本身必须是可追踪策略，并改变 A 的下一步；不能只是作者逃避信息。

## T22 — Function Phase Transition

场景前半为 interrogation；新证据出现后，真正的核心变为 conflict 或 emotional_turn。

要求：仅 DEEP 允许一次顺序切换；不得并行加载两个 primary；必须存在明确 transition trigger。

## T23 — Dialogue Load Transition

场景从普通互动开始，某句意外信息将负荷从 INTERACTIVE 推到 DRAMATIC。

要求：前半保持轻量，不提前预演高潮；触发后才提升策略/压力复杂度。

## T24 — Exit Discipline

场景已经完成决定或关系变化。

要求：payoff 后不再追加主题总结、重复确认或“我们都明白了”式尾巴。

Soft failure：`TAIL_DRIFT`。

## T25 — Claim / Lie / Promise Continuity

跨两个场景，角色已经公开说过一个版本的谎言并做出一个承诺。

要求：后续台词保持版本一致；若改口必须有新证据、被抓矛盾、坦白或策略转换等触发。

失败：`DECEPTION_CONTINUITY_BREAK`。

## T26 — Misunderstanding Repair

角色误解了上一句的指代或意图。

要求：后续必须发生 clarify / correct / rephrase / abandon 之一；不得无解释地突然恢复精准理解。
