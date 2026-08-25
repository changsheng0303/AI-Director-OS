---
name: ai-video-prompt-production
description: "将已确认剧本或分镜编译为中立 Video Prompt IR，并路由到 H3、Seedance 或 Fafajing Adapter。用于跨片段生产编排；不替代引擎格式权威、单条迭代或批量改写。"
license: MIT
metadata:
  hermes:
    tags: [video-prompt, h3, ref2va, minimax, storyboard, short-drama, nsfw-levels]
    related_skills: [tag-h3, ref2va-prompt-optimizer, h3-video-prompt-workflow, seedance25-prompt-workflow, fafajing-prompt-writer, ai-2d-animation]
---

# AI 视频提示词生产工作流（剧本/分镜 → 校验通过 → 交付）

类级工作流：先把剧本、分镜或创意编译为中立 Video Prompt IR，再交给用户指定的引擎 Adapter。现有后续章节记录 H3/Ref2VA 的生产经验，只在目标引擎为 H3 时适用。

## When to use

- 用户给出已确认剧本、分镜或多个片段，要求组织为可追溯的视频提示词生产链。
- 任务需要先判断 T2VA、I2VA、FL2VA、L2VA、全参考、视频编辑或视频续写，再选择引擎格式。
- 任务同时包含图片、视频、音频、对白或关键帧，需要统一素材角色和交接状态。
- 单条 H3 新建、已有提示词局部修改或存量文件批改，直接使用对应垂直 Skill，不加载本编排层。

## Input Mode 与 Video Prompt IR

在加载任何引擎格式前，读取 [references/video-prompt-ir.md](references/video-prompt-ir.md)，完成模式判断、素材角色、关键帧路径、对白/说话人和声音层映射。只有目标引擎确定后才加载对应 Adapter；不得同时加载多个引擎格式规范。

```text
Story / Shot IR / Assets
  → Input Mode
  → Video Prompt IR
  → Engine Adapter
  → Engine Validator
```

用户明确指定引擎时直接路由；未指定且最终格式会明显不同，先说明判断并询问。Video Prompt IR 是中立交接，不继承任何 Adapter 的正文语言、字段、长度或固定模板。

## H3 格式权威（仅目标引擎为 H3 时加载）

用户安装的第三方 skill 是格式/法典权威，先加载再动手：

