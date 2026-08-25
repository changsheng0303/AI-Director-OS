# Video Prompt IR v1.0

在选择视频引擎格式之前，将剧本、分镜、创意和参考素材整理为中立的 Video Prompt IR。IR 只表达创作意图、素材关系和时间状态，不包含 H3、Seedance 或 Fafajing 的最终字段、语言和长度规则。

## 1. 输入模式

先确定一种主模式：

- `T2VA`：纯文本生成完整视听时间线。
- `I2VA`：一张图片是 0 秒首帧，画面从该状态向前发展。
- `FL2VA`：首帧和尾帧均已给定，需要设计两者之间的连续变化。
- `L2VA`：只给尾帧，需要反推合理起始状态并逐步收敛到尾帧。
- `FULL_REFERENCE`：混合图片、视频、音频或多个可追踪主体参与生成。
- `VIDEO_EDITING`：直接修改一个已有视频。
- `VIDEO_CONTINUATION`：从已有视频的结束状态继续生成。

同一任务可叠加 `AUDIO_REUSE` 或 `AUDIO_REFERENCE`，但只能有一个主视频模式。图片较多但角色不明确时，先判断它们是关键帧、主体来源、场景/风格参考还是故事板；该判断会改变生成路径，无法安全推断时再询问用户。

## 2. 素材角色

为每个真实存在的素材分配稳定 `asset_id` 和一种或多种角色：

```text
image: first_frame | last_frame | keyframe | subject_source | scene_source | style_source | storyboard
video: edit_source | continuation_base | motion_source | rhythm_source | subject_source
audio: full_copy | partial_copy | voice_timbre | music_style | dialogue_source | beat_source | ambience_source
```

文件类型不等于素材角色。视频带声音不自动产生音频复用；图片只提供人物外观时不是关键帧。不得为不存在的素材建立引用。最终引擎标签由 Adapter 根据本条提示词中的首次出现顺序重新编号，不继承资产库或上一条提示词的编号。

## 3. 关键帧路径

- `I2VA`：首帧锚定 → 动作启动 → 连续发展 → 结果或反应。
- `FL2VA`：首帧状态 → 可观察中间变化 → 差异逐步缩小 → 尾帧状态。默认优先单镜连续插值，除非用户明确要求切镜。
- `L2VA`：合理前态 → 明确触发与变化路径 → 最终镜逐步收敛 → 尾帧落点。
- `VIDEO_CONTINUATION`：继承源视频最后的身份、位置、动作方向、镜头、光线、声音和道具状态，再引入新变化。

## 4. 中立结构

```yaml
ir_version: video-prompt-ir/1.0
target_engine: h3 | seedance | fafajing | other | unresolved
input_mode: T2VA | I2VA | FL2VA | L2VA | FULL_REFERENCE | VIDEO_EDITING | VIDEO_CONTINUATION
duration_seconds:
source_refs:
  story:
  narrative_ir:
  shot_ir:
assets:
  - asset_id:
    media_type: image | video | audio
    roles: []
    provenance:
subjects:
  - subject_id:
    source_asset_ids: []
    locked_traits: []
frame_anchors:
  start:
  intermediate: []
  end:
transition_path:
  start_state:
  trigger:
  intermediate_changes: []
  end_state:
shots:
  - shot_id:
    start_time:
    composition:
    primary_action:
    camera:
    end_state:
speakers:
  - speaker_id:
    subject_id:
    voice_source_asset_id:
dialogue:
  - speaker_id:
    language:
    verbatim_text:
    timing:
    crosses_cut: false
    cutoff_at_end: false
audio_relationships:
  - asset_id:
    relationship: full_copy | partial_copy | reference | weak_reference
sound_layers:
  diegetic_events: []
  ambience_and_physical: []
  non_diegetic_music:
constraints: []
```

只填写当前任务需要的字段。快速单镜概念稿可在内部使用简化 IR；生产级项目应保存 IR、来源引用和版本。

## 5. 共享不变量

1. 用户给出的对白、歌词和可见文字逐字保留，不翻译、不润色；不清楚的内容标记为不清楚，不猜测。
2. 说话人 ID 按目标视频中首次发声顺序分配并跨镜复用；视觉主体 ID 与说话人 ID 分离。
3. 对白和镜内音乐属于时间线事件；环境/物理声与观众专属配乐分层记录。
4. 视频编辑、视频续写、音频复制和音频风格参考必须区分，不能因素材存在而自动推断关系。
5. 所有切点必须递增并位于总时长内；首镜是否显示 0 秒时间戳由最终 Adapter 决定。
6. Adapter 不得静默改变 IR 的剧情、对白、素材角色或关键帧关系。若引擎能力不足，报告受影响字段并请求降级决定。

## 6. Adapter 边界

- **H3 / Ref2VA**：读取 `ref2va-prompt-optimizer` 的规范，输出其要求的六段式英文格式并运行 H3 Validator。不得继承 Fafajing 的中文正文或字符数要求。
- **Seedance**：读取 `seedance25-prompt-workflow`，按所选 Seedance 模式重新组织 IR。不得套用 H3 六段式。
- **Fafajing**：读取 `fafajing-prompt-writer` 的 Basic/Full-reference 指南，输出中文正文及其固定模板。不得把 Fafajing 的语言、长度和精确指令句提升为通用规则。
- **专项增强层**：`tag-h3`、`micro-expression-video-prompts`、`design-disney-animation-prompts` 和 `character-prediction-skill` 只修改其被授权的维度，不能夺取引擎格式权威。

## 7. 路由检查

交给 Adapter 前确认：主模式唯一、目标引擎明确、素材角色无歧义、引用素材真实存在、首尾状态可连接、对白逐字、声音层分离。输出后只运行目标引擎对应的 Validator。

