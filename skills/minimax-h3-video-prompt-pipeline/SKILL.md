---
name: minimax-h3-video-prompt-pipeline
description: "MiniMax官方h3-prompt-writing的长片生产Overlay：保留官方Base/Ref2VA格式，同时增加剧本Canon、资产、连续分镜、音频、批量校验和修复。用于多片段或整集；单条新建用h3-video-prompt-workflow。"
license: MIT
metadata:
  hermes:
    tags: [minimax, h3, ref2va, video-prompt, continuity, storyboard, batch]
---

# MiniMax H3 连续视频提示词流水线

目标不是生成一组各自好看的短片，而是把锁定剧本编译成能够连续剪辑的 H3 片段链。长片的正确顺序是：

`SCRIPT_CANON + DIALOGUE_CANON → Narrative IR → Runtime Map → Scene Geography → Visual Asset Pack → Shot IR → Continuity Manifest → Audio Timeline → H3 Prompts → Validation`

## 适用边界

- 多片段剧本、分镜、整集、2 分钟以上长片：使用本技能。
- 单条新建：路由到 `h3-video-prompt-workflow`。
- 单条已有提示词局部迭代：路由到 `h3-video-prompt-iteration`。
- 多文件存量格式升级：路由到 `ref2va-batch-rewrite`。

## 上游权威与职责边界

- `ai-2d-animation` 是全链路治理与 Canon/Narrative IR 权威。
- `ai-video-storyboard-compiler` 是唯一生产级分镜与 Shot IR 权威。
- `universal-dialogue-core` 是台词生成、重写和Voice/Knowledge连续性的权威；批准后的 `DIALOGUE_CANON.exact_text` 下游只读。
- `director-mindset` 只提供导演创意、构图和表演判断，不另建一套生产镜号。
- `storyboard-script-spec` 只作为空间、轴线、时长和切镜 QA 规范，不另建平行分镜表。
- 本技能只把已批准的 Shot IR 与资产绑定编译为 H3，不重新设计剧情、角色、场景或镜头顺序。

## 必读规范

- 所有任务先读官方只读技能 `../h3-prompt-writing/SKILL.md`，再按模式读取其 `references/base-en.txt` 或 `references/ref-en.txt`。官方字段、顺序、模式和时长规则不得由本技能覆盖。
- 本地增强与官方格式的合并方式必须遵守 [references/overlay-contract.md](references/overlay-contract.md)。
- 2 分钟以上、8 段以上，或用户要求“连贯成片”时，必须读 [references/continuity-contract.md](references/continuity-contract.md)。
- 同类角色或场景会跨片段出现时，必须读 [references/visual-asset-pack.md](references/visual-asset-pack.md)，并先交付资产提示词与资产绑定表。
- 用户反馈故事跳、动机断裂或情绪突变时，读 [references/story-quality-gates.md](references/story-quality-gates.md)。

## 不可跳过的长片门槛

### 1. 锁定剧本

先冻结场次顺序、关键动作、对白、剧情结果，以及人物目标、情绪、伤势、服装、道具、时间、天气。发现剧情因果缺口时先修剧本；镜头或 Prompt 不能替剧本补逻辑。

### 2. Narrative IR 与运行时预算

使用已验证的 Narrative IR 记录场景目标、因果事件、人物知识/状态、伏笔、道具和入场/离场状态。随后建立 Runtime Map：`scene_id / script_range / timeline_start / timeline_end / dialogue_sec / action_sec / hold_sec`。

- 目标时长必须由逐场时长相加得到，禁止先决定“固定 N 条 × 固定秒数”再硬塞剧情。
- 单条生成时长遵守当前 H3 档位，默认不超过 15 秒。
- 对白按真实语速、停顿和反应计算；不能因平均分段而加速人物。
- 区分 `timeline_duration_sec` 与包含剪辑余量的 `generation_duration_sec`。

### 3. 场景空间锁定

在生成主场景资产之前，先由生产级分镜编译器记录固定锚点、人物初始站位、朝向、视线、轴线、移动路径、天气、光线和关键道具位置。没有空间锁定，不得生成主场景基准提示词，也不得批量写 H3。

