# Project State Machine V1.2

## States
`INTAKE → INTENT_LOCKED → BIBLE_LOCKED → BEAT_LOCKED → SHOT_LOCKED → ASSET_LOCKED → PROMPT_READY → ROUTE_READY → GENERATING → QA_REPAIR → APPROVED → EDITING → FINAL`

## Entry / Exit
| State | Entry | Exit condition |
|---|---|---|
| INTAKE | 用户输入 | 需求结构化 |
| INTENT_LOCKED | Brief | Hook/目标/格式/情绪明确 |
| BIBLE_LOCKED | Intent | 角色/场景/视觉语言锁定 |
| BEAT_LOCKED | Bible | Beat 与信息曲线通过 |
| SHOT_LOCKED | Beat | Shot Contract 完整并通过 QA |
| ASSET_LOCKED | Shot | 关键资产有版本 |
| PROMPT_READY | Assets + Contract | Prompt 编译完成 |
| ROUTE_READY | Prompt | Primary/Fallback/Budget 确定 |
| GENERATING | Route | 生成资产存在 |
| QA_REPAIR | Output | QA PASS 或进入批准 |
| APPROVED | QA | 人审通过 |
| EDITING | Approved shots | 声画整合 |
| FINAL | Edit | Final QA + 版本冻结 |

## Transition Rules
- 不允许跳过 `SHOT_LOCKED` 直接批量生成。
- `FINAL` 不覆盖旧版本。
- 失败时沿最短依赖路径回退。
- 状态变更必须记录 actor、version、evidence。

## Rollback
`QA_REPAIR` → `PROMPT_READY`：Prompt/Contract 问题。
`QA_REPAIR` → `ASSET_LOCKED`：资产问题。
`QA_REPAIR` → `SHOT_LOCKED`：镜头设计问题。
故事级问题才回退到 Beat/Bible。
