# Universal Dialogue Core Skill v2.1 — Package

## Runtime Core

- `SKILL.md` — 主控、路由、Gate、Rewrite；
- `core-craft-rules.md` — 题材无关台词工艺；
- `universal-dialogue-template.yaml` — 通用母模板；
- `scene-function-router.yaml` — Scene Function 路由与 DEEP phase transition；
- `dialogue-rubric.md` — DEEP 评分器；
- `voiceprint-schema.yaml` — 角色语言指纹；
- `continuity-ledger.yaml` — 连续性、谎言、承诺、开放问题。

## Scene Functions

- `scene-functions/conflict.md`
- `scene-functions/concealment.md`
- `scene-functions/interrogation.md`
- `scene-functions/negotiation.md`
- `scene-functions/intimacy.md`
- `scene-functions/reconciliation.md`
- `scene-functions/exposition-delivery.md`
- `scene-functions/casual-exchange.md`
- `scene-functions/emotional-turn.md`
- `scene-functions/group-dialogue.md` — structural modifier

## Tests

- `tests/acceptance-cases.md` — T01–T26；
- `tests/universal-benchmark.md` — 正式 Benchmark 协议；
- `tests/adversarial-benchmark-v2.1.md` — 24 个对抗机制；
- `tests/benchmark-results-v2.1.md` — spec-level 对抗结果；
- `tests/generation-spotcheck-v2.1.md` — 8 场小样本生成回归。

## Experimental

`experimental/genre-adapters/`：题材层资产，默认不进入 Core 运行链路。

## Default Runtime

```text
Character / Screenwriter upstream
        ↓
Universal Core
        ↓
Dialogue Load Path
        ↓
Information Boundary
        ↓
Listener Model (only relevant facts)
        ↓
Scene Function
        ↓
Turn-coupled Beats
        ↓
Draft
        ↓
Actor + Director Pass
        ↓
Exit / Continuity / Score
        ↓
Final Dialogue
```
