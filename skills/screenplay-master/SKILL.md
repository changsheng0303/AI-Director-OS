---
name: screenplay-master
description: "创建、改写、续写、诊断或整理影视剧本。用户说写剧本、改剧本、小说改编、分场、场次、短剧、微短剧、番剧、剧情广告、台词场景、第一集、钩子、反转或剧本不好用时使用；不用于普通散文或纯营销文案。"
---

# Screenplay Writer

这是系统统一的剧本入口。用户描述要写什么即可，不要求记住 `/start`、`/plan`、内部阶段名或其他编剧 Skill。

## 六种模式

- **构思**：一句话、人物或主题 → 故事方向、结局承诺或简短大纲。
- **分场**：已确认故事 → 因果清楚的场次表，不提前塞满对白。
- **写剧本**：大纲、分场或明确需求 → 可拍的完整场景/单集/短片剧本。
- **改编**：小说、故事、章节或现有 IP → 保留来源关系的剧本化改编。
- **改稿**：保留用户指定内容，只修改授权范围，并给出新版本。
- **审稿**：先诊断问题；用户要求“直接改”时在同一轮给出修改稿，不把用户转给另一个 Skill。

微短剧、18 分钟番剧、广告、艺术短片和长剧是参数与参考方法，不是必须由用户选择的不同入口。

## 输入策略

先读用户已经给出的素材。只有缺失项会改变题材、核心关系、结局、时长或不可修改 Canon 时，才问一个合并问题；其余采用最小假设并明确写出。

用户说“你定”“直接写”“先给我一版”时立即产出暂定稿，不设置形式化审批门。用户只要一个场景，就不生成整套项目档案；用户要完整项目时再保存结构化状态。

## 节点流程

按 [screenplay-node-graph.md](references/screenplay-node-graph.md) 选择最小子图：

1. `source.ingest`：读取创意、原著或旧稿，标记来源与不可修改项。
2. `story.contract`：定义故事问题、主角目标、阻力、代价和结局承诺。
3. `cast.function`：只建立当前故事需要的角色功能、关系和声音。
4. `scene.outline`：按因果和价值变化组织场次。
5. `dialogue.pass`：需要对白时调用 `universal-dialogue-core` 的相应深度。
6. `screenplay.assemble`：把动作、表演、对白和声音整理为可拍剧本。
7. `screenplay.review`：只修证据明确的问题。
8. `canon.freeze`：用户确认后才锁定版本并交给分镜。

一个节点失败只重跑它和受影响下游，不整份推倒重来。

## 写作核心

执行前读取 [screenplay-core.md](references/screenplay-core.md)。按任务需要再选择已有专业参考，不全量加载。

不变量：

- 先确定结局承诺和主角选择，再扩写中段。
- 每场有目标、阻力、策略/行动、转折和退出状态；建置场至少提供新信息或关系变化。
- 相邻场次必须能回答“为什么这一场现在发生”。
- 角色行为来自欲望、恐惧、信念、关系或已知信息，不为反转突然降智。
- 世界规则通过行为、物件、代价和后果出现，不靠说明性对白。
- 对白执行试探、拒绝、隐瞒、逼问、说服、安慰、挑衅、谈判或终止等行为；画面已表达的信息不再解释。
- 写可见动作，不把摄影机景别写进文学剧本。分镜由下游负责。
- 不靠新增无关事件、重复对白或固定字数注水。

## 路由专业方法

- 电影概念模式：读 [film-concept-routing.md](references/film-concept-routing.md)。
- 分场或已批准资料装配：读 [scene-treatment-and-fusion.md](references/scene-treatment-and-fusion.md)。
- 小说/章节改编：读 [screenplay-writing-v1.md](references/screenplay-writing-v1.md) 中的来源保真、场景化和批处理部分；不继承其旧命令仪式。
- 50–100 集微短剧：使用 `micro-drama-creation` 的题材、钩子、付费与节奏参考，但本 Skill 仍是用户入口。
- 明确 18 分钟番剧：使用 `anime-series-scripting` 的长格式参考，不强制 12 场平均 90 秒。
- 对白高风险：交给 `universal-dialogue-core`，返回 `DIALOGUE_CANON`。
- 用户明确要红果/平台内容负责人视角：使用 `screenwriter-review` 作为审稿镜头，不把其市场偏好设为所有剧本的通用规则。
- 用户明确要求“原文只加不改”：才使用 `drama-script-iteration` 的严格增量模式。

## 按需参考目录

以下旧方法保留为可选节点资料，不在普通请求中全量加载：

- 任务边界与输出选择：[routing-and-output-modes.md](references/routing-and-output-modes.md)
- 1–3 分钟剧情宣传：[format-1-3min-promo.md](references/format-1-3min-promo.md)、[commercial-script-rules.md](references/commercial-script-rules.md)
- 4–6 分钟短片：[format-4-6min-short-film.md](references/format-4-6min-short-film.md)
- 微短剧与长系列：[format-micro-series.md](references/format-micro-series.md)、[format-long-series.md](references/format-long-series.md)
- 角色、结构与连续性：[character-arc-system.md](references/character-arc-system.md)、[tree-structure-method.md](references/tree-structure-method.md)、[continuity-system.md](references/continuity-system.md)
- 台词、钩子和题材：[dialogue-and-scene-style.md](references/dialogue-and-scene-style.md)、[hook-library.md](references/hook-library.md)、[genre-playbooks.md](references/genre-playbooks.md)
- 平台与风险：[platform-playbooks.md](references/platform-playbooks.md)、[compliance-and-platform-risk.md](references/compliance-and-platform-risk.md)
- 深度项目与审核：[complex-project-intake.md](references/complex-project-intake.md)、[review-checklists.md](references/review-checklists.md)
- 维护蓝图：[screenplay-master-full-blueprint.md](references/screenplay-master-full-blueprint.md)

## 默认交付

用户未指定时，交付当前最有用的一层：

- 构思：一句话故事、核心冲突、结局承诺、关键风险。
- 分场：场号、地点/时间、目标、可见行动、转折、退出状态。
- 剧本：场景头、可见动作、角色名、必要表演提示、对白、关键声音。
- 改稿：修改后完整文本 + 简短改动说明。
- 审稿：P0/P1/P2 问题 + 可执行修改；用户要求时附修改稿。

不要默认输出长篇自检、评分仪式、三套方向、全量人物百科或内部节点日志。

## 生产交接

用户确认后生成稳定版本：锁定场次顺序、事件结果、角色、精确对白和禁止修改项。下游 `ai-video-storyboard-compiler` 只读这些内容。未确认稿标记为 `provisional`，不得伪装成 Canon。

结构化项目可使用 `schemas/screenplay-graph.schema.json` 并运行：

```powershell
python "scripts/validate_screenplay_graph.py" "<screenplay-graph.json>"
```
