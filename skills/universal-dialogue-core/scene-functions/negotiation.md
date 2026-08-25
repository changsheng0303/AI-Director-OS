# Scene Function — Negotiation

```yaml
function_output:
  core_problem: 双方都想改变对方决定，但仍存在可交换、可让步或可重新定义的空间。
  preferred_tactics: [offer, condition, anchor, concession, reframe_value, deadline, walkaway, package_trade]
  beat_patterns:
    - ask -> refusal -> value_reframe -> condition -> concession -> agreement_or_walkaway
    - anchor -> counter -> reveal_priority -> trade -> decision
  information_rules:
    - 不要让角色过早暴露自己的底线。
    - 角色对“对方是否已经看穿底线”的判断会改变报价、让步与退出策略。
  pressure_rules:
    - 每次让步都应换取东西；否则只是单方面屈服。
  payoff_conditions:
    - 条件变化、联盟变化、承诺、拒绝或明确下一步。
  anti_patterns:
    - 双方突然因为一句大道理达成一致
    - 没有代价的连续让步
    - 只重复“拜托/不行”
  extra_checks:
    - 每个人真正不可让的是什么？可以交换的是什么？
    - 每个人认为对方知道自己的底线到什么程度？
```
