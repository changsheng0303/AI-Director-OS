---
name: h3-video-prompt-workflow
description: "MiniMax官方h3-prompt-writing的单条生产Overlay：保留官方T2VA/I2VA/FL2VA/L2VA/Ref2VA格式，同时增加本地风格、故事检查和校验；不负责多片段批量生产或存量批改。"
license: MIT
metadata:
  hermes:
    tags: [minimax, h3, ref2va, video-prompt, t2va, short-drama, chinese]
---

# MiniMax H3 单条提示词工作流（官方格式 Overlay）

## When to use

- 用户要求生成 MiniMax H3 / Ref2VA 格式视频提示词（文生视频 / 图生视频 / 参考生成 / 首尾帧）
- 用户从剧本 / docx 挑一个片段做一条 AI 视频提示词
- 触发词：H3、Ref2VA、六段式、文生视频、minimax 提示词

## 格式权威（官方Skill，只读加载）

MiniMax 官方 `h3-prompt-writing` 是唯一格式权威，**先加载再动手**：

- `h3-prompt-writing/SKILL.md`
- Base 模式：`h3-prompt-writing/references/base-en.txt`
- Full-reference Ref2VA：`h3-prompt-writing/references/ref-en.txt`

本技能是调用与质量控制 Overlay，不得改写官方字段、模式、顺序、时长和标签语义。项目风格、2D约束、连续性或校验增强只能作为本地扩展，编译进官方允许字段。

Overlay 的合并顺序与冲突规则读取 `../minimax-h3-video-prompt-pipeline/references/overlay-contract.md`。

## 模式分流

- T2VA / I2VA / FL2VA / L2VA 使用官方 Base 三段核心结构：`integrated_multimodal_description / overall_soundscape / non_diegetic_music`。
- Full-reference Ref2VA 才使用六段式：`subject_definitions / summary / retention_analysis / detailed_description / overall_soundscape / non_diegetic_music`。
- 纯文字 T2VA 不创建虚构的 `<Subject N>` 和 retention 行，不套用 `[reference generation]` 六段式。
- I2VA / FL2VA / L2VA 的首帧/尾帧对齐指令按官方 Base 指南原样组织。

- 剧本没给台词原文时**不编造 `<d>` 对话** — 轻笑/叹气/哼声等非语言人声放 `overall_soundscape`
- `DIALOGUE_CANON` 含 `logical_stress` 时，`<d>` 仍保持原文；在相邻表演/声音描述中用自然语言写明重音词、对比关系、停顿和音量策略。不得把 SSML 标签塞进 H3，也不得用翻译或加粗改变台词原文。

## 格式铁律

- 输出结构由官方模式决定，禁止对所有模式强制六段式
- `[Shot 1]` 无时间戳；后续 `[Shot N] At MM:SS.mmm,` 严格递增且在目标时长内
- 时长默认 5s，上限 15s；15s 建议 4–5 镜（切点约 3s/6s/9.5s/12s）
- 每个镜头必须引入新信息（主体/空间/状态/角度/时间）
- 官方字段正文用英文；只有 `<d>` 台词和可见文字保留原文语言
- 交付成品：不加标题、不加解释围栏、不加负面提示词、不加参数
- Ref2VA generation 的 `detailed_description` 通常 350–500 英文词；Base 模式不得机械套用 Ref2VA 词数与字段规则。精确时间线和完整对白优先。

## 2D 动漫风格标记（用户偏好 · 必带）

仅当用户或项目资产已锁定动漫2D时，使用以下防漂移写法；不得把该风格当作官方H3默认值：

- `subject_definitions`：角色写成 `anime 2D teenage girl, a cel-shaded anime character with large expressive eyes and slender proportions`；场景写成 `drawn in 2D anime background art style`
- `detailed_description` 第一句放整体风格锚点：
  `style-anime-lineless: Japanese anime 2D illustration style, no outlines, cel-shaded flat coloring with solid color blocks, hard-edged cel shadows, streak hair highlights, clean smooth texture; ...; characters and backgrounds strictly in 2D anime art style.`
