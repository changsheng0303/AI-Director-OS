# AI Director OS 整体系统与 Skills 说明

> 文档版本：1.1
> 更新日期：2026-08-26  
> 当前状态：当前系统架构与38个项目 Skill 的基准说明  
> 推荐入口：`short-drama-system`

## 项目概览

AI Director OS 是面向 Codex 的 AI 影视、动画、短剧与广告生产系统。它不是一条巨型 Prompt，而是一套按任务动态路由的 Skill 能力库：用户看到简洁的导演流程，内部按需调用剧本、角色、对白、导演分镜、视觉资产和视频模型适配模块。

系统的核心原则是：

- 创作判断交给适合的 LLM Skill；
- ID、引用、时长、状态和格式尽量交给确定性代码；
- 默认使用轻量底座，不因项目较长就自动启动复杂 IR；
- 已确认剧本、对白和资产下游只读，修改必须回到权威层；
- 一个步骤只加载一个主 Skill 和少量支持 Skill，避免上下文污染和重复权威。

## 目标与范围

本文说明：

1. 整体系统的六步流程与内部架构；
2. 简化数据底座和严格工程模式的区别；
3. 剧本生成、审稿与圆桌诊断的真实路由；
4. 当前38个项目 Skill 的用途、边界和所属阶段；
5. 常见请求应当调用哪个 Skill；
6. 当前风险、维护原则和下一步。

本文不包含每个 Skill 的全部方法论原文，也不等于将38个 Skill 在每次任务中全部加载。

## 系统架构

### 用户可见六步流程

```text
1. 项目与剧本
2. 审稿定稿
3. 导演分镜
4. 视觉资产与故事板
5. 视频提示词与生成
6. 成片交付
```

用户只需要选择：全流程、单点制作或继续项目。系统不要求用户理解 S-1、Narrative IR、Shot IR、Hash、State Diff 等内部名词。

### 内部职责链

```text
创意 / 小说 / 已有剧本
        │
        ▼
short-drama-system ──────────────── 单一导演入口
        │
        ├─ IP / 世界与角色基础
        ├─ 剧本创作 / 审稿 / 对白
        ├─ 导演设计 / 生产分镜
        ├─ 角色 / 场景 / 道具 / 系列图片
        ├─ Video Prompt IR
        └─ H3 / Seedance / Fafajing Adapter
```

### Skill 加载策略

- 每个用户可见步骤使用一个主 Skill；
- 最多加载两个真正必要的支持 Skill；
- 同名或相似 Skill 不并行输出两套权威文件；
- `director-mindset`提供创意导演判断，`ai-video-storyboard-compiler`是生产镜号权威；
- `h3-prompt-writing`是 H3 格式权威，本地 H3 Skill 只能作为 Overlay；
- 已批准对白由 `universal-dialogue-core`生成 `DIALOGUE_CANON`，下游逐字只读。

## 简化生产底座

普通项目默认使用 `simple-project.json`，只记录下游真正需要的内容：

| 数据 | 作用 |
|---|---|
| Canon-lite | 锁定事件、固定对白、角色和禁止改动 |
| Story Map | 前提、主角、目标、冲突、情绪变化与场景摘要 |
| Scene Contract | 场景目标、人物、空间、入场/离场状态和资产引用 |
| Runtime State | 当前人物、道具与场景状态 |
| Shot Table | 镜号、时长、主体、动作、起止状态、对白与资产引用 |
| Asset List | 角色、场景、道具、风格和故事板资产 |
| Prompt Jobs | 目标引擎、镜头范围和提示词任务状态 |
| Warnings | 当前无法自动修复的生产风险 |

### 分镜节奏规则

短片、短剧和 AI 视频默认以整段序列平均 **3–4秒/镜**作为节奏参考，但禁止按计时器机械切镜。切镜必须来自至少一个主要变化：

1. 情绪变化；
2. 信息变化；
3. 主体变化；
4. 动作阶段变化；
5. 视线或观看视角变化。

