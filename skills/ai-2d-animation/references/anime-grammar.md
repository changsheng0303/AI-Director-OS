# Anime Grammar — 动漫本体语法 V1.2

动漫风格化不是"加一个 anime 形容词"，而是一整套**非写实的符号系统、表演惯例、作画语言与演出节奏**。真人电影语法是"让看不见的可见"，动漫语法是"让不可画的可见"——情绪直接画在画面上。

本文档是第 5/6 节的执行细则，与 `animation-rules.md`（通用原理）、`acting-rules.md`（写实表演）配合使用。任何镜头在分镜阶段必须先选择**演出处理类型**（见 §6），再决定具体语法。

---

## 1. 符号化情绪系统（Symbolic Emotion / 记号的演出）

动漫允许把情绪直接画成符号。以下符号必须作为**可见视觉元素**写入 Image/Video Prompt，禁止只用情绪形容词：

| 情绪/情境 | 符号化表达 | Prompt 写法示例 |
|---|---|---|
| 尴尬/紧张/无奈 | 大颗汗滴（anime sweat drop）挂在太阳穴/脸颊 | "large anime sweat drop on temple" |
| 压抑的愤怒 | 额头青筋（anger mark ⬆），有时配阴影压低 | "visible anger vein on forehead, low-angle shadow" |
| 震惊/爆点 | 背景速度线（speed lines）或集中线（concentration lines） | "radial speed lines background" |
| 黑化/杀意 | 负片气场（dark aura）、眼部打阴影（eyeshadow/glare）、刘海遮眼 | "dark aura, eyes hidden by bangs with glare" |
| 无语/呆滞 | 豆豆眼（dot eyes）、猫嘴（cat mouth）、半睁眼 | "dot eyes, cat mouth, blank stare" |
| 心动/治愈 | 背景花瓣/星星/闪光（sparkle、flower background） | "sparkling flower petals background, soft glow" |
| 害羞 | 脸部红晕（blush）、侧脸回避、双手捂脸 | "heavy blush on cheeks, averting gaze" |
| 惊讶定格 | 动作中断 + 全身定格 + 白闪（white flash） | "frozen pose, white flash frame" |
| 情绪爆发 | 颜艺（face fault：极度夸张扭曲的表情）+ 夸张变形 | "exaggerated gag face, extreme deformation" |
| 喜剧瞬间 | Q版化/SD化（super-deformed：头身比突然变 2-3 头身） | "super-deformed chibi form, 2-head proportion" |
| 台词情绪 | 对话框外的符号化音效（💢 ❗ ❓ ♨） | 写入 audio 字段："anger mark sound effect" |

**规则**：符号化情绪优先用于 Level 0-1 与喜剧/热血桥段；Level 2+ 的暧昧场景用**光、影、构图、肢体语言**替代符号，避免破坏氛围。

## 2. 有限动画美学（Limited Animation）

AI 视频生成的最大翻车源是"所有东西都在动"。动漫的本体美学恰恰是**静止 + 局部动**：

- **tachi-mise（站姿戏）**：对峙/对话/情绪戏，角色保持基本站姿，只动口型、呼吸、眼神、发丝、衣摆。镜头用微推（slow push）或静态制造张力。
- **口型动画**：3 帧循环（开-半-闭），不追求口型同步完美。
- **背景静止法则**：角色运动时背景尽量静止；只有镜头运动时才允许背景移动。写 Prompt 时明确 "static background"。
- **局部动优先**：一场戏只允许 1-2 个活动区域（如"只有头发和衣摆在动，身体静止"）。
- **关键帧密度**：动作戏提高关键帧密度（sakuga），日常戏降低密度，形成节奏对比。

**Prompt 写法**：Video Prompt 的 MOTION 段必须写明"哪些在动、哪些静止"（例："only hair and skirt sway, body and background static"）。

## 3. 作画爆发（Sakuga / 动画力）

高潮镜头的"作画力"来自以下手法的组合，**只在最重要的 10-20% 镜头使用**：

- **拉伸变形（smear）**：高速运动中角色/肢体沿运动方向拉伸、产生残影（motion smear）。
- **冲击帧（impact frame）**：击打/爆发瞬间插入 1-2 帧的极限变形或速度线全屏。
- **极限透视（extreme perspective）**：仰角/俯角强化速度与力量，肢体越轴透视。
- **白闪/黑闪（flash frame）**：爆发、回忆、震惊时的全屏闪白/闪黑。
- **动作压缩-爆发（anticipation→burst）**：先压（蓄力、蹲低、收拳），再瞬间展开。
- **Cut-in**：爆发瞬间插入无关信息特写（对手的脸、飞散的碎片、静止道具）制造停顿感。
- **Bank shot（复用镜头）**：回忆/惯例/变身/主题曲段落复用同一机位的镜头，建立仪式感。