- 用户说"改成2D风格/生成2D动漫提示词" = 补以上标记即可，剧情/镜头/台词不动
- 用户问"动漫有哪些风格/想换风格" = 查 `references/anime-style-catalog.md`（三大预设 + 8 种上色技法 + 7 家公司流派 + 特殊形态 + 演出处理类型，各带英文锁定关键词）；选定后只改 `detailed_description` 风格前缀

### 反 3D 压制（3渲2 问题 · 2026-08 实证）

**症状**：参考图是纯 2D 动漫设定图（vision 验证无 3D 特征），但 H3/Seedance 生成出来像 3渲2——体积光影/材质反光/轻微景深。原因：视频模型训练数据里"动漫"均值大量来自 3D 渲染作品，模型默认理解就是 3D 感，`anime illustration` 压不住。

**修复**：`detailed_description` 风格前缀显式否定 3D 特征（比单纯加 2D 词有效）：

```text
Flat 2D hand-drawn TV anime cel animation style, absolute 2D cel look,
lineless anime illustration, no outlines,
no 3D render, no CGI, no volumetric lighting, no realistic material reflections, no depth of field,
flat cel coloring with solid color blocks, hard-edged cel shadows in darker tones, ...
```

三组压制词各有分工：`Flat 2D hand-drawn TV anime` = 2D 动画主信号；`no 3D render / no CGI` = 反渲染声明；`no volumetric lighting / no realistic material reflections / no depth of field` = 逐个否定 3渲2 三大特征。

**若重生成仍 3渲2**（模型能力上限，非提示词问题）：① 换平台（即梦 Seedance 2D 动漫支持通常优于 H3）② 换参考图类型——**TV 动画单帧截图感**（`TV anime screenshot, 2D cel` 标记）比设定图/立绘更稳，设定图会把模型带向"渲染感" ③ 关键帧锁死起止。

**参考图质检**：生成前先用 vision 判断参考图是否纯 2D（查体积光/AO/材质反射/景深/次表面散射），参考图带 3D 感则先换图再调提示词。

### 整集分段编译（多段提示词交付）

整集分段按剧情与动作边界决定；每段使用其官方输入模式对应结构并独立校验，不得一律输出六段式。

**插入微擦边场次后结构会变**（2026-08 实测）：纯情感集加一处 L1-L2 微擦边后，整集变 **5 段 = 3×15s + 1×15s 擦边段 + 1×5s 尾段（共 65s）**，或 11 镜 55s（擦边 1 镜并入主段）。分段边界按场次切，不硬凑 15s。

### 福利番单集微擦边节奏（用户校准 2026-08）

用户创作爆衣福利番（食戟向 / L3 基线）时，**即使纯情感铺垫集也必须插入 L1-L2 微擦边镜头**——"第一集没有微擦边的镜头"会被点名纠正，纯故事集=不合格。微擦边插入模式（实测可用）：
- **动作触发**：弯腰接碗 / 踮脚够高架 / 俯身递物 → 领口随动作微敞露锁骨+胸线上缘（`collarbone and the smooth upper line of her chest`）、浴衣下摆上撩露小腿/大腿（`the curve of her calves and thighs above the knee`）；写 `nothing more` 明确收住边界
- **环境加成**：蒸汽拂面脸颊微红、发丝沾水汽垂落（`steam drifts up past her flushed cheeks, strands clinging to her damp skin`）——经典 L2 手法
- **一次性配角承担擦边**：老板娘/年轻常客等，无感情线、不违反"无女二"设定；主角反应 = 目光移开/耳根微热（克制，学生角色不涉性）
- **镜头语言**：低角度仰拍（拉伸接碗/够瓶的身姿）、俯身视角（弯腰递物）
- **衣裂/爆衣特效演出**（食戟式爆衣镜头必读）：`references/foodgasm-burst-effects.md`——九种特效形式（白光爆发/布料炸裂/味觉电流/味觉幻境/冲击波/花瓣化/光环/表情神化/音效）+ 15s 三拍组合模板（入口→味觉电流→爆衣+幻境→评语）+ L3 合规要点（白光=天然遮挡缓冲、花瓣化=最安全美化、防雷词用 exposed 不用 bare）
- **合规**：穿着状态、不露乳首、无性暗示动作、非机能装（浴衣/和服/围裙）；擦边有叙事功能（居酒屋=生计，蒸汽=告别主题），非纯福利插入
- **嵌入位置**：情感铺垫集的中段作"呼吸节拍"（暖光场次），与压抑主线形成先暖后冷反差，增强归来戏的冲击

