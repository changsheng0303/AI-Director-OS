# Universal Dialogue Core — Craft Rules v2.1

STANDARD / DEEP 按需加载。这里放“所有题材共享”的低频工艺规则，不包含具体题材风格。

## 1. Information Economy

### 1.1 角色信息上限

显性台词不得超过角色的知识强度：

`UNKNOWN < SUSPECTED < BELIEVED < KNOWN`

角色可以撒谎，但谎言仍必须建立在其已知与目的之上。

### 1.2 Exposition Filter

如果双方都知道某段背景，优先用：

- 指代；
- 半句话；
- 旧习惯；
- 具体物件；
- 对方反应；
- 改口；
- 回避；
- 动作；
- 冲突中的局部信息。

观众需要知道 ≠ 人物需要完整说出来。


## 1.3 Listener Model / Perceived Knowledge

客观知识边界之外，再追踪会改变策略的**二阶认知**：

```yaml
listener_model:
  self_knows: []
  thinks_other_knows: []
  thinks_other_suspects: []
  thinks_other_believes_false: []
  mistaken_assumptions: []
```

只追踪当前场景有行为价值的事实，避免全量心智模拟。

典型用途：

- 隐瞒：我以为你不知道，所以我敢用某种说法；
- 审问：我故意表现得“已经知道”，测试你会不会补充；
- 谈判：我判断你不知道我的底线，因此不主动暴露；
- 亲密：我以为你早就知道，所以某次承认的风险被误判。

如果人物策略只能在“角色凭空知道对方知道什么”的前提下成立：`LISTENER_MODEL_BREAK`。

## 2. Subtext

潜台词不是“永远说反话”。

内部可拆：

```yaml
surface:
behavior_goal:
subtext:
unconscious_need: optional
```

好的潜台词满足：

`表层表达` 是角色为了 `行为目标` 在当前关系和风险下做出的合理策略。

若删掉“潜台词解释”后，表层句子和真实目的完全没有可追踪关系：`FALSE_SUBTEXT`。

## 3. Tactic Shift

阻力出现后，角色应该至少发生一种变化：

- 改措辞；
- 改问题角度；
- 提高 / 降低压力；
- 转移话题；
- 暂时示弱；
- 改用事实；
- 改用沉默；
- 改用第三人 / 物件；
- 退出当前目标。

连续重复同一诉求但只换近义词：`TACTIC_FLATLINE`。


## 3.1 Turn Coupling / Adjacency

每一轮新台词都要识别上一轮的 `move`，再选择响应模式：

```text
answer / refuse / redirect / challenge / correct / repair / ignore / misread / accept / escalate / deescalate
```

检查法：

> 如果把上一句换成任意别的句子，这一句仍然完全成立吗？

如果连续多轮答案都是“是”，说明角色可能只是在轮流朗读自己的预设立场。

注意：`ignore`、`misread`、`redirect` 也算响应，但必须是**有行为目的的非响应**。

连续多轮互不咬合：`TURN_DECOUPLING`。

## 3.2 Conversational Repair

真实对话允许误解、听错、含义偏移，但必须有修复机制：

- clarify：澄清；
- correct：纠正事实；
- narrow：缩小问题；
- rephrase：换说法；
- abandon：放弃修复，保留误解。

不要让角色在明显误解发生后无原因地继续“精准理解”后续所有信息。

## 4. Rhythm

允许：打断、抢话、不回答、答非所问、反问、停顿、半句话、动作回应、误解、第三人插话。

禁止为了“像口语”机械加入：

- 大量省略号；
- 随机口吃；
- 无意义填充词；
- 每句都带语气词。

节奏变化必须来自人物压力与策略。

## 5. Silence & Action

动作优先于重复性台词。

沉默必须至少承担：拒绝、犹豫、施压、掩饰、权力变化、关系确认、信息回避中的一种。

无功能沉默只是停顿装饰。

## 6. Character Voice

Voice 由六层共同形成：

1. 角色选择说什么；
2. 选择不说什么；
3. 用什么策略；
4. 句式和词汇；
5. 节奏与停顿；
6. 不同关系 / 压力下如何变形。

“每人一个口头禅”不算 Voice Separation。

## 7. Actor Pass

逐角色检查：

- Fidelity：符合稳定人物逻辑吗？
- Knowledge：知道到这个程度吗？
- Motivation：说这句是为了做什么？
- Exposure：愿意暴露这么多吗？
- Voice：换人后还能成立吗？
- Stress：当前压力是否影响表达？

## 8. Director Pass

只看结果：

- scene_change 是否发生；
- tactics 是否变化；
- performance_space 是否存在；
- visual_redundancy 是否过多；
- payoff 是否落到信息 / 关系 / 决策 / 行动之一。


## 8.1 Exit / Tail Discipline

为 DRAMATIC 场景定义最小 `exit_condition`：

```yaml
exit_when:
  - want_achieved
  - want_blocked
  - decision_deferred
  - tactic_abandoned
  - cost_exceeds_value
  - scene_change_completed
```

达到 payoff 后，默认执行一次尾部压缩：

1. 删除主题总结；
2. 删除“所以我们现在明白了……”类复述；
3. 删除双方重复确认已经做出的决定；
4. 保留真正改变余味、关系或下一步行动的最后一拍。

轻微冗尾标记 `TAIL_DRIFT`，通常局部剪掉即可。

## 9. Dialogue Doctor

重点清理 AI 常见模式：

- 所有人都异常会表达；
- 每句话都完整漂亮；
- 角色互相理解过快；
- 开头总是“其实 / 我只是 / 你知道吗”；
- 结尾总是总结主题；
- 情绪被角色自己解释完；
- 金句密度过高；
- 每一轮都机械 A/B/A/B；
- 冲突只靠提高音量，不改变策略；
- 为制造高级感而故意含糊。

## 10. Compression

逐句两问：

1. 删除后剧情是否仍成立？
2. 删除后人物、关系、情绪、节奏是否也不受损？

两者皆是：删除。

## 11. Multi-Character Asymmetry

三人以上不得平均分配台词。

动态功能可包括：

- driver；
- resistor；
- mediator；
- observer；
- disruptor；
- target；
- gatekeeper。

角色可以不说话，但其反应必须影响其他人的策略，才算真正参与。

## 12. Candidate Selection

只用于 DEEP 的关键句，最多 3 候选：

- A：最符合角色；
- B：行为目的最清晰；
- C：潜台词 / 戏剧效果更强。

优先级：

`Character Truth > Scene Function > Speakability > Cleverness`

## 13. Continuity Audit

检查：

- 已知事实是否重复“第一次知道”；
- 怀疑是否无依据突然升级为确认；
- 关系倒退是否有原因；
- 同一秘密是否重复首次揭露；
- 角色是否忘记自己上一场的决定；
- 口吻变化是否来自状态而非模型漂移。

## 14. Claim / Lie / Promise Continuity

连续场景至少追踪会影响后续对话的：

- claims：角色公开声称过什么；
- lies：已建立的谎言版本；
- denials：明确否认过什么；
- promises：答应过什么；
- unanswered_questions：尚未回应的重要问题；
- conversational_debts：角色欠对方的解释、回应或行动。

角色可以改口，但必须有触发：新证据、被抓住矛盾、主动坦白、策略转换、记忆修正等。

无触发自行改变说法：`DECEPTION_CONTINUITY_BREAK`。
