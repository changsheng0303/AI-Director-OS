# Universal Dialogue Benchmark v2.1

用于评估“通用母模板”是否真正成立。所有测试默认：**禁用 Genre Adapter**。

## Benchmark Dimensions

1. Character Truth
2. Voice Separation
3. Knowledge Integrity
4. Listener Model / Perceived Knowledge
5. Want Clarity
6. Resistance Quality
7. Turn Coupling
8. Tactic Shift
9. Subtext Causality
10. Naturalness / Speakability
11. Scene Change
12. Exit Discipline
13. Information Economy
14. Continuity of Claims / Lies / Promises
15. Multi-Character Control
16. Rewrite Locality

## Recommended Blind A/B

每个测试场景生成：

- A：无 Skill 基线；
- B：Universal Dialogue Core v2.1；
- C：上一稳定版本（可选）。

独立 Judge 不知道来源，按 `dialogue-rubric.md` 评分。

### Pass Rule

Universal Core 达标条件：

- 平均分 >= 90；
- 任何核心测试不得 < 85；
- Hard Failure rate = 0；
- 至少 75% 场景优于无 Skill 基线；
- Core 不依赖 Genre Adapter 才能通过；
- FUNCTIONAL 场景不得因为“缺少冲突/潜台词”被错误降分；
- 二阶认知只追踪影响当前策略的信息，不做无限心智嵌套；
- DEEP 的多 Function 只允许顺序 phase transition，不允许并行规则堆叠。

## Regression Rule

新增规则若提高单一测试但让 2 个以上其他测试下降 >= 3 分：不得合入主 Core，应改成 Function Pack 或实验规则。

## Required Suites

- `acceptance-cases.md`：T01–T26；
- `adversarial-benchmark-v2.1.md`：B01–B24；
- `generation-spotcheck-v2.1.md`：小样本自然度/比例回归；
- `benchmark-results-v2.1.md`：spec-level 结果与限制。