### 长格式整集（18 分钟番剧级）分段编译（2026-08 实测）

单集 18 分钟 = 上/中/下三部 × 6 分钟并发，每部 6:00 ≈ **24 段 × 15s**，一集 72 段。与 50s 集（3×15s+1×5s）是不同量级，编译方式：

- **编号规范**：`EP01_上部_段01_晨光街景_15s.txt`（集_部_段号_内容_时长）——**先规划全部分段编号再落盘**，中途补段会撞号（本次踩坑：补"黑车伏笔"独立段时与已有段02重名，需批量 mv 重排）
- **分段粒度**：按剧本场次切，每场 90s = 6 段；场次内按剧情节拍拆单段。单段一个主动作（三连舀汤/钢笔点纸/攥拳），拒绝多动作塞一段
- **每段仍独立 txt，按官方模式选择 Base 或 Ref2VA 结构并独立校验**；段间用 End State→Start State 衔接（模型无跨段记忆）
- **配套编译器文档**（ai-2d-animation V1.7 规范，`提示词\EP01_上部_编译器文档.md` 模板）：
  - Prompt Trace 总表：段×scene/beat×ending_function×单主动作×邻接类型
  - Shot Adjacency 五锁抽查（人物/空间/道具/光/方向）+ bridge_reason
  - Ending Function 分布表（SUSPENSE_HOLD/CHOICE_LANDING/RELATIONSHIP_LANDING 等 11 种，防模板化结尾）
  - 投喂批次建议（参考图绑定分组：试水段→男主图一段→文字角色段→全链段）
- **编译器审计脚本**（批量检查 24 段）：① 风格标记必含 `anime style|cel shading|2D animation|TV anime` ② 违禁形容词 `8k|masterpiece|cinematic|ultra-detailed` ③ 模板化结尾 `fade to black|lights dim|empty street`（注意 `without a fade to black` 是反模板化声明，正则会误报，人工复核）④ 动作顺序 trigger→action→reaction 词检（正则过严会误报，抽查确认）

### 环境/世界观批量修改后的提示词残留修复（2026-08 实测）

剧本环境大改（如街头摊位→现代小饭馆）后，批量替换提示词里的场景词（execute_code 跑 `replace` 映射表）会产生**语义残留**，必须精修：

- **动词不配**：`lifts the glass door`（布帘→玻璃门后 lift 不成立）→ 改 `slides open the glass door`
- **重复词**：`worn worn indoor slippers`、`warm orange warm street sign lights`（替换链叠加）→ 去重
- **残余旧词**：`small street stall`/`humble street stall`（映射表没覆盖的变体）→ 补映射
- **替换顺序**：长词先于短词（`humble street food stall` 在 `food stall` 之前），否则先被短词吃掉
- 改完全量重跑校验器 + 防雷词扫描 + `grep -inE "stall|awning|slabs|clogs"` 查残留



用户对批量生成的场景帧/配角设定图不满意（如"图片太丑了不需要"）时，**不要反复重出图**，直接回退纯文字管线：

