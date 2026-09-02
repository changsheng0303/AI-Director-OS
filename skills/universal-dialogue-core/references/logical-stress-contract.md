# Logical Stress Contract

逻辑重音回答“这句话中哪一部分决定角色真正要纠正、对比、限定或迫使对方接受的信息”。它不是情绪强度，也不等于提高音量。

## 何时标注

只在重音位置影响句意或行动时标注：

- 否定与纠正：不是 A，是 B；
- 明确对比或排除项；
- 身份、对象、数量、时间、地点或范围限定；
- 关键揭示、承诺、拒绝、威胁和最终决定；
- 同一句存在两种合理解释；
- 潜台词在某个词上泄漏。

寒暄、简单确认、纯功能指令和句意只有一种读法的台词不标。单句默认一个主重音，必要时最多两个次重音；超过三个通常说明台词或标注需要重写。

## 两层数据

### 语义层：Canon

```yaml
logical_stress:
  - span: "不敢"
    role: rejected_alternative
    strength: light
    contrast_with: "不能"
    reason: "否定对方把原因理解成胆怯"
  - span: "不能"
    role: corrective_focus
    strength: strong
    contrast_with: "不敢"
    reason: "真正原因是存在不可逾越的限制"
```

`span` 必须逐字存在于 `exact_text`。语义角色可用：

`corrective_focus / contrast / rejected_alternative / negation / exclusivity / identity / quantity / time / location / reveal / commitment / threat / concealment_leak`

### 表演层：可替换实现

```yaml
delivery:
  pause_before_ms: 250
  pause_after_ms: 0
  rate: "前半句轻而快，主重音处放慢"
  pitch: "不刻意升高"
  volume: "保持低声，不靠喊"
  visual_cue: "说到主重音时抬眼看向对方"
```

语义层锁定后，下游可以根据演员、语言或引擎能力调整表演实现，但不能改变重音词和对比关系。没有可靠依据时只记录语义层，不编造精确毫秒、音高百分比或分贝。

## 各层表示

- **DIALOGUE_CANON**：保存 `exact_text + logical_stress + delivery`，是唯一真源。
- **剧本**：关键句使用简短括注，如`（“不敢”轻带；停半拍，“不能”落重，音量不抬）`。Fountain 导出可用 `_词_` 表示下划线重音，强主重音可用 `**_词_**`；样式只是显示，不是 Canon。
- **分镜**：引用 line ID，安排说话、停顿、听者反应和 `visual_cue`；不重新判断重音。
- **普通视频提示词**：用自然语言说明重音、停顿和可见动作，保留原台词。
- **SSML/TTS**：目标引擎支持时，把强调、停顿、语速、音高和音量分别编译；不把原始 SSML 写进剧本或不支持 SSML 的视频模型。
- **音频复核**：已有配音后，可把词级时间、重音/音高和停顿分别写入 TextGrid tiers；这是 QA 记录，不反向改写 Canon。

## 外部实现依据

- Fountain 项目保留粗体、斜体和下划线样式并交给下游渲染，说明剧本显示层可携带重音但不应承担语义推断。
- `ssml-builder` 把 `emphasis` 与 `prosody(rate/pitch/volume)`、`break` 分为不同接口，说明“强调什么”和“声音如何变化”必须分开。
- Text2ToBI 将 boundary、intonation 和 break index 分层并可输出 SSML；其自动预测仍有语料与边界限制，因此不能取代编剧确认。
- praatIO/TextGrid 适合保存时间对齐的词、音高和停顿层，用于成音后的检查。

## 质量门

- 重音 span 不在原台词中：FAIL。
- 普通句被过度标注：删除标注。
- 只写“加重语气”但没有语义原因：FAIL。
- 强调实现与角色身份冲突，如克制威胁被自动写成大喊：重做 delivery，不改重音语义。
- 下游修改 exact_text 或重音 span：必须提交 Dialogue Change Request。
