# Multi-Reference Fidelity — 多图参考保真度专项（2026-08 用户校准 v2：全图保真）

> **用户明确要求：上传的每一张参考图都必须有还原度**——不是"主图保真、其余弱化"，而是每张图在成片里都要可辨识地还原。
> v1 的"主次保真/降级弱化"思路已被用户否决（2026-08）。本文件为现行标准。

## 〇、官方校准（2026-08 狩猎吸收 · MiniMax-AI/MiniMax-H3 官方仓库）

官方 `h3-prompt-writing` skill 的 `references/ref-en.txt` 已吸收为 `references/official-ref2va-spec.txt`。官方规范与"全图保真"直接相关的 4 条铁证：

1. **一图可定义多 Subject，一 Subject 可合并多图**（官方原文："One subject may be defined by multiple reference assets, and one reference asset may provide multiple subjects"）。示例：`<Subject 2> is the fluffy white Samoyed in <Picture 2>, <Picture 3>, and <Picture 4>`——**三张图合并定义一只狗，每张图各贡献特征**。这正是"每张图都有还原度"的官方实现路径：多图合并到一个 Subject，逐图声明贡献。
2. **图只用做"特征来源"时不建独立 Picture 条目**（官方："If `<Picture N>` only identifies the source of another referenced item...cite it inside that item's definition without adding a separate line"）。即：场景/角色图作为 Subject 的属性源，写在 `<Subject N> is the [X] in <Picture N>, featuring...` 里；只有图作为**首帧/关键帧/构图锚点**时才单独建 `<Picture N>`。
3. **retention_analysis 只对 Subject 逐行**：多图合并的 Subject 写一行 `fully_preserved`（官方示例 `<Subject 2>...fully_preserved - 狗的特征逐项列出`），不要求每张图一行。**图的存在感体现在 Subject 定义里逐图点名 + retention 里该 Subject 的特征清单**。
4. **detailed_description 必须 350-500 英文词**（generation 任务）——描述太短 = 模型只能靠参考图脑补 = 还原度低。这是还原度低的**直接元凶之一**：文字细节必须够密，图才有"锚"可依。

## 〇一、总则

- **全图必还原**：进入提示词的所有 `<Picture N>` 都必须有可辨识的还原，默认不允许任何一张被弱化/背景化/丢弃。
- 单段图数上限是**拆段的理由，不是降级的理由**。
- retention_analysis 中 `weak_reference` **默认禁用**——除非用户明确说"这张图随便"。

## 一、为什么多图还原度低（根因 → 修复）

### 根因 1：参考图没有"任务归属" → 模型忽略部分图
多张图混在一起，只写 `<Subject 1> comes from <Picture 1>`，没说每张图各自负责什么属性域。
模型不知道 `<Picture 2>` 该用在哪 → 直接忽略 → 那张图"没有还原度"。
**修复：一图一任务**——每张图在 `subject_definitions` 里独占一个属性域（脸+发型 / 场景 / 服装 / 道具），互不重叠、缺一不可。

### 根因 2：图在正文里没有出现点 → 模型执行时不调用
图只在 `subject_definitions` 定义了，`detailed_description` 里从不提"此刻 `<Picture N>` 的内容可见"。
模型按正文执行，不会主动回去调用没被点名的图。
**修复：图→出现点映射**——每张图在正文至少一个 `[Shot N]` 里被点名。

### 根因 3：多宫格设计表/拼贴图 → 缝合怪
一张图里多个视图（正面/侧面/背面/表情包），模型不知道该还原哪个 → 五官/发型缝合。
**修复**（三选一）：① 提示词指明 `use only the front full-body view of <Picture 1>`；② 建议用户裁剪单视图；③ 当属性词典逐属性取用，retention 标 `partially_preserved` 说明取用范围。

### 根因 4：弱引用 + 主动标 weak_reference → 自断还原
`come from` 弱写 = "风格类似即可"；把某张图标 `weak_reference` = 主动告诉模型"这张不用还原"。
**修复**：全部 `exactly copied from` 强引用 + 逐属性清单；retention 只允许 `fully_preserved` / `partially_preserved`（必须有剧情理由：换装/昼夜/时段），**默认无 weak_reference**。

### 根因 5：单段图数超载 → 注意力稀释
模型单段注意力有限，≥5 张必然每张都"像但不像"。
**修复**：**单段 ≤4 张**；超了就拆段，每段内所有图仍全保真，分段生成后剪辑拼接。

## 二、全图保真守则（写提示词时逐条执行）

### 守则 1：一图一任务（属性域分离）
每张参考图独占一个属性域，绝不让两张图抢同一个任务：

| 图位 | 属性域 | 示例 |
|---|---|---|
| `<Picture 1>` | 角色脸+发型+瞳色（最高辨识） | 凉子的脸/银白发/高马尾 |
| `<Picture 2>` | 场景/环境（布局/家具/光色） | 篠原家客厅 |
| `<Picture 3>` | 服装或道具（单品） | 蕾丝内衣 / 心率表 |
| `<Picture 4>` | 第二角色或第二场景 | 悠太 / 玄关 |

