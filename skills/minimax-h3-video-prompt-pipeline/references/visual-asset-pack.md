# Visual Asset Pack

在 Scene Geography 锁定后、Shot IR 与 H3 生产前，把会跨片段复用的视觉实体锁定成独立资产。它解决的是“主角和主场景每条 Prompt 都重新长一遍”的漂移问题；不替代 Shot Contract 的动作连续性。

## 1. 必须产出的资产

按剧本出现频率和连续性风险盘点，至少包含：

| 类型 | 必须资产 | 交付目标 |
|---|---|---|
| 角色 | 主角；跨场景的重要配角 | 独立角色主提示词、造型状态、参考图状态 |
| 场景 | 主场景；重复出现且承载调度的场景 | 独立场景主提示词、空间锚点、无角色基准图 |
| 道具 | 跨镜反复出现、被持握、被交接或承载剧情的道具 | 独立道具主提示词、持有侧/损伤/开合等状态 |
| 视觉基调 | 全片反复出现的画风、色彩、材质与光线规则 | 可复用风格句和禁止漂移项 |

不必为只出现一次的普通群众、一次性背景或没有叙事功能的小物件强制出资产图。

## 2. 每类资产的提示词要求

### 角色主提示词

一位角色一条锁定提示词，固定：年龄段、脸型、肤色、发型、瞳色、体型、服装层次、鞋、饰品、标志性道具、气质和画风。不要写当前场景动作、台词或镜头运动。

需要跨场景时，另列“可变状态”：衣物湿度、污渍、伤势、手持物、季节外套；这些状态必须引用同一个角色资产 ID，不能重新设计脸和发型。

### 场景主提示词

一个主场景一条锁定提示词，固定：建筑朝向、出入口、门窗、主要家具/地标、地面材质、前中后景、主光源、昼夜与天气基线、时代/地域特征和画风。优先生成“无角色基准图”，避免人物姿势被错误继承为场景资产。

场景输出必须同时列出分镜可用的空间锚点，例如 `A 旧书铺门口 / B 柜台 / C 左墙书架 / D 中央漏水区 / E 后窗`。

### 道具主提示词

固定形状、材质、尺寸关系、文字/纹样、磨损与开合状态。对于会被角色拿起、递交或落地的道具，记录默认手别、相对尺度和上一镜/下一镜的状态。

### 风格主提示词

只锁定整片共用的视觉语言：媒介、线条、上色、材质、色彩命题、镜头质感和允许的特效规律。不得混入具体角色或场景动作。

## 3. Asset ledger

把资产写入 `visual_asset_pack.md`，并给稳定 ID：

```text
AS-CHAR-01  许闻川  主角角色资产
AS-SCENE-01 知止旧书铺  主场景资产
AS-PROP-01  知止铜钥匙  关键道具资产
AS-STYLE-01 2D水墨都市奇幻  全片风格资产
```

人类审阅版写入 `visual_asset_pack.md`；机器版写入 `asset_ledger.json`。每项记录：`asset_id / type / canon_description / master_prompt / variable_states / reference_file / approval_status / used_by_segments`。

`approval_status` 只能是 `draft / user_approved / replaced`。H3 生产链使用 `user_approved` 资产时才可标为 B_shared_reference 或 A_frame_linked；纯文字草稿只能使用 C_text_only。

```json
{
  "project_id": "book-mountain-ep01",
  "assets": [
    {
      "asset_id": "AS-CHAR-01",
      "type": "character",
      "canon_description": "许闻川固定角色描述",
      "master_prompt": "full reusable image prompt",
      "variable_states": ["dry", "rain_wet"],
      "reference_file": "assets/xu-wenchuan.png",
      "approval_status": "user_approved"
    }
  ]
}
```

## 4. Asset binding

人类审阅版使用 `asset_binding.md`；机器版使用 `asset_binding.json`。每个 H3 段至少列出：

| segment_id | required_assets | reference_files | visible_state | continuity_use |
|---|---|---|---|---|
| EP01-S01-001 | AS-SCENE-01, AS-STYLE-01 | old-bookstore-base.png | 雨夜、门半掩、柜台右侧暖灯 | B_shared_reference |

绑定的资产必须真的出现在该段；不要把未出镜角色或无关道具塞进 H3 的 subject definitions。

```json
{
  "project_id": "book-mountain-ep01",
  "bindings": [
    {
      "segment_id": "EP01-S01-001",
      "required_assets": ["AS-SCENE-01", "AS-STYLE-01"],
      "visible_state": {"AS-SCENE-01": "rain_night"},
      "continuity_use": "B_shared_reference"
    }
  ]
}
```

## 5. 与 ai-image-assets 的交接

当用户需要生图提示词、参考图或角色/场景定稿时，调用 `ai-image-assets`：

1. 本技能先输出资产清单和优先级。
2. `ai-image-assets` 为角色、场景、道具生成对应的图片提示词或图片。
3. 用户确认资产图后，把实际文件路径写回 `reference_file` 和 `approval_status`。
4. 运行资产绑定校验后再开始 Shot IR 与 H3 文件；每段只绑定相关资产。

用户若只要求文字 H3，可保留 `draft` 资产并用 C 级连续性；必须明确说明这不是无缝视觉一致性保证。

## 6. 最小交付模板

```markdown
# Visual Asset Pack — {project}

## AS-STYLE-01｜全片风格
状态：draft / user_approved
主提示词：

## AS-CHAR-01｜{主角}
状态：
固定描述：
可变状态：
主提示词：
参考图：

## AS-SCENE-01｜{主场景}
状态：
空间锚点：
主提示词：
参考图：

## AS-PROP-01｜{关键道具}
状态：
固定描述：
状态机：
主提示词：
参考图：
```