**验收**：每个 Sakuga 镜头必须有明确的"蓄力帧→爆发帧→结果帧"三帧结构，写进 Key Pose 与 Timing。

## 4. 动漫构图惯例

| 构图 | 用途 | Prompt 写法 |
|---|---|---|
| 低角度英雄构图（low angle hero） | 角色登场/觉醒/压迫感 | "low angle, dramatic upward shot" |
| 对角线爆发构图 | 冲锋/能量释放 | "diagonal composition, dynamic burst" |
| 中心对称释放构图 | 大招/能量波/变身 | "centered symmetrical composition, energy release" |
| 剪影先置（silhouette first） | 神秘登场/氛围 | "silhouette against backlight" |
| 斜线地平线（dutch tilt） | 不安/失衡/打斗 | "dutch angle, tilted horizon" |
| 窥视构图（through-object framing） | 偷窥/紧张/信息隐藏 | "framed through foreground object" |
| 极端大特写转场 | 情绪爆点/信息揭示 | "extreme close-up on eyes, hard cut" |

## 5. 动漫上色与作画语言参数化（Visual Language）

决定"看起来像不像动漫"的五个视觉变量，**每个项目必须锁定**并写入 Image Prompt 的 VISUAL LANGUAGE：

1. **线稿（Lineart）**：粗细（thin/medium/bold）、是否闭合、是否带抖动（rough/clean）。日系标准 = clean thin-to-medium、闭合优先；厚涂系 = 无描边。
2. **上色（Coloring）**：赛璐璐平涂（cel shading，硬边二分阴影）/ 柔和渐变（soft gradient）/ 厚涂（painterly）。**默认赛璐璐**。
3. **阴影（Shading）**：阴影层数（1-3 层）、阴影形状（硬边/模糊）、阴影颜色（纯黑/彩色阴影如紫灰、蓝灰）。
4. **高光（Highlight）**：头发条状高光（hair shine streak）、眼睛高光（eye catchlight 星形/月牙形）、皮肤润光（skin sheen）。
5. **质感（Texture）**：网点（screentone）、噪点、纸感（canvas grain）、空气感（atmospheric haze / soft background）。

**锁定写法**："clean thin lineart, cel shading with 2-tone hard shadows in blue-gray, streak hair highlights, star eye catchlights, soft atmospheric background, light grain"。

**风格一致性检查**：连续镜头必须复用同一组五要素描述（放入 LOCKED 段），防止 STYLE_DRIFT。

## 6. 演出处理类型（Anime Treatment）

**每个 Shot Contract 必须声明 `anime_treatment`**（写入 storyboard 的"演出处理"列）：

| 类型 | 适用 | 要点 |
|---|---|---|
| `REALISTIC-ANIME` | 正剧、情感重场 | 写实表演 + 动漫造型，克制使用符号 |
| `SYMBOLIC` | 喜剧、情绪爆发 | 符号化情绪为主，允许颜艺/SD |
| `LIMITED` | 对话、对峙、日常 | 有限动画，静态+局部动 |
| `SAKUGA` | 战斗、高潮 | 高密度关键帧、变形、冲击帧 |
| `COMEDY-SD` | 搞笑桥段 | Q版化、节奏停顿、颜艺 |
| `MOE` | 萌系日常 | 反应镜头、红晕、豆豆眼、治愈光效 |

## 7. 类型演出惯例（Genre Performance）

| 类型 | 演出惯例 |
|---|---|
| 热血/战斗 | 爆发→冲击→结果三段、嘶吼/喊声、极限透视、背景速度线、BGM 鼓点 |
| 萌系 | 反应镜头优先（事件→角色反应→观众笑点）、豆豆眼、红晕、娇嗔音效、花瓣光效 |
| 日常/空气系 | 生活噪音、光影随时间变化、静物空镜头、留白、低信息密度 |
| 搞笑 | 颜艺、SD化、节奏停顿（先静后爆）、吐槽位、重复梗（recurring gag） |
| 悬疑/惊悚 | 低机位阴影、细节特写、屏息留白、声音先入（off-screen sound）、缓慢推镜 |
| 恋爱/擦边 | 光斑、樱花/逆光、心跳音效、拉近+慢推、视线交错、指尖微动 |

## 8. AI 视频生成中的动漫化执行

1. **关键姿势驱动**：优先描述"起始 Key Pose → 变化 → 结束 Key Pose"，而不是连续动作流。
2. **有限动画约束**：每段 MOTION 声明"动什么、不动什么"，明显降低模型漂移率。
3. **符号画出来，不要写形容词**："震惊"→"radial speed lines + frozen pose + white flash"。
4. **首尾帧策略**：复杂 Sakuga 用首尾帧锁死起止，中间交给模型。
5. **演出类型与 NSFW Level 联动**：Level 2+ 的暧昧场景用光影/构图/肢体（REALISTIC-ANIME 或 LIMITED）替代符号化夸张，保持氛围。