- 场景：`subject_definitions` 用英文文字定义场景（空间/道具/光源），不建 `<Picture N>`；`detailed_description` 保留反 3D 压制词（`no 3D render, no CGI, no volumetric lighting`）
- 角色：**已获用户认可的参考图仍绑 `<Picture N>`**（男主图一），被拒的配角用纯文字定义（发色/眼镜/服装/气质全量锁定 + `fully_preserved`）
- 这样编译的提示词依然能过校验器，镜头效果取决于文字密度而非参考图

## 工作流

1. `read_file` 剧本 / 描述，确认片段与角色
2. 加载官方 `h3-prompt-writing`，先判断 Base 或 Full-reference 模式，再读取官方对应参考文件；本地风格/题材资料只能作为 Overlay
3. **故事层检查**（用户反馈"跳"或涉及多镜剧情时必读）：`references/story-craft-for-h3.md`——开场 3 镜关系线索、情绪阶梯禁跳级、Beat 因果四问、信息点 ≤3/15s、相邻镜头 30/70 连续性；修复顺序 Story → Scene → Adjacency → Camera → Prompt
3aa. **多图参考保真度**（2 张以上参考图必读）：`ref2va-prompt-optimizer/references/multi-reference-fidelity.md`（2026-08 用户校准 v2：**全图保真**）——**每一张参考图都必须可辨识还原，不允许弱化/降级任何一张（用户明确定调，weak_reference 默认禁用）**；一图一任务（属性域分离：脸+发型/场景/服装/道具）；每图在 `detailed_description` 至少一个点名出现点（逐图核对）；单段 ≤4 图，超了**拆段**（拆段=图多时的唯一解法，不是降级）；`exactly copied from` 强引用+逐属性清单；设计表（多宫格角色图）必须指明取哪个视图或建议裁剪单视图；换装必写"脸和发型不变"；同框多角色全部点名还原，不把配角降级成模糊背景
3ab. **参考图识别协议**（用户按类型给图、不逐张点名对应时必读——2026-08 用户定调"我可能不会告诉你是哪几张图，我会大概告诉你是什么类型，当你不明确也可反问我"）：① 先用**文件名/历史资产库/分镜上下文**推断哪张图对应谁（如 `男主-白濑悠太.png` → 悠太）；② 推断得出 → 用推断结果写提示词，交付时附**放图顺序表**（`第 N 张 <Picture N> → 角色/内容描述`），推断假设标注 `ASSUMPTION`；③ 推断不出（一段多角色/多场景分不清）→ **用 clarify 反问给候选选项**，不猜；④ **绝不瞎猜绑错图**——绑错 = 还原出错误对象，破坏性大于"没还原"；⑤ 提示词只定义 `<Picture N>` 槽位的内容角色，用户中途换图只需按类型换文件，提示词不变
3a. **悬疑/惊悚题材**（用户给悬疑参考图/深夜异响/躲藏窥视类）：`references/suspense-thriller-genre.md`——**用户校准：悬疑≠静止，"动态大一些"（惊醒→爬行→躲藏→钻床底→门把手→光束→僵住动作链）**；"反应先于原因"威胁画外、三段式时间轴、SUSPENSE_HOLD 结尾、微动作清单、悬疑负面提示词
3b. **分级检查**（L1-L4 提示词必读）：`references/nsfw-grading-for-h3.md`——分级只管内容边界不管通用镜头语言（特写/暧昧台词任何等级可用）、暴露梯度 L2<L3（**L3 尺度链：脱外衣→脱内衣→上身裸露**）、三不原则+遮挡三硬规则（**covering the nipple 精确表述/遮而不掩/裸露持续呈现**）、**直面原则（禁黑场/定格/剪影/关灯收尾）**、**剧情驱动四要素（关系/目标/冲突/反转，裸露=手段非情境）+ 服装性暗示前提（禁机能装）**、L3 性暗示镜头语言（ECU 边缘/慢镜/窥视/主观镜头）、L4 降级 L3 满格表达；**§7 防裸露四原则（写"剩什么"不写"露什么"/绝口不提 nipple-breast/遮挡=穿着的衣物/镜头裁切兜底）——生成"脱衣→露全胸"时的根因与对策**；**§7b 完整脱衣写法（脱内衣动作完整+构图遮挡三选一：裁切/背面/手臂——"脱了但看不见"，半脱写法已弃用）**；**§8b 裸露对称原则（男女都可脱：他先脱/互解/同时脱，男裸不受三不约束）**；**§8 多镜快剪（用户要"分镜更多"时：保持镜头数压缩单镜时长，5s 可 8-12 镜）**
3b2. **长分镜→多段 H3**（EP 级 30+ 镜分镜 / 2 分钟+ 整集）：路由到 `minimax-h3-video-prompt-pipeline`，本单条工作流不承担整集编译
3b3. **批量段编译器审计**（整部 20+ 段交付时读）：`references/compiler-audit-batch.md`——ai-2d-animation V1.7 编译器层批量检查（风格标记/违禁形容词/模板化结尾/动作顺序）+ 编译器文档结构（Prompt Trace / Adjacency 五锁 / Ending Function 分布 / 投喂批次）+ 已知正则误报；配套 SKILL.md 正文「长格式整集分段编译」小节
4. 按官方模式写单条提示词到用户工作目录 `.txt`
5. 按模式校验（路径含单引号 `l'x` 时用**双引号**包裹路径）：
   ```bash
   # Base T2VA/I2VA/FL2VA/L2VA
   python "{Codex技能目录}/minimax-h3-video-prompt-pipeline/scripts/verify_h3_base_prompt.py" "<file>" --mode <MODE> --duration <N>

   # Full-reference Ref2VA
   python "{Codex技能目录}/ref2va-prompt-optimizer/scripts/validate_ref2va_prompt.py" "<file>" --duration <N>
   python "{Codex技能目录}/h3-video-prompt-workflow/scripts/check_description_words.py" "<file>"
   ```
   Base 模式不运行 Ref2VA 六段式与 `detailed_description` 词数检查。Ref2VA 两个校验均通过后再交付。
