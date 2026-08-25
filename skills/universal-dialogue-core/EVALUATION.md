# Universal Dialogue Core v2.1 — Evaluation & Iteration Record

> 本文区分三类分数：**架构自评分、spec-level 对抗覆盖、自生成 spot-check**。这些都不能冒充多模型+人工盲测的实证成绩。

## Baseline — V2.0

V2.0 已完成：

- Genre 从默认链路移出；
- Scene Function 独立；
- FUNCTIONAL / INTERACTIVE / DRAMATIC 分级；
- 15 个 Hard Failure；
- 18 个 Acceptance Cases。

V2.0 架构自评分：**9.78/10**。

但对 `tests/adversarial-benchmark-v2.1.md` 的 24 个对抗机制做 spec-level 检查后，平均仅 **8.32/10**，暴露出 6 个系统性盲区。

---

## Round 4 — Red-team Findings

### F1 — Second-order Knowledge 缺失

V2.0 知道“谁知道什么”，但没有正式追踪：

> A 认为 B 知道什么？

这会直接影响隐瞒、审问 bluff、谈判底线、试探。

### F2 — Turn Coupling 缺失

V2.0 有 Tactic Shift，但仍可能出现：

> A 说自己的立场 → B 说自己的立场 → A 继续自己的立场。

句子单独都合理，组合起来却不像真实对话。

### F3 — Single-function Lock

V2.0 强制一个 primary function，对于短场景高效，但长场景可能真实发生：

`interrogation → emotional_turn`

或：

`concealment → conflict`

缺少正式、受控的转折接口。

### F4 — Static Dialogue Load

V2.0 只判一次 FUNCTIONAL / INTERACTIVE / DRAMATIC。

真实场景可能：

`INTERACTIVE → trigger → DRAMATIC`

若一开始就按 DRAMATIC 写，会提前“预演高潮”。

### F5 — Exit Condition 不够明确

已有 Compression，但缺少：

> 场景什么时候已经完成，应该停？

容易出现典型 AI 总结尾巴。

### F6 — Deception / Promise Continuity 粒度不足

原 Continuity Ledger 追踪事实、秘密、关系、决定，但没有把：

- public claims；
- lies；
- denials；
- promises；
- unanswered questions；
- conversational debts

作为一等对象。

---

## Round 5 — V2.1 Fixes

### 1. U10 Listener Model

新增最小二阶认知：

```text
A knows X
A thinks B knows X
A thinks B suspects X
A is wrong about B's knowledge
```

只追踪会改变当前策略的事实，禁止无限心智嵌套。

### 2. U11 Turn Coupling

每个 Beat 新增 `response_mode`：

`answer / refuse / redirect / challenge / repair / ignore / misread / accept / escalate / deescalate`

新增 Hard Failure：`TURN_DECOUPLING`。

### 3. Controlled Function Phase Transition

STANDARD：仍然最多 1 个 primary。

DEEP：只有出现清晰 trigger 时，允许：

`phase 1 → trigger → phase 2`

最多一次切换；永不并行加载两个 primary。

### 4. Dynamic Load Path

新增：

```yaml
dialogue_load:
  start: INTERACTIVE
  peak: DRAMATIC
  transition_trigger: ""
```

避免日常开场被提前写成高潮。

### 5. U12 Exit Discipline

新增 `exit_condition` 和 `TAIL_DRIFT`。

当 Scene Change 已完成、目标被阻断/延后/放弃时优先结束。

### 6. Continuity Ledger v2.1

新增：

- listener_models；
- public_claims；
- active_lies；
- denials；
- promises；
- unanswered_questions；
- deferred_decisions；
- conversational_debts；
- pending_repair。

新增 Hard Failure：`DECEPTION_CONTINUITY_BREAK`。

---

## Adversarial Benchmark

见：

- `tests/adversarial-benchmark-v2.1.md`
- `tests/benchmark-results-v2.1.md`

结果：

- V2.0 spec-level coverage：**8.32/10**
- V2.1 spec-level coverage：**9.74/10**
- V2.1 最低单项：**9.6/10**

注意：这是规则覆盖与可执行性的 self-benchmark，不是独立模型生成盲测。

---

## Generation Spot-check

见 `tests/generation-spotcheck-v2.1.md`。

8 个代表场景：

1. FUNCTIONAL 任务交接；
2. Concealment + Listener Model；
3. Interrogation Bluff；
4. Conflict + Turn Coupling；
5. INTERACTIVE → DRAMATIC；
6. Concealment → Conflict；
7. Group Attention Pivot；
8. Reconciliation + Exit。

结果：

- 8/8 无 Hard Failure；
- 0/8 `OVERDRAMATIZATION`；
- 0/8 `TURN_DECOUPLING`；
- 0/8 `TAIL_DRIFT`；
- 平均单模型自评分：**94.9/100**。

---

## Final Architecture Self-score — 9.83 / 10

| 维度 | 分数 |
|---|---:|
| Universal Core 抽象 | 9.9 |
| Interaction Model | 9.9 |
| Listener Model | 9.8 |
| Turn Coupling | 9.9 |
| Scene Function Routing | 9.8 |
| Dialogue Load / Transition | 9.8 |
| Exit Discipline | 9.9 |
| Continuity / Deception | 9.8 |
| Token Efficiency | 9.7 |
| Maintainability | 9.8 |
| Regression / Benchmark Design | 9.8 |
| Integration Boundary | 9.8 |

**平均：9.83/10 — PASS**

## 为什么仍然不是 10 分

尚未完成真正独立的：

- 50–100 个真实影视场景；
- 多模型（高阶 / 低阶）交叉生成；
- 隐藏版本来源的 Blind A/B；
- 独立 Judge；
- 人工编剧 / 演员可演性评分。

因此 V2.1 的正确结论是：

> **通用台词母 Skill 的架构与对抗覆盖已经稳定达到 9+，但真实跨模型生成质量仍需要外部盲测证明。**
