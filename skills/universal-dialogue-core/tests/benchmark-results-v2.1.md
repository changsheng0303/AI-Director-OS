# Benchmark Results — v2.0 → v2.1

## Method

这是一次**spec-level adversarial self-benchmark**：逐项检查 Skill 是否具有足够明确、低歧义、可执行的规则来处理 24 个对抗场景。它不是独立模型/人工盲测，因此不能冒充真实生成质量实验。

评分口径：10 分制，关注“规则覆盖 + 路由明确度 + 失败检测 + 定向返工路径”。

| Case | V2.0 | V2.1 | Δ |
|---|---:|---:|---:|
| B01 | 8.0 | 9.8 | +1.8 |
| B02 | 8.1 | 9.7 | +1.6 |
| B03 | 7.8 | 9.7 | +1.9 |
| B04 | 8.2 | 9.7 | +1.5 |
| B05 | 8.3 | 9.8 | +1.5 |
| B06 | 8.2 | 9.7 | +1.5 |
| B07 | 8.0 | 9.6 | +1.6 |
| B08 | 8.5 | 9.8 | +1.3 |
| B09 | 8.1 | 9.7 | +1.6 |
| B10 | 8.2 | 9.8 | +1.6 |
| B11 | 8.3 | 9.7 | +1.4 |
| B12 | 8.4 | 9.7 | +1.3 |
| B13 | 8.4 | 9.8 | +1.4 |
| B14 | 8.6 | 9.6 | +1.0 |
| B15 | 8.2 | 9.9 | +1.7 |
| B16 | 8.5 | 9.8 | +1.3 |
| B17 | 8.1 | 9.8 | +1.7 |
| B18 | 8.4 | 9.8 | +1.4 |
| B19 | 8.5 | 9.7 | +1.2 |
| B20 | 8.2 | 9.8 | +1.6 |
| B21 | 8.6 | 9.7 | +1.1 |
| B22 | 8.7 | 9.7 | +1.0 |
| B23 | 8.5 | 9.6 | +1.1 |
| B24 | 8.8 | 9.8 | +1.0 |

- V2.0 平均：**8.32/10**
- V2.1 平均：**9.74/10**
- 提升：**+1.42**
- V2.1 最低单项：**9.6/10**

## V2.0 主要失分簇

1. **Second-order knowledge 缺失**：知道“客观事实”，但不知道角色对对方知识状态的判断；
2. **Turn coupling 缺失**：能检查 tactic shift，却不能保证一句真正回应上一句；
3. **Single-function lock**：长场景真实机制转折没有正式接口；
4. **Static load**：场景中途从日常升到戏剧状态时缺乏负荷路径；
5. **Exit condition 缺失**：payoff 后容易出现 AI 总结尾巴；
6. **Deception / promise continuity 粒度不足**：continuity 有事实和关系，却未单独追踪公开说法、谎言与对话债务。

## V2.1 修复映射

| 失分簇 | 修复 |
|---|---|
| Second-order knowledge | `U10 Listener Model` + perceived knowledge fields |
| Turn coupling | `U11 Turn Coupling` + `response_mode` + adjacency audit |
| Single-function lock | DEEP `phase 1 → trigger → phase 2`，最多一次切换 |
| Static load | `dialogue_load.start / peak / transition_trigger` |
| Exit drift | `U12 Exit Discipline` + exit_condition + `TAIL_DRIFT` |
| Deception continuity | claims / lies / denials / promises / unanswered questions ledger |

## Verdict

**PASS — spec-level adversarial coverage 9.74/10**

真正下一步的实证测试仍应是：同一批真实场景，多模型生成 + 隐藏来源 + 独立 Judge / 人工演员评分。
