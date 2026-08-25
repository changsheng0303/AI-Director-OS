# Universal Dialogue Core — Evaluation Rubric v2.1

用于 DEEP 模式与 Skill 回归评测。**只评通用台词能力，不评题材风格。** 完整权重主要用于 `DRAMATIC`；`FUNCTIONAL` 使用 Light Gate，不因缺少冲突、潜台词或复杂策略而扣分。

## 1. Weighted Score

| 指标 | 权重 | 9+ 标准 |
|---|---:|---|
| Character Truth | 12 | 行为、表达、边界符合稳定人物与当前状态 |
| Knowledge Integrity | 9 | 知道/怀疑/误信/隐瞒严格区分，无越权 |
| Listener Model | 6 | 策略符合“我认为对方知道/怀疑什么”，二阶认知不凭空 |
| Motivation / Want | 9 | 关键台词有具体行为目的 |
| Resistance | 7 | 对话存在真实阻力，阻力影响策略 |
| Tactic Dynamics | 7 | 遭遇回应后策略会调整，不机械重复 |
| Character Voice | 9 | 去名后仍可凭信息选择、策略、句式和节奏区分 |
| Turn Coupling | 8 | 每轮真实响应上一轮 move，非预写独白轮播 |
| Subtext / Exposure Control | 8 | 表层表达与真实目的有因果距离，暴露程度符合风险 |
| Naturalness / Speakability | 8 | 口语可演，不过度完整、文学化或模型化 |
| Scene Progression / Exit | 8 | 状态有效变化，并在 payoff 后及时收束 |
| Information Economy | 4 | 信息最小充分，无说明书对白 |
| Continuity | 3 | 事实、谎言、承诺、关系和说法连续 |
| Rhythm / Performance Space | 2 | 长短、停顿、打断和动作给表演留空间 |

总分：100。

## 2. Pass Threshold

- 95–100：9.7–10.0，极强；
- 93–94：9.5–9.6，关键场景终稿级；
- 90–92：9.0–9.4，通过；
- 85–89：8.5–8.9，定向轻修后重评；
- 80–84：8.0–8.4，明显问题；
- 75–79：7.5–7.9，重写问题段；
- <75：回到 Scene Change / Wants / Beats。

## 3. Hard Failure Gate

任一出现即 FAIL：

`KNOWLEDGE_LEAK / PERSONALITY_BREAK / MOTIVE_VOID / RESISTANCE_VOID / EXPOSITION_DUMP / VOICE_COLLAPSE / SCENE_STAGNATION / EMOTION_OVEREXPLAIN / VISUAL_REDUNDANCY / CONTINUITY_BREAK / UNPLAYABLE_PROSE / TACTIC_FLATLINE / FALSE_SUBTEXT / AUTHOR_SPEAK / OVERDRAMATIZATION / LISTENER_MODEL_BREAK / TURN_DECOUPLING / DECEPTION_CONTINUITY_BREAK`

### Soft Failure

`TAIL_DRIFT`：payoff 已完成仍继续解释/总结/重复确认。默认扣 `Scene Progression / Exit` 与 `Information Economy`，局部压缩即可。

## 4. Light Gate — FUNCTIONAL / 低负荷 INTERACTIVE

不使用完整戏剧权重，只检查：

1. Character Truth；
2. Knowledge Integrity；
3. 必要时 Listener Model；
4. Task Clarity；
5. Turn Coupling；
6. Naturalness；
7. Information Economy；
8. No Overdramatization。

简单对白“直接”不是缺点。

## 5. Score Discipline

禁止：

- 因为“整体读起来不错”而全部 9+；
- 先给总分再倒推子项；
- 用文采抵消 Character / Knowledge / Listener / Motivation 问题；
- 用题材爽感抵消 Core 缺陷；
- 因为句子漂亮而忽略角色其实没有回应上一句。

评分顺序：

1. Hard Failure；
2. Character Truth；
3. Knowledge；
4. Listener Model；
5. Motivation；
6. Resistance；
7. Turn Coupling；
8. Tactic Dynamics；
9. Scene Progression / Exit；
10. Voice；
11. Subtext；
12. Naturalness；
13. Economy / Continuity / Rhythm。

## 6. Rewrite Target

最低层优先修：

```text
knowledge        -> Information Boundary
listener_model   -> Perceived Knowledge / Belief About Other
character        -> State / Voice
motivation       -> Wants
resistance       -> Resistance
turn_coupling    -> Response Mode / Adjacency
strategy         -> Beat Tactic
progression      -> Scene Change / Beats
exit             -> Payoff / Tail Compression
voice            -> Information Choice + Syntax + Rhythm
subtext          -> Exposure Strategy
naturalness      -> Compression / Speakability
continuity       -> Claims / Lies / Promise / Ledger
```

## 7. Evaluation Output

```yaml
score_total: 93
score_10: 9.5
hard_failure: none
soft_failure: none
scores:
  character_truth: 11/12
  knowledge_integrity: 9/9
  listener_model: 6/6
  motivation: 8/9
  resistance: 6/7
  tactic_dynamics: 7/7
  character_voice: 8/9
  turn_coupling: 8/8
  subtext_exposure: 7/8
  naturalness_speakability: 7/8
  scene_progression_exit: 8/8
  information_economy: 4/4
  continuity: 3/3
  rhythm_performance: 1/2
weakest_layers: []
rewrite_targets: []
verdict: PASS
```