### 4. Visual Asset Pack

在 Scene Geography 之后、Shot IR 和 H3 之前，建立可复用的 `Visual Asset Pack`。它至少包含：

- 每位主角和跨场景重要配角的角色主提示词；
- 每个主场景的场景主提示词及空间锚点；
- 跨镜反复出现或承载剧情的关键道具主提示词；
- 全片统一的风格、色彩、材质、时代和光线规则；
- `asset_binding.md`：每个镜头段绑定哪些资产、使用何种参考图、状态是否已获用户确认。
- `asset_ledger.json` 与 `asset_binding.json`：供机器检查资产ID、批准状态和逐段覆盖。

角色和场景资产必须作为独立提示词交付，不能只散落在 H3 的 `<Subject N>` 定义中。若用户需要实际生图提示词或参考图，使用 `ai-image-assets`；本技能负责指定哪些资产、何时生成、如何绑定回 H3。

未确认资产可用于概念分镜，但不得标记为可生产的 A/B 级连续链。每段 H3 仍须重复必要状态，因为资产图锁定身份与空间，不替代动作连续性。

### 5. Shot Contract

Shot Contract/Shot IR 必须来自 `ai-video-storyboard-compiler`。每个原子片段有且只有一个主要动作和一个主要镜头响应，并填写：

`segment_id / source_script_range / narrative_intent / location / duration / locked_state / start_state / trigger / primary_motion / acting_reaction / camera_response / secondary_motion / end_state / bridge_type / next_segment / continuity_method / reference_assets / guardrails`

硬规则：

- `end_state[N]` 必须可直接成为 `start_state[N+1]`。
- 人物离场、转身、换手、拾取、放下、受伤、服装变化必须在镜头链中看见或有明确省略依据。
- 相邻镜保持屏幕方向、视线、轴线、道具手别、光线和天气；改变时必须有可观察原因。
- 场景切换要标记 `scene_transition`，并说明声音、构图、动作、道具或光线接口。

### 6. Continuity Manifest

先写整批 `continuity_manifest.json`，再写提示词。Schema 和示例见 [references/continuity-contract.md](references/continuity-contract.md)。Manifest 是相邻关系的权威；任何 Prompt 修改导致起止状态变化时，必须先更新 Manifest，再联动修改相邻段。

### 7. 参考资产策略

H3 不会记住上一条生成结果。连续性等级必须明确：

- `A_frame_linked`：上一段尾帧作为下一段首帧/关键帧，或使用 video continuation；用于连续动作、关键表演和重要近景。
- `B_shared_reference`：每段重复绑定同一角色、场景、服装和道具参考，并写完整起止状态；用于普通对话和稳定场景。
- `C_text_only`：只用于空镜、过场或低风险镜头，不得承诺无缝人物连续。

每段必须自包含所需外观与状态，不能依赖文件外的“全局锁定段落”让模型记忆。

### 8. Audio Timeline

正式长片必须提供 `audio_timeline.json` 或等价机器表，记录对白/旁白起止、说话人、环境声持续区间、音乐段、声音桥和字幕文本。若存在 `DIALOGUE_CANON`，音频条目必须引用 `line_id/dialogue_version` 并逐字使用 `exact_text`。对白时长必须先在 Runtime Map 中占位，再编译进 H3；不得靠生成模型临时压缩或润色台词。

## Official H3 Adapter 输出

每个生成片段单独保存一个 `.txt`。先按官方 `h3-prompt-writing` 判断模式，再使用对应结构：

```text
T2VA / I2VA / FL2VA / L2VA:
integrated_multimodal_description:
overall_soundscape:
non_diegetic_music:

Full-reference Ref2VA:
subject_definitions:
summary:
retention_analysis:
detailed_description:
overall_soundscape:
non_diegetic_music:
```

