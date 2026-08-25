# Scene Function — Concealment

```yaml
function_output:
  core_problem: 角色必须回应互动，但又不能让关键事实、感情、动机或知识暴露。
  preferred_tactics: [partial_truth, answer_adjacent, redirect, counterquestion, minimization, overnormalization, silence]
  beat_patterns:
    - prompt -> safe_answer -> pressure -> leak_risk -> tactic_shift -> residue
    - ordinary_question -> guarded_answer -> unexpected_detail -> recovery
  information_rules:
    - 明确 hidden_fact / allowed_surface / accidental_leak 三层。
    - 同时明确隐藏者“认为对方已经知道/怀疑到什么程度”，策略必须基于该主观判断。
    - 谎言只能使用撒谎者已知的信息。
  pressure_rules:
    - 越接近暴露点，表达可更短、更具体或更防御，不能无理由无限含糊。
  payoff_conditions:
    - 秘密保住但怀疑上升；或部分泄露；或角色为保密付出关系/行动代价。
  anti_patterns:
    - 为制造悬念拒绝回答本来必答的信息
    - 含糊代词代替真实策略
    - 隐瞒角色突然说出完整内心解释
  extra_checks:
    - 对方究竟察觉了什么，而不是作者希望观众感觉“神秘”？
    - 隐藏者是否错误高估/低估了对方掌握的信息？这个误判是否影响说法？
```