完整台词、连续动作、关键沉默、空间建立和情绪停顿可以超过4秒；插入、反应和冲击镜头可以短于3秒。平均时长偏离只产生诊断提醒，不自动判错。

## 可选严格工程模式

只有用户明确要求“完整工程模式”“严格溯源模式”“审计级交接”时，才启用完整 Foundation Hash、Narrative IR、Shot IR、Artifact Registry、State Diff 和正式变更 ID。

以下情况本身不会自动启动严格模式：

- 项目较长；
- 集数较多；
- 有多个角色；
- 需要多段视频；
- 用户只是希望角色保持一致。

## 剧本生成与质量控制

### 生成阶段必做的自检

`screenplay-master`生成完整剧本时，会运行六门自检：

| 质量门 | 检查内容 |
|---|---|
| 结构 | 开场、主线、转折、结局与目标时长是否匹配 |
| 角色 | 欲望、障碍、伤口、选择、变化和动机是否稳定 |
| 钩子与节奏 | 开场抓力、升级、反转、兑现和结尾余韵 |
| 对白 | 是否口语、可演、有压力、无解释性废话 |
| 格式 | 是否符合短片、短剧、广告、剧集等目标格式 |
| 连续性 | 人名、关系、时间、伏笔、事件与约束是否一致 |

这套六门检查属于常规自检，默认执行，不需要用户额外提出“审稿”。

### 条件启用的专项检查

| 条件 | 调用能力 |
|---|---|
| 对白很多、角色声音风险高、秘密/知识边界复杂 | `universal-dialogue-core` |
| 微短剧第一集、平台爽点、付费卡点或内容负责人审稿 | `screenwriter-review` |
| 现有剧本局部迭代、改人设、补过渡 | `drama-script-iteration` |
| 需要去除AI腔、不改变事实与结构 | `humanizer` |
| 需要多视角冲突、行业评委会诊 | 圆桌诊断参考模块 |

## 圆桌诊断是否会在生成剧本时自动进行

### 结论

**不会。** 普通剧本生成完成后会执行六门自检，但不会自动启动“剧本圆桌诊断评审”。

圆桌诊断不是常规自检，而是一种多视角、用户可见的诊断产品。当前提供两档：默认精简模式召集3个最相关的结构、受众和生产视角；完整模式召集4–6个功能性评委。两档都会引用剧本证据并由主治医生整理分歧，只诊断、不直接改稿，也不替用户作最终裁决。

### 当前真实触发条件

| 用户请求 | 是否启用圆桌 | 实际路由 |
|---|---:|---|
| “帮我写一个剧本” | 否 | `screenplay-master`＋六门自检 |
| “写完后自己检查一下” | 否 | 六门自检，必要时对白专项 |
| “深度审一下这个剧本” | 不一定 | 默认先走普通深度 Review；只有要求多视角时才进圆桌 |
| “深度审稿，多视角看看” | 是 | 默认精简圆桌：结构、受众、生产3视角 |
| “从制片、编剧、导演、平台、观众角度审” | 是 | 用户点名多方，使用完整圆桌 |
| “给我开完整圆桌会诊/召集5位评委” | 是 | 完整4–6视角圆桌 |
| “按圆桌意见迭代修改” | 是，然后回编剧层 | 圆桌归纳 → `screenplay-master`或迭代 Skill 改稿 |
| “每写一场都开圆桌” | 默认不建议 | 只在用户坚持时执行 |

因此，“只有要求剧本深度审稿、迭代修改时启用”这个说法还需要补一个条件：**深度审稿必须需要多视角或圆桌形式**。单一专业深审并不必然启动圆桌。

### 为什么不默认启用

1. **它不是同一种检查。** 六门自检回答“剧本是否成立”；圆桌回答“不同利益方会如何评价”。
2. **产出很重。** 全剧会诊通常包含多位评委长篇陈述和归纳，会显著增加 Token、阅读与决策成本。
3. **意见天然冲突。** 商业制片、类型编剧、核心受众、营销和审查视角可能互相矛盾，过早介入会让初稿失去清晰方向。
4. **容易形成自我否定循环。** 同一个模型一边写、一边模拟多方批评、再立即重写，容易过度优化、抹平个性或反复改动已成立部分。
5. **圆桌只诊断，不开方。** 诊断结果仍需交回编剧或迭代 Skill 执行修改；在每次初稿后自动运行会制造不必要的往返。
6. **应保留用户决策权。** 圆桌主治医生只整理分歧，不应该在用户未要求时替用户引入五套价值标准。