- 不得把多条生产提示词合并进一个 Markdown 文件。
- 不得把纯文生 T2VA 伪装成 Ref2VA 六段式；是否需要 reference labels 由官方模式语义决定。
- I2VA/FL2VA/L2VA 的首帧/尾帧对齐行必须按官方 `base-en.txt` 原样组织。
- `[Shot 1]` 不带时间戳；后续切点严格递增且小于片段时长。
- 台词逐字保留为 `<d>[Chinese] 原话</d>`，不得润色或翻译。
- Ref2VA 的 `detailed_description` 遵守官方细节规则；Base 模式不套用 Ref2VA 的六段式或 retention 规则。
- 一个片段可含多个内部镜头，但只在信息重点或观看视角真正变化时切。
- 本地 Overlay 的 START/END、资产和连续性约束只能自然编译进官方允许的描述字段，不新增官方未定义的顶层字段。

## 批量生产顺序

1. 读取 `SCRIPT_CANON`、可选 `DIALOGUE_CANON` 与已验证 Narrative IR，不在本层改写剧情或台词。
2. 建立 Runtime Map，再由 `ai-video-storyboard-compiler` 锁定 Scene Geography。
3. 生成 `visual_asset_pack.md`、`asset_ledger.json` 和资产提示词；需要图片时用 `ai-image-assets`，确认后写回参考图路径。
4. 由唯一分镜权威生成 Shot IR，再生成 `asset_binding.json`、`continuity_manifest.json` 和 `audio_timeline.json`。
5. 先抽取一个高风险连续链（3–5 段）做样片提示词。
6. 检查资产绑定、结构化状态、音频占位、邻接和总时长后，再批量生成其余独立 `.txt`。
7. 每条跑 Ref2VA 语法校验；整批跑本技能的两个校验脚本。
8. 修改失败段时，同时审查资产绑定、前一段 END 与后一段 START，禁止只改中间文件。

## 校验

```powershell
python "<技能目录>/ref2va-prompt-optimizer/scripts/validate_ref2va_prompt.py" "<prompt.txt>" --duration <秒>
python "scripts/verify_h3_base_prompt.py" "<base-mode-prompt.txt>" --mode T2VA --duration <秒>
python "scripts/verify_ref2va_batch.py" <ref2va-prompt-files> --durations-json '<json>'
python "scripts/verify_asset_binding.py" "asset_ledger.json" "asset_binding.json" "continuity_manifest.json"
python "scripts/verify_continuity_manifest.py" "continuity_manifest.json" --require-asset-pack --strict-state-schema --require-audio-timeline
python "scripts/verify_official_upstream.py" "references/upstream-lock.json"
python "../universal-dialogue-core/scripts/verify_dialogue_handoff.py" "dialogue_canon.json" "audio_timeline.json"
```

必须修掉所有 ERROR。WARNING 需要人工审阅并在交付说明中记录，不得把“格式 PASS”描述成“影片已连贯”。

## 交付物

长片交付至少包含：

- `SCRIPT_CANON.md`
- `dialogue_canon.json`（有对白的正式生产项目）
- `visual_asset_pack.md`
- `asset_ledger.json`
- `runtime_map.csv` 或同等表格
- `scene_geography.md`
- `shot_contracts.csv` 或同等表格
- `continuity_manifest.json`
- `audio_timeline.json`
- 每片段一个 H3 `.txt`
- `asset_binding.md`
- `asset_binding.json`
- 校验结果摘要

交付表列出片段编号、剧本出处、时间线时段、生成时长、主要动作、起止状态、衔接方式、连续性等级、提示词文件和参考资产。

## 失败模式

- 只有人物外观锁定，没有状态链：单条好看但无法拼接。
- 主角和主场景只有散落的 H3 描述，没有独立资产提示词/参考图：外观和空间会逐段漂移。
- 用场景概要代替原子片段：一条 Prompt 塞数十秒剧情，生成必丢动作。
- 固定平均时长机械拆段：对白被截断、动作异常加速、总片长虚假。
- 多条六段式放进一个文件：无法逐条投喂与校验。
- 对所有模式强制六段式：违反官方 Base/Ref2VA 模式分流。
- 只写 `same as previous`：模型没有跨请求记忆。
- END/START 不相等：人物瞬移、道具换手、视线跳轴。
- 纯文字 C 级片段宣称无缝：能力声明不诚实。
- Prompt 阶段新增台词、角色或反转：破坏 SCRIPT_CANON。
- 只跑六段式校验：格式正确不等于剧情、时长或连续性正确。