### 守则 2：图图有出现点
每张图必须在 `detailed_description` 至少一个 `[Shot N]` 里被点名，且点名时写清"照图"：
```
[Shot 1] The character appears exactly as <Picture 1>: silver hair, high ponytail...
         The room matches <Picture 2>: low table, warm lamp, tatami unchanged...
         She wears the outfit from <Picture 3>...
```
写完自查：**逐图数一遍出现点**——任何一张图没有出现点，模型就不会还原它。

### 守则 3：retention 全图一行、禁 weak_reference
- 每张图（经 `<Subject N>` 引用）在 `retention_analysis` 恰有一行。
- 标记只允许：`fully_preserved` / `partially_preserved`（须注明剧情理由，如"换装"）。
- **`weak_reference` 默认禁用**——除非用户明确放弃某张图。

### 守则 4：同框多角色 = 全部还原
- 每个角色都绑自己的参考图，全部要求还原，不把配角降级成"模糊背影"。
- 办法：**拆镜聚焦**（每镜 1-2 角色，各自带图出现点）或全景句同时点名多张图：
  `In the full shot, <Subject 1> as <Picture 1> sits at the table, <Subject 2> as <Picture 3> beside him...`

### 守则 5：单段 ≤4 图，超了拆段
- 图数超限 → **拆段**（按出场角色/场景拆），每段内全部图仍然全保真。
- 拆段后各段独立生成、剪辑拼接，不牺牲任何一张图的还原。

### 守则 6：设计表处理（保留）
- 设计表/拼贴图必须先明确"还原哪个视图"（三选一见根因 3 修复）。
- 即使裁剪后，裁剪出的单视图图仍按全图保真规则处理。

### 守则 7：换装防漂移（保留）
- 参考图穿 A 服装，剧情要 B 服装：`face and hair exactly as <Picture 1>; only the outfit changes to [B]`。
- 服装图 `<Picture N>` 的还原 = "该服装单品被穿上"，retention 标 `partially_preserved`（理由：换装）。

### 守则 8：场景图还原
```
<Subject 2> is the room setting exactly copied from <Picture 2>: [布局/家具/光色锚点]，unchanged in all shots。
```
- 场景图有"无人物"要求时写明：`the background contains no people, as in <Picture 2>`。

## 三、subject_definitions 全图写法模板

```
<Subject 1> is the character whose face, hair color, hairstyle, and eye color are exactly copied from <Picture 1>: [逐属性清单]。
<Subject 2> is the room setting exactly copied from <Picture 2>: [布局/家具/光色锚点]，unchanged in all shots。
<Subject 3> is the outfit/prop exactly copied from <Picture 3>: [单品清单]，worn/held by <Subject 1> whose face matches <Picture 1>。
<Subject 4> is the second character exactly copied from <Picture 4>: [逐属性清单]。
```

## 四、参考图识别协议（用户只给类型、不点名对应时）

> 用户可能只告诉你"有角色图、有场景图、有道具图"，不逐张点名哪张对应谁（2026-08 用户定调：`我可能不会告诉你是哪几张图，我会大概告诉你是什么类型`）。
> 处理流程，按序执行：

1. **优先推断**：用文件名（如 `男主-白濑悠太.png`）、历史资产库（用户已有的角色/场景图）、分镜上下文（该段出现谁）推导出候选映射。
2. **可推断 → 用推断 + 附放图顺序表**：在交付物中附"放图顺序说明"（`第 1 张放 <Picture 1> 对应的角色图，第 2 张放 <Picture 2> 对应的场景图……`），让用户按序放图。推断假设标注 `ASSUMPTION`。
3. **不可推断 → 反问**：一段里有多个角色/多张场景图且无法确定对应关系时，用 clarify 反问，给出候选选项（"这段第 1 张角色图是花穗还是凉子？"）。**多问一句的成本远低于绑错图。**
4. **绝不瞎猜**：绑错图 = 还原出错误对象，破坏性大于"没还原"。宁可反问。
5. **识别对象是"图槽位"而非"图文件"**：提示词只定义 `<Picture N>` 槽位的内容角色（主角色/场景/道具），实际文件由用户按放图顺序表放入；若用户中途换图，只需按类型换文件，提示词不变。

### 放图顺序表模板（交付时必附）
```
📎 本段放图顺序（共 N 张）：
  第 1 张 <Picture 1> → [角色/内容描述]
  第 2 张 <Picture 2> → [角色/内容描述]
  ...
```

## 五、生成后自检（交付前必答）

- [ ] **逐图数一遍**：每张上传的参考图都有一行 subject 定义？（无孤儿图）
- [ ] 每张图都有独立属性域，没有两张图抢同一任务？
- [ ] 每张图在 `detailed_description` 至少一个出现点？（逐图核对）
- [ ] retention_analysis 每图一行，**无 weak_reference**（除非用户主动放弃）？
- [ ] 单段 ≤4 图？超了拆段了？
- [ ] 设计表指明了取哪个视图 / 已裁剪？
- [ ] 换装处写了"脸和发型不变"？
- [ ] 同框多角色全部点名还原，没有谁被降级成模糊背景？
- [ ] 参考图对应关系已确认（推断并标注 ASSUMPTION，或反问确认）？
- [ ] 交付物附了"放图顺序表"？