### 推荐使用时机

```text
剧本 V1
  ↓
常规六门自检
  ↓
用户确认方向基本成立
  ↓
需要多视角深审时启动圆桌
  ↓
输出问题清单与意见分歧
  ↓
screenplay-master / drama-script-iteration 改为 V2
  ↓
再次常规审稿并锁定 Canon
```

适合启动圆桌的节点：完整大纲、第一集定稿前、完整短片 V1、第三幕争议、商业可行性争议、主角是否讨喜、平台/受众判断出现分歧。

不适合启动圆桌的节点：一句创意、尚未成形的灵感、每个场景刚写完、纯格式修改、纯对白压缩、纯错字修复。

## Skills 总览

当前仓库包含38个项目 Skill。它们是可选能力库，不会同时加载。

### A. 总控、IP 与全链路

| Skill | 主要用途 | 不负责 |
|---|---|---|
| `short-drama-system` | 六步导演入口、项目路由、简化生产底座 | 不独占所有专业创作 |
| `ai-2d-animation` | AI 2D动画全链路，简化模式与可选完整工程模式 | 不替代各引擎格式权威 |
| `ip-foundation-engine` | 创意种子→世界边界、阵容、关系、禁止假设 | 不写逐集剧情与运行时状态 |
| `ip-worldbuilding` | 九章世界观设定书与可选季级规划 | 不写逐集剧本 |

### B. 剧本、审稿、对白与人物行为

| Skill | 主要用途 | 典型触发 |
|---|---|---|
| `screenplay-master` | 通用影视剧本、短片、广告、剧集、诊断与改写 | 写剧本、做大纲、审稿、改稿 |
| `micro-drama-creation` | 50–100集竖屏微短剧工业流程 | 爽点、钩子、付费卡点、出海 |
| `anime-series-scripting` | 约18分钟一集的番剧剧本 | 番剧、上中下并发排产 |
| `drama-script-iteration` | 已有短剧/番剧的局部迭代 | 改剧情、改人设、补过渡 |
| `screenwriter-review` | 短剧/漫剧第一集和内容负责人审稿 | 选题判断、第一集生死线 |
| `universal-dialogue-core` | 台词生成、重写、知识边界、潜台词和角色声音 | 对白精修、群戏、秘密、谎言承诺 |
| `character-prediction-skill` | 根据已锁定人设预测高风险场景反应 | 行为一致性，不扩写人物百科 |
| `humanizer` | 去除AI腔，增加自然表达 | 不改变事实和结构 |
| `graded-anime-plot-writing` | L2/L3/L4分级动漫剧情与合规自检 | 不负责普通全年龄剧本入口 |

### C. 导演、分镜与表演

| Skill | 主要用途 | 权威边界 |
|---|---|---|
| `director-mindset` | 构图、景别、机位、运镜、声音、表演和剪辑判断 | 导演创意视角，不输出模型格式 |
| `storyboard-script-spec` | 空间锁定、镜头价值、切镜接口、时长与连续性规范 | QA规范，不另建平行镜号 |
| `ai-video-storyboard-compiler` | 剧本→生产 Shot 表、生成段、起止状态与交接 | 生产镜号唯一权威 |
| `micro-expression-video-prompts` | FACS/AU微表情、压制/泄漏层和表演时间线 | 专注表演关键镜头 |
| `design-disney-animation-prompts` | 动画十二原则的图生视频动作与过渡提示 | 不生成完整剧本或直接编辑视频 |

### D. 角色、场景与图片资产

