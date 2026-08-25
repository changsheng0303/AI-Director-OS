# Scene Function — Interrogation

```yaml
function_output:
  core_problem: 一方试图缩小未知，另一方决定提供、扭曲或拒绝信息。
  preferred_tactics: [probe, verify_detail, trap_question, false_confidence, silence_pressure, timeline_check, contradiction]
  beat_patterns:
    - question -> answer -> verification -> inconsistency -> pressure -> new_information
    - broad_prompt -> narrow_detail -> contradiction -> choice_to_reveal_or_resist
  information_rules:
    - 怀疑程度必须与证据强度匹配。
    - 结论不得超过可见线索。
    - 提问者可以 bluff“我已经知道”，但 bluff 不等于真实证据；被问者只根据自己认为提问者掌握的程度做反应。
  pressure_rules:
    - 问题逐步缩小，不重复同一问题。
  payoff_conditions:
    - 获得证据、改变信念、暴露谎言、缩小范围或改变下一步行动。
  anti_patterns:
    - 凭空推理
    - 被问者主动完整解释全部事实
    - 提问者重复问同一句
  extra_checks:
    - 每轮问题新增了什么可验证信息？
    - 提问者是在利用真实证据，还是利用对方对其知识状态的误判？
```
