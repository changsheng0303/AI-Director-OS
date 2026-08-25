# Prompt Engineering Rules

## 1. Prompt 是执行契约，不是文学描写
优先使用可验证的信息：主体、状态、动作、空间、镜头、时间、连续性。

## 2. 静态与动态分离
Image Prompt 描述“状态”；Video Prompt 描述“变化”。

## 3. 变量分层
`LOCKED`：角色设计、服装、关键道具、场景风格
`SHOT`：姿态、表情、构图、镜头
`MOTION`：动作、运镜、节奏
`OPTIONAL`：粒子、光效、背景动态

失败时优先只修改 SHOT/MOTION，避免破坏 LOCKED。

## 4. 避免模糊词
“很有动漫感”“非常震撼”“电影级”不能替代具体视觉行为。
应写成：线条、色块、阴影层数、姿态、镜头、Timing、动画效果。

## 5. Negative Prompt
只写已知高风险项，不堆无关负面词。优先：角色漂移、额外肢体、服装变化、错误方向、摄影写实化、背景变形。

## 6. 动漫视觉语言参数化（Anime Visual Language）

"动漫感"必须写成**五个可锁定的视觉变量**（详见 `anime-grammar.md` §5），禁止使用"很有动漫感"这类无法执行的词：

1. **线稿 Lineart**：thin/medium/bold、clean/rough、闭合或无线描边
2. **上色 Coloring**：赛璐璐平涂（cel shading）/ 柔和渐变 / 厚涂 —— 日系默认赛璐璐
3. **阴影 Shading**：层数（1-3）、硬边/模糊、阴影色（黑/蓝灰/紫灰）
4. **高光 Highlight**：发丝条状高光、眼瞳星形/月牙形高光、皮肤润光
5. **质感 Texture**：网点、噪点、纸感、空气感雾化

同一项目内五要素放入 LOCKED 段复用，连续镜头禁止更换——这是防 STYLE_DRIFT 的第一道锁。

## 7. 演出符号必须画出来

情绪不能只写形容词，必须转成可见视觉元素（`anime-grammar.md` §1 符号表）：
"震惊" → `radial speed lines + frozen pose + white flash`；
"害羞" → `heavy blush + averting gaze + sparkle background`；
"无语" → `dot eyes + cat mouth`。
Video Prompt 的 MOTION 段必须声明"哪些在动、哪些静止"（有限动画约束），
例如：`only hair and skirt sway, body and background static`。


## 8. V1.4 Narrative Video Compiler
Video Prompt 不再只是“START/MOTION/END”的动作说明，而是由以下顺序编译：
`Narrative Intent → Information State → Visual Motif → Start State → Trigger → Primary Action → Reaction → Camera Response → Secondary Motion → Timing → End State → Continuity`。

### 8.1 Shot Atomicity
默认每个片段只有一个主动作变化。多个动作必须存在明确因果链，否则拆镜。

### 8.2 Camera Necessity
所有非 Static 运镜必须能回答：它增加了信息、情绪或空间认知中的至少一项。

### 8.3 Model-Readable Language
优先：`slowly turns head / pauses / lowers umbrella / focus remains on her face / camera holds`。
避免：`like a memory`, `poetically`, `deeply cinematic` 等不能验证的文学化词汇。

### 8.4 Prompt Trace
每个 Video Prompt 应能回溯：`shot_id + shot_version + locked_variables + changed_variables + camera_logic + failure_risks`。
