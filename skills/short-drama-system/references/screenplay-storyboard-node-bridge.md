# Screenplay → Storyboard Node Bridge

剧本和分镜是两张可独立重跑的图，不是一个巨型阶段。

```text
source.ingest → story.contract → cast.function → scene.outline
                                             ↓
dialogue.pass → screenplay.assemble → screenplay.review → canon.freeze
                                                        ↓ script_canon
source.lock → beat.extract → space.map/audio.ledger/asset.plan → shot.design
                                                        ↓
performance.pass → clip.group → continuity.check → storyboard.deliver
```

## 端口契约

`canon.freeze` 向 `source.lock` 只传：

- 剧本版本和来源；
- 场次 ID 与顺序；
- 锁定事件和场次退出状态；
- 角色 ID、知识边界和当前关系；
- 精确对白 ID、原文、逻辑重音语义和可选 delivery；
- 禁止修改项；
- 允许分镜推断的范围。

不传全套编剧分析、平台评分、题材教程或未采用的备选方案。

## 局部失效

- 只改台词原文或逻辑重音：重跑 `audio.ledger`、受影响 `shot.design` 和下游；只改音量/语速等 delivery 时无需重做剧情或镜头结构。
- 只改角色表演：重跑 `performance.pass` 和下游，不重写剧本。
- 改场次动作或退出状态：从该场 `beat.extract` 重跑。
- 改人物身份、世界规则或结局：标记相关剧本节点和分镜节点为可能过期，由用户选择重算范围。
- 只换视频引擎：保留镜头表，从 `clip.group` 或引擎编译节点重跑。

任何下游节点都不能借“适配模型”为理由静默改写剧本 Canon。
