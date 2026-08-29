# Storyboard Node Graph

分镜采用可组合节点，而不是一次性巨型提示词。每个节点只拥有一种判断，输入输出可以被替换、跳过或重跑。

| Node type | 输入端口 | 输出端口 | 何时运行 |
|---|---|---|---|
| `source.lock` | `source_text`, `canon` | `locked_scene` | 所有正式任务 |
| `beat.extract` | `locked_scene` | `beats` | 所有分镜任务 |
| `space.map` | `locked_scene`, `assets` | `space_map` | 多人、复杂运动或空间风险 |
| `audio.ledger` | `locked_scene` | `audio_units` | 有对白、旁白、OS |
| `asset.plan` | `locked_scene`, `assets` | `fixed_assets`, `pending_assets` | AI 生成或跨片段一致性 |
| `shot.design` | `beats`, `space_map?`, `audio_units?` | `shots` | 所有分镜任务 |
| `performance.pass` | `shots`, `character_state` | `shots` | 表演关键镜头 |
| `clip.group` | `shots`, `engine_profile` | `clip_groups` | 需要 AI 生成片段 |
| `continuity.check` | `shots`, `clip_groups?` | `issues`, `validated_graph` | 生产交付前 |
| `storyboard.deliver` | `validated_graph` | `human_storyboard` | 最终交付 |

节点只读取声明的输入端口。一个节点失败，只重跑该节点和依赖它的下游。`shot.design` 是镜号和时长唯一权威；`clip.group` 不能改镜头内容；`performance.pass` 不能改原台词或剧情结果。用户只看最终分镜，节点图仅在维护或工程模式展示。

```text
source.lock → beat.extract → shot.design → continuity.check → storyboard.deliver
```

```text
source.lock ─┬→ beat.extract ─────────────┐
             ├→ space.map ───────────────┤
             ├→ audio.ledger ────────────┤→ shot.design → performance.pass
             └→ asset.plan ──────────────┘                 ↓
                                              clip.group → continuity.check → storyboard.deliver
```
