# Scene Function — Exposition Delivery

```yaml
function_output:
  core_problem: 观众需要获得信息，但角色不能因此变成解说器。
  preferred_tactics: [need_to_know, task_brief, correction, warning, demonstration, disagreement, question_driven_reveal]
  beat_patterns:
    - immediate_need -> minimum_fact -> reaction/question -> necessary_detail -> action
    - wrong_assumption -> correction -> consequence -> decision
  information_rules:
    - 只交代当前行动所需的最小信息。
    - 已知信息不复述；未知信息通过需求、冲突或错误认知释放。
    - 若角色误判对方已知程度，允许出现“说少了/说多了→被纠正”的自然 repair。
  pressure_rules:
    - 信息每增加一层，都要对应一个新的决策、风险或问题。
  payoff_conditions:
    - 信息改变理解、计划、风险判断或下一步行动。
  anti_patterns:
    - 双方都知道却完整复述历史
    - 一口气解释规则、背景、人物关系和主题
    - 信息说完但没有任何人因此改变行为
  extra_checks:
    - 如果删掉这句信息，观众是否真的会无法理解当前行动？
```
