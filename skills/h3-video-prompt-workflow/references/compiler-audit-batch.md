# 批量段编译器审计（ai-2d-animation V1.7 × H3 六段式）

> 用途：一次校验整部/整集 20+ 段 H3 提示词是否符合 ai-2d-animation V1.7 编译器规范。
> 单段格式校验用 ref2va 校验器（--duration），本审计补"编译器层"批量检查。
> 2026-08 在《爆衣味觉学园》EP01 上部 24 段上实测通过（24/24 无真问题，仅正则误报需人工复核）。

## 审计脚本（python，execute_code 跑）

```python
import re
from pathlib import Path

base = Path(r"{当前工作区}\<项目>\提示词")
files = sorted(base.glob("EP01_上部_段*.txt"))

issues = {"no_anime_marker": [], "forbidden_word": [], "cliche_ending": [], "no_action_order": []}
for f in files:
    t = f.read_text(encoding="utf-8")
    name = f.name
    if not re.search(r"anime style|cel shading|2D animation|TV anime", t, re.I):
        issues["no_anime_marker"].append(name)
    for w in ["8k", "masterpiece", "cinematic", "ultra-detailed", "hyper-realistic", "4k"]:
        if re.search(rf"\b{w}\b", t, re.I):
            issues["forbidden_word"].append(f"{name}:{w}")
    for pat in [r"fade to black", r"lights dim", r"pull back to wide", r"empty street"]:
        if re.search(pat, t, re.I):
            issues["cliche_ending"].append(f"{name}:{pat}")
    if not re.search(r"\b(trigger|action|reaction|settle)\b|act of|moves|reaches|lifts|pushes|slides", t, re.I):
        issues["no_action_order"].append(name)

for k, v in issues.items():
    print(f"{k}: {len(v)} 项"); [print(f"   - {i}") for i in v]
```

## 检查项与已知误报

| 检查项 | 判定 | 误报情况（需人工复核） |
|---|---|---|
| 风格标记 | 必含 anime style / cel shading / 2D animation / TV anime | 无 |
| 违禁形容词 | 无 8k / masterpiece / cinematic / ultra-detailed | 无 |
| 模板化结尾 | 无 fade to black / lights dim / empty street 等 | **`without a fade to black` 是反模板化声明，会命中正则**——人工确认语境 |
| 动作顺序 | 含 trigger/action/reaction/settle 或具体动词 | **正则过严**：`holds on...as the shot ends` 收束段（纯反应/定格段）也会漏检——抽查 2-3 段确认即可，不必全改 |

## 配套编译器文档结构（存 `提示词\EP01_上部_编译器文档.md`）

1. **Prompt Trace 总表**：段号 | scene/beat | ending_function | 单主动作 | 邻接类型（SCENE_BREAK/CONTINUE/REACT/REVEAL/TIME_JUMP/CONSEQUENCE）
2. **Shot Adjacency 五锁抽查**：6 处关键邻接 × 五锁保持（人物身份/空间锚点/道具状态/光向/屏幕方向）+ bridge_reason
3. **Ending Function 分布**：11 种（ACTION_COMPLETE/COMEDY_BUTTON/DIALOGUE_BUTTON/RELATIONSHIP_LANDING/REVEAL_LANDING/CHOICE_LANDING/REACTION_LANDING/MOTION_CONTINUE/SUSPENSE_HOLD/TRANSITION_BRIDGE/CONSEQUENCE）——每段恰一个，无 FADE_TO_BLACK/LIGHTS_DIM 默认
4. **Compiler 公式核对**：Context Lock → Subject State → 单主动作 → Secondary Motion → Camera Response → Environment Motion → Audio Cue → Exit State
5. **V1.7 Gate 3 自检**：空间锚点对齐 / 180° 轴线 / Start-End 邻接闭环 / 无 UNMOTIVATED_CUT
6. **投喂批次建议**：参考图绑定分组（试水无图段 → 主角图一段 → 文字角色段 → 全链段）

## 分层分工（重要）

- **ai-2d-animation V1.7** = 导演/编译器层：Story→Scene→Beat→Adjacency 校验、Ending Function、镜头因果
- **tag-h3 六段式** = 模型适配层：subject_definitions / summary / retention_analysis / detailed_description / soundscape / music

两层互补：24 个 txt = 可投喂体，1 份编译器文档 = 可追溯设计依据。改剧本后两层都要重跑。
