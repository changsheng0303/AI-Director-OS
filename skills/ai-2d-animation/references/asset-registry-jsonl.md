# Asset Registry — 资产注册表（JSONL 落地格式）

把 Asset Bible 从"文档"升级为**可追溯、可复用、能接续状态**的机器可读资产表。回答三件事：屏幕上具体需要什么、它与已有资产是不是同一个、此刻是哪种造型/视图/状态。

## 与 asset-system.md 的关系

- `references/asset-system.md`：资产类型、锁定策略、版本策略（概念层）。
- 本文件：注册表的**落地 JSONL 格式**与**复用判断规则**（操作层）。
- 产出建议存 `assets/asset-registry.jsonl`，随项目走。

## 数据模型

每条记录一行 JSON，字段：

```json
{
  "id": "char_youtai_v002",
  "type": "character | costume | prop | location | bg | fx | audio_motif",
  "name": "白濑悠太",
  "version": 2,
  "status": "locked | variant | deprecated",
  "source": "EP01-P1 | 创作者补充 | 参考图 ref_001.png",
  "locked_fields": ["脸型", "发色", "服装主色", "标志性道具"],
  "variant_fields": ["姿态", "表情", "配饰"],
  "state": {"pose": "standing", "gaze": "right", "prop": "heart_watch:on"},
  "used_in": ["EP01-S1-03", "EP01-S2-05"],
  "note": "心跳表是标志道具，变体不得移除"
}
```

### 字段说明
- `id`：`类型_名称_v版本`。只在结构性修改时升版本（与 asset-system.md 版本策略一致）。
- `status`：`locked` 设计锁定资产 / `variant` 允许变体 / `deprecated` 已废弃。
- `state`：接续状态快照（角色姿态/视线/道具状态/服装状态），每个镜头生成后写回（§8 Continuity State）。
- `used_in`：使用镜头列表，追溯复用。

## 复用判断规则（occurrence → decision）

从剧本拆出"出镜需求"后，判断是**复用已有资产**还是**新建变体**：

```
新需求 X 与已有资产 Y 比较：
1. 识别特征（脸型/发型/服装主色/标志道具）全部匹配 → 复用 Y，更新 state
2. 识别特征部分匹配，但 X 是明确的新造型/新状态 → 建变体 Y_v+N（variant）
3. 识别特征不匹配 → 新建资产
4. 仅状态不同（姿态/表情/道具开关）→ 不建资产，只更新 state
```

### 关键纪律
- **不猜**："她""那个人""另一把钥匙"指谁 → 保留原称谓，`state` 标 `unresolved`，向创作者确认。
- **区分出镜形式**：实际出镜 / 画外声 / 屏幕/照片呈现 / 仅被提及——被提及不等于要做视觉资产。
- **不把每个名词建档**：只保留影响识别、复用、提示词、镜头或连续性的事实。
- **状态 delta 传递**：本场结束的 `state` 就是下一场的 `continuity_in` 输入；CHANGED 必须写明原因（§8）。

## 示例

```json
{"id": "char_youtai_v001", "type": "character", "name": "白濑悠太", "version": 1, "status": "locked", "source": "EP01-P1", "locked_fields": ["黑发", "校服", "左腕电子心率表"], "variant_fields": ["表情", "姿态"], "state": {"pose": "standing", "gaze": "forward"}, "used_in": ["EP01-S1"]}
{"id": "prop_watch_v001", "type": "prop", "name": "电子心率表", "version": 1, "status": "locked", "source": "EP01-P1", "locked_fields": ["屏幕显示数值"], "variant_fields": [], "state": {"display": 98}, "used_in": ["EP01-S1-06"]}
```

## QA 检查

- [ ] 每个出镜角色/道具/场景都能在注册表中找到（或已声明省略理由）
- [ ] 镜头引用的资产 ID 与注册表一致，无裸命名
- [ ] 跨镜头 state 连续：上一镜的 `state` = 下一镜的 `continuity_in`
- [ ] 变体有版本号，锁定的识别特征未漂移（防 CHARACTER_DRIFT）
