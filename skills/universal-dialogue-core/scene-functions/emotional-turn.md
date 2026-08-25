# Scene Function — Emotional Turn

```yaml
function_output:
  core_problem: 角色当前的情绪控制方式失效，必须改变表达策略或做出新的选择。
  preferred_tactics: [contain, deflect, deny, crack, partial_admission, direct_choice, withdraw]
  beat_patterns:
    - containment -> trigger -> failed_control -> exposure -> response -> new_state
    - pressure -> denial -> contradiction -> break_or_choice
  information_rules:
    - 情绪变化要由已发生的刺激触发，不能凭空跳档。
  pressure_rules:
    - 情绪越高，未必话越多；可短句化、破碎化、沉默化。
  payoff_conditions:
    - 角色承认/拒绝某事，关系改变，决定改变，或控制方式改变。
  anti_patterns:
    - 角色完整讲解自己的心理状态
    - 用长演讲代替情绪转折
    - 没有触发就突然爆发
  extra_checks:
    - 哪个具体刺激让原策略失效？
```