| Skill | 主要用途 | 典型交付 |
|---|---|---|
| `character-design-director` | 人物圣经、视觉锚点、三视图、表情与姿态 | 角色卡与生图提示词 |
| `anime-scene-asset-design` | 2D动漫场景资产化与七维场景卡 | 空间、材质、光线、声音与提示词 |
| `ai-image-assets` | 从剧本盘点角色、场景、氛围与道具 | 按生图工具分类的资产提示词 |
| `series-image-director` | 多张系列图的Visual DNA、一致性与修复 | 系列生产计划和提示词 |
| `cinema-dna-21x9x3` | 电影感单帧、21:9三联镜头与海报 | 构图压力、色彩命题、反CG |
| `one-image-film-ad-director` | 从一张参考图发展完整短片/广告/预告 | 叙事、镜头、声音和提示词 |
| `pop-visual-ad-director` | 10–15秒波普、多巴胺快消广告 | 高饱和快切与转化导向 |

### E. 视频提示词生产与引擎适配

| Skill | 主要用途 | 路由边界 |
|---|---|---|
| `ai-video-prompt-production` | 分镜→中立 Video Prompt IR→目标引擎 | 编排层，不替代引擎格式权威 |
| `h3-prompt-writing` | MiniMax H3官方T2VA/I2VA/FL2VA/L2VA/Ref2VA格式 | H3格式唯一权威 |
| `h3-video-prompt-workflow` | H3单条新建的本地生产 Overlay | 不负责多片段长片 |
| `h3-video-prompt-iteration` | 已有H3提示词局部迭代与重校验 | 不负责初次批量生成 |
| `minimax-h3-video-prompt-pipeline` | 多片段/整集H3连续生产 | 长片、资产、音频和连续性 |
| `ref2va-prompt-optimizer` | 单条Full-reference Ref2VA优化与校验 | 不负责多文件批改 |
| `ref2va-batch-rewrite` | 多个Ref2VA文件批量升级与字数校验 | 不用于单条新建 |
| `tag-h3` | TAG/Danbooru风格H3六段式提示词 | 用户明确要求TAG风格时使用 |
| `seedance25-prompt-workflow` | Seedance 2.5新建、延长、编辑、白模和多宫格 | 只负责Seedance规范 |
| `fafajing-prompt-writer` | Fafajing Basic/Full-reference提示词 | 不处理H3或Seedance |
| `adult-adjacent-video-prompts` | 限制级/擦边视频提示词专项 | 只在明确相关内容时使用 |

### F. 文档与音乐

| Skill | 主要用途 | 交付 |
|---|---|---|
| `project-documentation` | 项目档案与正式项目说明书 | Markdown；用户要求时再生成Word |
| `songwriting-and-ai-music` | 歌词、歌曲改编和AI音乐提示词 | 歌词、结构与Suno等提示词 |

## 常见路由示例

| 用户请求 | 主 Skill | 可能的支持 Skill |
|---|---|---|
| “我只有一个创意，帮我做成短片” | `short-drama-system` | `ip-foundation-engine`、`screenplay-master` |
| “写一个60秒剧情短视频” | `screenplay-master` | `universal-dialogue-core` |
| “做50集红果短剧” | `micro-drama-creation` | `screenwriter-review` |
| “给完整剧本做生产分镜” | `ai-video-storyboard-compiler` | `director-mindset`、`storyboard-script-spec` |
| “只讨论镜头怎么拍” | `director-mindset` | `storyboard-script-spec` |
| “建立角色三视图和表情表” | `character-design-director` | `series-image-director` |
| “从剧本提取所有素材” | `ai-image-assets` | 角色/场景专项 Skill |
| “把整集做成H3提示词” | `minimax-h3-video-prompt-pipeline` | `h3-prompt-writing` |
| “修改一条已有H3提示词” | `h3-video-prompt-iteration` | `h3-prompt-writing` |
| “深度圆桌审稿” | `screenplay-master`的圆桌参考模块 | 改稿时回到编剧或迭代 Skill |

## 当前状态

