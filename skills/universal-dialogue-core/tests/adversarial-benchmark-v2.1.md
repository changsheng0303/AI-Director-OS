# Universal Dialogue Core — Adversarial Benchmark v2.1

目的：专门攻击 V2.0 在“通用母模板”层面的盲区。**禁用所有 Genre Adapter。**

本组不是题材测试，而是对话机制测试。

| ID | 对抗场景 | 主要压力点 | 通过标准 |
|---|---|---|---|
| B01 | A 隐瞒 X，误以为 B 已知一半 | second-order knowledge | A 的说法符合自己对 B 的判断 |
| B02 | 审问者其实不知道答案，却装作已经知道 | listener model + bluff | bluff 不创造客观证据 |
| B03 | 双方都错误判断对方掌握的信息 | mistaken beliefs | 策略来自主观认知，事实边界仍正确 |
| B04 | 谈判者隐藏底线并判断对方是否察觉 | listener model | 不过早暴露底线 |
| B05 | 两人立场冲突，容易写成轮流演讲 | turn coupling | 每轮真实咬合上一轮 move |
| B06 | 被问者故意不答 | deliberate non-answer | 非回答本身有 tactic，并改变下一轮 |
| B07 | 指代误解 | repair | clarify/correct/rephrase/abandon 可追踪 |
| B08 | 一方纠正事实后对方必须改策略 | reactive update | 纠正真实改变后续表达 |
| B09 | interrogation → emotional_turn | function phase shift | 明确 trigger；顺序切换，不并行 |
| B10 | concealment → conflict | function phase shift | 秘密暴露是转折触发 |
| B11 | negotiation → conflict | function phase shift | 谈判空间消失后才转冲突 |
| B12 | reconciliation → intimacy | function phase shift | 先完成具体修复，再进入有限暴露 |
| B13 | casual/interactive → dramatic | load escalation | 高负荷只在 trigger 后启动 |
| B14 | dramatic → interactive | load de-escalation | 冲突解除后语言复杂度下降 |
| B15 | payoff 已完成但模型想继续总结 | exit discipline | 删除冗余尾巴 |
| B16 | 目标明确被阻断 | exit discipline | 不再重复同一诉求 |
| B17 | 跨场景谎言版本 | deception continuity | active lie 保持一致或有触发改口 |
| B18 | 已作出的承诺 | promise continuity | 后续行为/台词记得承诺 |
| B19 | 重要问题被延后 | open loop | unresolved question 进入 ledger |
| B20 | 矛盾已出现但无人注意 | observed vs unobserved contradiction | 不能自动让所有人识破 |
| B21 | 四人群戏注意力突然转向第三人 | attention pivot | target/driver/联盟随之变化 |
| B22 | 沉默者用动作改变局势 | nonverbal participation | 其他人策略受其反应影响 |
| B23 | 权力关系变化后发言权改变 | floor/status dynamics | 插话/让话/回避随权力变化 |
| B24 | 必要信息传递同时有人隐瞒关键部分 | exposition + concealment | primary 单一，另一机制进入 tactic |

## Pass Rule

- Core spec coverage 平均 >= 9.5/10；
- 任一核心机制不得 < 9.0；
- 新增规则不得依赖 Genre；
- 不允许为了通过 B09–B12 把所有场景都改成多 Function；
- 不允许为了通过 B01–B04 建立无限层心智模型，只追踪会改变当前策略的二阶认知。
