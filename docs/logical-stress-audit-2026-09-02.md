# 逻辑重音项目检索与系统接入 · 2026-09-02

## 检索并读取的项目

- `nyousefi/Fountain`：纯文本剧本格式；解析器保留粗体、斜体和下划线样式并交给显示/导出层处理。可用 `_词_` 或粗体+下划线表现剧本重音，但样式本身不说明为什么强调。
- `mandnyc/ssml-builder`：将 `emphasis` 与 `prosody(rate/pitch/volume)`、`break` 分为独立接口，并校验强调强度和语音参数。说明语义强调、停顿、语速、音高、音量不能混成一句“加重语气”。
- `Howell-Prosody-Lab/Text2ToBI`：从文本预测边界、语调和 break index，可输出表格、inline 标注或 SSML；项目明确声明部分指标仍为实验性，不能替代编剧确认。
- `timmahrt/praatIO`：读写 Praat TextGrid，支持词/音素区间、pitch 点和多 tier 时间对齐，适合已有配音后的重音与停顿 QA。

## 系统决定

1. `universal-dialogue-core` 是逻辑重音唯一判定权威。
2. 逻辑重音分为语义层和表演层：
   - 语义层：span、作用、强度、对比项、原因；
   - 表演层：停顿、语速、音高、音量、可见动作。
3. 普通台词不标；单句默认一个主重音，最多三个 span。
4. `exact_text + logical_stress` 写入 `DIALOGUE_CANON`；下游只能编译，不得重选。
5. 剧本显示可使用括注或 Fountain 样式；视频提示词使用自然语言；TTS 目标明确支持时才输出 SSML；已有音频可用 TextGrid 做后验 QA。

## 新增实现

- `references/logical-stress-contract.md`
- `scripts/compile_logical_stress.py`
- `scripts/test_logical_stress.py`
- `examples/logical-stress-line.json`
- Screenplay Graph 的 `logical_stress` 与 `delivery` 字段
- Storyboard audio ledger、Video Prompt IR 和 H3/Seedance/Fafajing Adapter 继承规则