6. 修掉所有 ERROR（WARNING 当审阅提示），**PASS 后再交付**
7. 交付：中文表格说明改动 + 完整提示词代码块 + MEDIA: 文件链接 + **参考图清单表**（见下方）

### 参考图清单表（交付必附 · 2026-08 用户校准）

每段提示词交付时，必须附带一张**参考图使用清单表**，让用户一目了然知道哪些图已有、哪些需生成：

| 段 | Subject | 角色/场景 | 参考图文件 | 状态 |
|---|---|---|---|---|
| 段XX | `<Picture 1>` | 角色名 | 完整文件路径 | ✅ 已有 / ❌ 需生成 |

**表尾追加**：
- 需要新生成的图片列表（编号 / 内容描述 / 建议生成方式 / 画幅）
- 共用道具/场景图标注（多段共用 = 优先高质量生成）
- 已有图路径必须用用户机器上的**实际路径**（查 `EP1_参考图清单与分段表.md` 或搜索资产目录）

此表的价值：用户不需要逐段翻提示词去拼凑"我到底还缺什么图"，一张表全看清，直接进入生成/投喂流程。

## Pitfalls

- **`[Shot 1]` 绝对不能带时间戳**（2026-08 实测踩坑两次）：写 `[Shot 1] At 00:00.000,` 会被校验器判 ERROR（"[Shot 1] must not have a timestamp"）。只有 `[Shot 2]` 起才标 `At MM:SS.mmm,`。写完每段先自查第一镜有没有误带
- 外观来源图片只在 `<Subject N>` 里引用；只有真实首帧/关键帧才独立定义 `<Picture N>`
- 切点标在时长外（如 15s 标 00:15.000）→ 校验必挂；**最后一镜切点必须严格小于时长**（15s 用 00:14.500，标 00:15.000 算越界）
- 仅 Full-reference Ref2VA 有 `summary` 任务类型前缀；Base 模式没有 `summary` 字段
- 校验 `--duration` 只传纯数字（15/10/5），别从文件名子串截取（如 "5s附段" 截出 "5s" → invalid float 报错）
- 台词被"润色"成英文 → 必须 `<d>[Chinese] 原话</d>` 原文保留
- 每个 `retention_analysis` 行里的 shot 列表必须与 `detailed_description` 实际出现范围一致，别留孤儿标签
- **Subject 定义与 retention 行必须一一对应（2026-08 实测两坑）**：① 在 `subject_definitions` 定义了 `<Subject 2>` 但 retention_analysis 没给它行 → ERROR "must have exactly one retention row; found 0"（解法：画面里没出现的角色直接从 definitions 删掉，别留空 retention）；② retention 用了 `<Subject 2>` 但 definitions 没定义 → ERROR "Labels used later but never introduced"（解法：补定义）。**每段写完自查：definitions 定义了几个 Subject，retention 就有几行**
- **用 patch 改 `subject_definitions` 后必须重读文件+重跑校验**（2026-08 实测）：patch 时 old_string 覆盖了含 `<Subject 2>` 的行，结果 Subject 1 定义被复制成两行、Subject 2 丢失——校验器能查出 retention 不匹配，但重复的 `<Subject 1>` 行要 read_file 才能发现
- 迭代改时长（5s→15s）后必须用 `--duration 15` 重新校验，旧切点可能越界
- 角色设定混搭（人类 + 半兽 + 全兽）容易在生成时崩一致性：`subject_definitions` 里把每个角色的兽化程度写死（full human / human-faced with ears+tail / anthropomorphic）
- **防雷词子串陷阱（L3 及以下强制）**：`double-breasted`（双排扣）含 "breast" 子串、`bare` 易混进 "barely"——写服装词时警惕；交付前跑扫描：
  ```bash
  grep -inE "nipple|breast|boob|bare|naked|nude|penis|vagina|dick|cock|pussy|\bsex\b" *.txt && echo "FAIL: 有防雷词" || echo "PASS: 零防雷词"
  ```
  命中后替换：`double-breasted` → `double-buttoned` / `twin-button line`；`bare chest` → `chest and torso exposed`（避开 bare/naked/nude 整词）
