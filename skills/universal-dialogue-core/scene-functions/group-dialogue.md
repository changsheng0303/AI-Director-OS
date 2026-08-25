# Scene Function — Group Dialogue

```yaml
function_output:
  core_problem: 三人以上同时拥有不同目标、信息和联盟，场面不能退化成轮流发言。
  preferred_tactics: [coalition, interrupt, redirect, side_with, isolate, mediate, observe, expose, withhold]
  beat_patterns:
    - driver_move -> resistor -> third_party_shift -> coalition_change -> decision
    - topic -> split -> interruption -> alliance -> new_target
  information_rules:
    - 明确谁知道什么；不要让群体自动共享所有信息。
  pressure_rules:
    - 发言权、注意力和联盟要变化；不平均分配台词。
    - 追踪当前 attention_target 与 floor_holder；注意力转移必须改变至少一人的策略。
  payoff_conditions:
    - 联盟、决策、权力、被怀疑对象、行动方向至少一项变化。
  anti_patterns:
    - 所有人依次发表完整意见
    - 每个人发言长度近似
    - 沉默角色完全不影响场面
  extra_checks:
    - 谁推动？谁阻止？谁是目标？谁掌握关键事实？谁改变联盟？
    - 谁当前拥有发言权？谁的沉默/动作让注意力转向了谁？
```