- `tag-h3` — H3 六段式创作法典（构图/情绪梯度/NSFW 技法/避免常见错误表）
- `ref2va-prompt-optimizer/references/ref2va-spec.md` — 规范（必读）
- 校验脚本：`{Codex技能目录}/ref2va-prompt-optimizer/scripts/validate_ref2va_prompt.py`
- `ai-2d-animation` — Shot Contract 导演体系（anime_treatment / 分级 §13 / 动漫语法），**v1.7-research-optimized（2026-08 最新，正式位置在 `{Codex技能目录}\creative\ai-2d-animation\ai-2d-animation-v1.7-research-optimized\` 嵌套子目录，113 文件）**：NSFW **五级**分级（0-4，Level 4 = 露骨，v1.7 定稿：只管内容边界不管通用镜头语言、L4 无三不铁律、用户优先）+ Story Engine V1.7（Story Contract 22 字段 + Beat Chain + Scene Contract + Shot Adjacency 30/70 + State Ledger/Promise Registry/Audience Delta + spatial-continuity）、Narrative Video Compiler（13 段 TRACE + MiniMax Adapter：单主动作/6-10s 拆段/Start-End Frame）、Ending Architecture（12 种 ending_function + Anti-Cliche）、story-craft（故事不跳规则）、shots-library、3 套风格预设、tease-actions-library 动作库、**6 个校验脚本**（validate_storyboard.py + validate_story_contract.py + validate_shot_adjacency.py + validate_video_prompt_trace.py + validate_story_architecture.py + validate_ending_contract.py）
  - ⚠️ **路径坑**：v1.7 打包后内容在 `ai-2d-animation-v1.7-research-optimized/` 子目录，旧 v1.5-final/v1.4-final 子目录与顶层旧路径均已不存在；引用校验脚本/SKILL.md 必须带 v1.7-research-optimized 子目录前缀

## H3 Adapter 生产流程

0. **读取 IR**：确认 `input_mode`、`target_engine=h3`、素材角色、关键帧关系、对白和声音层已锁定。
1. **读素材**：docx 用 read_file 自动提取全文；先通读再选段。
2. **选高光段**：优先戏剧张力最强的冲突/杀必死/反转瞬间；用户说"几段"默认给 3 段（不同场景各一），每段配 Shot Contract 概览表（镜号/时间/内容/Anime Treatment/分级处理）。
3. **定分级（NSFW Level 0-4 五级）**：用户指定 Level 时按五级表核对：
   - Level 0-1：直接执行（全年龄/健康性感）
   - Level 2：遮挡强制主力档（极大露出+遮挡：花瓣/光晕/构图裁切/雾气）
   - Level 3：性张力+亲密+遮挡，可直接执行（衣物脱落边缘、性暗示、亲吻/接触）
   - Level 4（露骨：生殖器官/性行为/全裸）：**用户优先**，但 H3 平台不支持 → 降级 Level 3 满格表达（性张力拉满+遮挡兜底），并告知用户原因
   - **执行上限**：不生成生殖器官/露骨性行为/性行为过程的提示词描述（用户已知悉并接受）；学生角色场景按当轮指令
   - 部位特写递进结构（成人向）：手→肩→腰→颈→腿→唇，越接近隐私部位遮挡越密（发丝/灯晕/身体/剪影/黑场），最后剪影/黑场收尾
   - **L1 vs L2 靠镜头意图区分**（用户问过"是否过于接近"）：L1 = 功能性记录（她在游泳所以拍到泳装，镜头不得为展示身体停留）；L2 = 凝视性镜头（镜头为拍泳装而让她游泳，主动聚焦曲线/逆光轮廓/服装焦点）。同一画面，镜头意图不同 = 等级不同
   - **L3 暴露高于 L2**（用户确认）：L2 = 穿着状态极大露出（服装始终穿着）；L3 = 脱衣裸露 + 隔衣模拟（暴露高于 L2，乳头/臀部必遮，止步于完全性行为之前）；L3 镜头用性暗示强化（ECU 边缘特写/慢镜律动/窥视构图/主观镜头），写法见 `references/level-camera-language.md`
4. **写六段式**：`subject_definitions` / `summary` / `retention_analysis` / `detailed_description` / `overall_soundscape` / `non_diegetic_music`，全英文（`<d>` 台词原文除外）。
   - 纯文生无参考资产：summary 前缀用 `[reference generation]`，subject_definitions 纯文字定义外观，不建 `<Picture N>`
   - 角色一致性靠 `<Subject N>` 锁定；辨识特征全保留
5. **存文件 + 校验**：写入工作目录 txt，然后跑：
   ```bash
   python "{Codex技能目录}/ref2va-prompt-optimizer/scripts/validate_ref2va_prompt.py" "<file>.txt" --duration <秒>
   ```
   **PASS（0 errors）才算完成**；ERROR 修掉再交付。
6. **交付**：中文说明 + Shot Contract 概览表 + 完整可粘贴六段式（不加 Markdown 围栏说明）+ 文件 MEDIA 链接 + 分级处理说明（尤其降级时要解释原因）。
7. **迭代**：只改用户点名段落；角色外观改动需 subject_definitions + retention_analysis + detailed_description 三处同步；全量覆盖同一文件，每轮重跑校验。
8. **故事层检查（用户反馈"故事很跳"后的强制环节，2026-08）**：多镜提示词交付前过一遍 story-craft 四问，避免"镜头漂亮但剧情跳"：
   - **关系前史**：开场 3 镜内必须有一个关系线索镜头（道具/称呼/无意识动作/微表情，四选一）——观众不知道角色关系，后文亲密/冲突必被误读（旧情人=指尖抚旧痕/喊名字音节；恋人=共同物品/称呼；暗恋=排练对话）
   - **情绪阶梯禁跳级**：觉察→犹豫→软化→默许→情动，每个跳级点必须有过渡节拍（一个镜头或一个表演拍）；**身体接触必须晚于默许信号**（对视/放松/不再推拒），禁止"角色还没同意手已摸上去"
   - **因果链**：每个 Beat 能回答"为什么现在发生/为什么这么做/为什么这种方式/然后呢"——行为只能由"剧情需要"解释 = 断链
   - **信息释放**：观众知道 ≥ 至少一个角色知道（信息差=张力）；每个 WITHHOLD 必须有对应 REVEAL 不悬空；15s 内信息点 ≤3、情绪级 ≤3
   - 交付说明里若剧情有信息差/阶梯设计，一句话点出（"观众先看到他→她发现"），用户能感知镜头语言的存在
   - 高张力/L3 场景的信息差镜头语言写法（WITHHOLD→REVEAL→MISDIRECT 结构、被凝视母题、静爆节奏）见 `references/narrative-gap-techniques.md`
   - **氛围片段 vs 剧情场景**（2026-08 外部评测 8.7 的核心反馈："优秀电影片段 Prompt ≠ 优秀动画剧情 Prompt"，视觉 A 级/剧情 B+）：多镜 L3 提示词如果只有"氛围+动作"，没有以下四件套，就是氛围片段——交付前自查：
     1. **角色目标**：她/他为什么在这里、要得到什么（"我来拿我的画"比"她走进画室"强一个量级）
     2. **冲突对象**：谁挡在目标和需求之间（显性对立 + 隐性情感，如"客人的婚纱 vs 当年约定的婚纱"）
     3. **角色选择**：必须有 climax_choice——角色主动做决定（伸手拿画→被握住→没抽回），不是被动接受环境
     4. **角色弧线**：开场状态 ≠ 结束状态（要结束过去→发现没结束→选择留下）；行为可被动机解释而非"剧情需要"
   - **动作密度控制**（AI 生成稳定性关键）：15s 内核心动作 ≤4 个（评测：8 个动作/15s = 高概率位置漂移/手部错误/动作跳跃）；每个镜头有 camera motivation（为什么这样拍：ECU because 观众必须读到犹豫）

## 红线清单分层（2026-08 用户确认）

用户要求红线清单**去除用户级内容偏好条款**（不写学生涉性/不露隐私器官/不要魔法特效/兽化程度写死——这些不再作为 skill 固化红线，用户自行把握创作边界）。交付红线说明时按三层呈现：

1. **格式红线**（校验器强制，违反必 ERROR）：六段顺序、`[Shot 1]` 无时间戳、切点递增且在时长内、summary 前缀 6 选 1、每主体恰一行 retention、外观图不独立定义、`<d>` 原文保留、成品零包装、声音三层分离。
2. **法典成人规则**（tag-h3）：男性默认隐形、半遮半掩>全裸、情绪梯度节奏、场景重交互轻背景。
3. **平台合规**：**用户优先**（2026-08 用户明确要求，ai-2d-animation §13.2 已改）——用户要求与平台政策冲突时以用户创作意图为准，平台政策仅作风险提示；Level 4 平台实际不支持时降级 Level 3 满格表达并告知原因，不擅自改动用户设定。

不要把用户个人内容偏好写进 skill 红线；用户要求的尺度变化以当轮指令为准。

## 用户偏好条款已移除（2026-08 用户明确要求）

用户已要求从 3 个 H3 workflow skill（`h3-video-prompt-workflow` / `minimax-h3-video-prompt-pipeline` / `h3-video-prompt-iteration`，均 curator-managed）的 SKILL.md 中**删除写死的用户偏好条款**，包括：不要魔法特效、主角=人类配角=兽人/半兽、日漫风>真人实拍、亚洲面孔、多步特写链偏好、交付约定（中文/改动表/MEDIA/💡）等。同时删除了 `minimax-h3-video-prompt-pipeline/references/character-template.md`（《深渊赌局》角色模板）。

**未来会话行为**：不得再默认套用这些偏好；风格、特效、角色构成、交付格式一律按当轮指令决定。若需要为某项目固化偏好，应存为该项目的独立模板（如 `{当前工作区}\` 下），而非写进 skill。

## 单镜时长定标（2026-08 实测精化，非拍脑袋）

```
段时长 ≈ 对白句数 × 1.3s + 画面节拍数 × 0.8-1.5s
```

- **对白句数只算角色台词/OS**。心跳嘀声、惊呼、环境声、呜咽、轻笑一律不算对白（实测：误把音效当对白会导致估算偏 1.3s/句）。
- **画面节拍 = 关键叙事事件数**（一个完整动作变化/一次信息揭示/一次情绪转折 = 1 拍），不是描述里用词数量。例：`俯身 → 胸口擦过手臂 → 发丝滑落` = 3 拍。
- 3 拍及以上的慢推/情绪镜用 ×1.3；纯动作/爆发镜用 ×1.0；揭示/窥视慢推镜可到 ×1.5。
- **冲击帧/特效镜例外**：白闪、光晕、变形等纯视觉爆发镜（0.3-0.5s）不套公式，直接按 0.5s 以内定——它们是情绪放大不是叙事拍。
- 15s 视频对白控制在 3-4 句；9+ 节拍或 6+ 句对白拆成 2 镜，拆点在 hook 断点。

## Pitfalls（本环境实测）

- **Windows 用户名含特殊字符**：bash 单引号路径会炸，路径一律双引号包裹
- 校验脚本路径含空格/单引号时同样用双引号
- 迭代改时长后必须用新 `--duration` 重跑校验（旧切点会越界）
- 15s 建议 4-5 镜（切点约 3s/6s/9.5s/12s），末镜留展示时间，切点不能标在时长边界（00:15.000 必挂）
- 剧本没给台词原文 → 不虚构 `<d>` 对话；非语言人声（轻笑/叹息）放 overall_soundscape
- 交付给完整可粘贴版，不只给 diff
- 参考图外观只用 vision_analyze 提取细节进 subject_definitions；只有真实首帧/关键帧锚点才独立定义 `<Picture N>`（须配 keyframe completion）
- 校验脚本若报 `AttributeError: 'NoneType' object has no attribute 'strip'`：CSV/字段有缺失值，先修数据/脚本的 None 处理再跑

## 场景还原度测试工作流（新增）

当用户明确要求“图一角色、图二场景，测试 H3 对场景的还原度”时，优先做**单事件、场景主导**的测试，不要写成普通剧情片段：

1. **先判定图二的资产关系**：如果图二是实际场景构图/首帧/关键帧，定义为独立 `<Picture 2>`，summary 使用 `[keyframe completion]`；如果图二只提供场景外观而不要求构图复现，才把场景写入 `<Subject 2>` 并使用 `[reference generation]`。用户说“还原度/保持原布局/同一视角”时，默认优先 `keyframe completion`，不要把场景图仅当普通 subject。
2. **输入检查**：视觉接口通常有文件大小限制；大图先压缩到 10MB 以下再分析，保留原图作为 H3 上传资产。临时缩略图/URL 无法读取时，不得假装看过；应使用用户给出的 Scene Contract，并明确哪些细节是契约锁定而非视觉确认。
3. **测试结构**：默认 15s、3 镜：`Shot 1 = 同视角宽景锁构图`，`Shot 2 = 角色在场景中完成一个小范围动作`，`Shot 3 = 回到中广景并保持固定建筑锚点`。角色动作只作为尺度参照，场景占画面主体，避免对白和复杂剧情干扰测评。
4. **场景锚点清单**：在独立 Picture 定义和 detailed_description 中写出可验证锚点：地面几何、柱梁/门窗、固定家具、装饰物、光源方向、前中后景关系、角色可移动区域；明确“保持位置不变”“不新增房间/家具/人物/建筑结构/光源”。
5. **镜头与运动约束**：先 WS/Orient，再进行一次小幅 lateral track 或 push-in；不改变轴线、时间、天气和光向。Shot 3 必须保留稳定展示帧，便于与图二逐项对照。
6. **风格与还原分离**：不要用大量“反 3D”否定词替代场景锁定；风格词用于画面媒介，场景 Picture/Keyframe 才负责布局还原。若需要纯 2D TV 动画质感，使用稳定的 `Flat 2D hand-drawn TV anime cel animation, flat cel coloring, matte surfaces` 前缀，并保持与参考图风格一致。
7. **交付前验证**：运行 Ref2VA 校验器；额外检查 Picture 角色关系、`[Shot 1]` 无时间戳、后续时间递增、三镜都引用场景锚点、结尾为可比较的稳定状态。交付时说明图二采用的是 `keyframe completion` 还是 `reference generation`，避免用户误以为两者还原能力相同。

### 场景测试模板指针

场景还原测试的已验证结构可参考工作目录中的 `TEST_scene_fidelity_mainhall_15s.txt`；不要机械复制其中的资产关系，先按上面的 keyframe/reference generation 判定规则选择。

## 交付约定（本用户）

- 全程中文交流（提示词正文英文除外）
- 每轮给改动对照表（Markdown 表格：项目|变更）
- 文件保存到工作目录（如 `{当前工作区}/h3-prompts\\`），附 MEDIA 链接
- 💡 段给出下一步选项（拆条生成/再调一版/切 Ref2VA 图生模式）
