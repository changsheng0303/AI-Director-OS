# Suspense / Mystery Dialogue Adapter v1.0

## Mission

通过**信息不对称、错误确信和策略性回答**制造张力，同时保证线索公平与人物知识边界。

## Information Ledger

进入关键场景前内部维护：

```yaml
knowledge_ledger:
  fact:
    true_state:
    known_by: []
    believed_by: []
    lied_about_by: []
    suspected_by: []
    reveal_window:
```

## Preferred Tactics

- probe：用旁敲侧击确认对方知道多少；
- partial_truth：说真的一部分，隐藏关键部分；
- answer_adjacent：回答相邻问题而不是核心问题；
- trap_question：让对方在细节上暴露知识；
- false_confidence：表现出“我已经知道”，逼对方补充；
- redirect：主动把注意力移到更安全的话题；
- controlled_reveal：释放足以改变局面的最小信息；
- silence_pressure：利用不回答让对方继续说。

## Beat Bias

`Question → Safe Answer → Probe → Inconsistency → Pressure → Partial Reveal → New Question`

重要揭示后通常应产生新的未知，而不是一次解释完毕。

## Rhythm Rules

- 线索台词尽量短且可回看；
- 关键矛盾点周围减少无关语言；
- 同一秘密不要被连续三次不同角色解释；
- 谎言必须符合撒谎者当前已知信息；
- 怀疑不等于确定，措辞强度必须对应证据强度。

## Subtext Rules

悬疑对白的表层通常是“谈某件事”，深层往往是：

- 我在判断你是否危险；
- 我在确认你知道多少；
- 我需要你相信错误版本；
- 我想让你主动暴露信息；
- 我不确定自己是否应该相信你。

## Anti-Patterns

- 反派主动完整解释计划；
- 角色凭空推理出没有证据的信息；
- 为制造悬念故意让角色不说本来必然会说的话；
- 揭秘等于大段 exposition；
- 通过含糊代词制造假悬念；
- 观众被隐瞒了角色已经明确知道的必要信息，却没有叙事理由。

## Payoff Rule

每个关键悬疑场至少产生一种：

- evidence gained；
- belief changed；
- lie exposed；
- suspect narrowed；
- trust shifted；
- mystery deepened with fair clue。

## Extra Checks

- 线索是否在揭示前已经公平存在？
- 知识账本有没有泄漏？
- 角色的确信程度是否与证据匹配？
- 揭示后是否真正改变下一步行动？