- 换风格（如赛璐璐→无线平涂）时改 `detailed_description` 风格前缀即可，`subject_definitions` / `summary` / 台词不动；改完重跑校验 + 防雷词扫描
- **多图参考还原度低的第一嫌疑不是模型，是提示词写法**（2026-08 用户反馈"还原度怎么这么低"）：逐条对照 fidelity 规则自查——① **`detailed_description` 词数是否 ≥350**（官方规范 350-500，实测全部 15 段原版只有 123-256 词 = 模型脑补 = 还原度低**头号元凶**，跑 `scripts/check_description_words.py`）；② 图数是否 >4（超了拆段）；③ subject 定义是否 `exactly copied from` + 逐属性清单（禁 `come from` 弱写）；④ 每张图在 detailed_description 是否有出现点（无出现点=模型不还原）；⑤ 角色图是否多宫格设计表未指明视图；⑥ 换装处是否写了"脸和发型不变"。修完提示词再怀疑模型，别一上来换模型/换平台
- **优化已有提示词时的三查清单**（2026-08 实测：用户给旧版段04/05要求优化）：① 词数不足（旧版 280 词 < 350 最低线 → 补构图/光线/运镜细节，不改剧情台词）；② 缺场景 Subject 定义（旧版只定义角色没定义教室/门口 → 补 `<Subject N> is the [场景] in <Picture N>`）；③ 动作节奏模糊（旧版"缩回再探出"没写时间间隔 → 补 `A half-second of empty doorframe passes in stillness` 精确节拍）。三步修完重跑校验器+词数检查
