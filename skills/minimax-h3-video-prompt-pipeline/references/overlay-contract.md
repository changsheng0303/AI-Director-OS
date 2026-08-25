# Official core + local overlay contract

目标：完整保留 MiniMax 官方 `h3-prompt-writing`，同时保留现有本地长片、资产、连续性、风格和校验能力。采用组合，不采用 Fork。

## 1. 两层职责

### Official core（只读）

官方Skill独占以下权威：

- 输入模式：T2VA / I2VA / FL2VA / L2VA / Full-reference Ref2VA
- 顶层字段、字段顺序与英文输出要求
- 首帧/尾帧对齐语句
- Shot时间戳语法
- Picture/Video/Audio/Subject标签与引用关系
- retention marker与任务类型语义
- 4–15秒时长边界及官方示例

本地不得改写、复制后冒充官方、向官方目录写补丁，或新增官方未定义的输出顶层字段。

### Local overlay（可维护）

本地增强负责：

- PROJECT_BRIEF、SCRIPT_CANON、Narrative IR
- Runtime Map、Scene Geography、Shot IR
- 角色/场景/道具资产提示词与参考图绑定
- START/END状态、跨段邻接、音频时间线
- 项目风格、2D约束、题材方法、批量生产和修复
- 官方格式之外的项目文件与机器校验

## 2. 运行时组合

```text
Local preproduction artifacts
→ Local Shot/Asset/Continuity constraints
→ Official mode selection
→ Compile constraints into official allowed description fields
→ Official-format prompt
→ Official-format validation
→ Local package validation
```

本地状态不得作为第七段或自定义顶层字段写入最终Prompt。它们只能转译进：

- Base模式的 `integrated_multimodal_description`
- Ref2VA的 `subject_definitions / summary / retention_analysis / detailed_description`
- 官方声音字段

## 3. 冲突优先级

1. 用户当轮明确要求
2. 官方H3模式、字段和语义
3. 已批准SCRIPT_CANON与Shot IR
4. 已批准资产与连续性状态
5. 本地风格、题材和生成经验

若本地增强无法放入官方结构，应保留在伴随工件中，不修改官方Prompt格式。

## 4. 功能保留映射

| 现有修改功能 | 新形式 |
|---|---|
| 18分钟分段 | Runtime Map + Shot IR + 每段官方格式Prompt |
| 主角/主场景一致性 | Visual Asset Pack + asset binding + 官方参考标签 |
| 镜头连续性 | Continuity Manifest + 描述字段中的START→END动作 |
| 尾帧回灌 | I2VA/FL2VA/L2VA官方对齐语义或Ref2VA关键帧关系 |
| 角色/道具状态 | 结构化Manifest；只把当前可见状态编译进Prompt |
| 音频规划 | audio_timeline；当前片段声音编译进官方声音字段 |
| 2D/项目风格 | 项目资产锁；编译进官方描述字段，不设为官方默认 |
| 批量校验 | 独立本地脚本，不改变官方Skill |

## 5. 更新规则

- 官方更新先安装到临时/版本化位置并做差异比较。
- 更新 `upstream-lock.json` 前确认官方文件内容与目标commit一致。
- 官方更新只替换官方目录；本地Overlay仅在兼容性需要时单独升级。
- 用 `verify_official_upstream.py` 检查官方目录未被污染。