- 已完成：简洁六步总控；
- 已完成：Canon-lite、Story Map、Runtime State、Shot表、资产和Prompt Jobs；
- 已完成：小说改编可选原文证据、节拍认领与资产锚点；
- 已完成：分镜默认平均3–4秒与切镜动机规则；
- 已完成：新手“只选任务、不选Skill”快速入口；
- 已完成：38个Skill自动索引与许可证清单；
- 已完成：圆桌精简3视角模式；
- 已完成：《沙浪之上》圆桌介入A/B首轮基线；
- 已完成：生产失败注册、证据等级与回归校验基础设施；
- 已完成：H3、Seedance、Fafajing分离路由；
- 已完成：38个项目 Skill 已上传公开GitHub仓库；
- 进行中：真实生成结果的持续 A/B 与失败回写；
- 未自动启用：圆桌会诊、完整工程IR、外部付费生成和发布。

## 关键决策

1. **圆桌诊断不作为普通生成自检。** 普通剧本使用六门检查；圆桌只在明确需要多视角时启用。
2. **深度审稿不等于圆桌。** 单一专业深审可由普通Review或短剧审稿完成。
3. **分镜平均3–4秒是序列目标。** 禁止按计时器机械切镜。
4. **生产镜号只有一个权威。** 导演Skill提供创意，分镜编译器负责生产表。
5. **格式权威与本地增强分离。** 官方H3 Skill管格式，本地Skill管生产Overlay。
6. **默认轻量。** 项目规模不自动触发重型工程模式。

## 交付物

| 交付物 | 状态 | 路径 |
|---|---|---|
| 系统仓库 | 已完成 | `changsheng0303/AI-Director-OS` |
| 本系统说明 | 已完成 | `docs/AI-Director-OS-系统与Skills说明.md` |
| 新手快速入口 | 已完成 | `docs/新手快速入口.md` |
| Skill与许可证索引 | 已完成 | `docs/SKILL_INDEX.md` |
| 生产失败注册 | 已完成 | `quality/failure-registry.jsonl` |
| 圆桌真实项目基线 | 已完成 | `docs/experiments/roundtable-lite-salang-summary.md` |
| 总入口 | 已完成 | `skills/short-drama-system/` |
| 轻量Schema与校验器 | 已完成 | `skills/short-drama-system/schemas/`、`scripts/` |

## 风险与问题

| 风险 | 影响 | 建议 |
|---|---|---|
| 38个Skill全部启用 | 自动触发竞争、上下文浪费 | 按项目只启用真正需要的入口与专项 |
| 圆桌过早启用 | 意见冲突、Token成本高、初稿个性被抹平 | 方向成立后按里程碑启用 |
| 多个审稿Skill职责相近 | 可能产生两份不同审稿结论 | 先按题材选择单一审稿权威 |
| 外部平台规则变化 | Seedance/H3/Fafajing规范可能过期 | 保留官方格式权威并做版本审计 |
| 混合许可证 | 公开可见不等于统一授权 | 遵守根LICENSE/NOTICE与各Skill声明 |
| 无真实生成QA | 提示词格式通过不等于视频效果通过 | 使用同资产、同模型、同参数做A/B |

## 下一步

1. 在至少5个不同题材项目上继续记录精简圆桌的返工率和质量影响；
2. 为《沙浪之上》V2候选执行真实片段生成A/B，补充看片证据；
3. 将新的真实生成失败追加到 `quality/failure-registry.jsonl`；
4. 失败跨项目重复达到阈值后，才提升为共享校验规则；
5. 发布前由GitHub Action检查Skill索引、简化底座和失败注册表。

## 版本记录

| 版本 | 日期 | 变更 |
|---|---|---|
| 1.1 | 2026-08-26 | 增加新手入口、自动Skill索引、精简圆桌、真实项目A/B基线和失败回写基础设施 |
| 1.0 | 2026-08-26 | 建立整体系统、38个Skills、剧本质量门与圆桌诊断路由说明 |

## 来源

- `skills/short-drama-system/SKILL.md`
- `skills/screenplay-master/SKILL.md`
- `skills/screenplay-master/references/roundtable-script-doctor.md`
- 当前38个项目 Skill 的 `SKILL.md`
- 根目录 `README.md`、`LICENSE.md`、`NOTICE.md`
