---
name: universal-dialogue-core
description: "生成、补写、重写或诊断影视/动画/短剧对白，控制角色口吻、知识边界、潜台词、回合咬合、群戏、谎言承诺连续性与可演性。用于纯台词、场景对白和SCRIPT_CANON台词定稿；不重做剧情结构、世界观或分镜。"
license: Proprietary package supplied by user; local optimization and integration only.
metadata:
  version: "2.2.0-local"
  upstream_version: "2.1.0"
  language: zh-CN
---

# Universal Dialogue Core

题材无关的影视对白核心。目标是让台词符合人物、当前目标、知识边界和关系压力，并让每一轮真正作用于上一轮，最终产生可追踪的场景变化。

## 边界

本技能负责：

- 写、补、改、压缩或诊断台词；
- 区分角色声音与压力下的临时变形；
- 控制谁知道、怀疑、误信或隐瞒什么；
- 处理潜台词、策略变化、多人对话和对话退出；
- 生成可锁定的 `DIALOGUE_CANON` 供分镜、配音和视频提示词使用。

本技能默认不负责：

- 重写世界观、人物身份、整集结构或既定结局；
- 决定正式机位、镜头调度或视频模型格式；
- 为了“更有戏”擅自增加秘密、冲突、关系或情节结果。

根源在上游时标记 `UPSTREAM_CONFLICT`，只给最小必要建议，不用润色掩盖结构问题。

## 上游优先级

`Safety > SCRIPT_CANON > Character Truth > Knowledge Boundary > Listener Model > Turn Coupling > Scene Function > Continuity > Genre Style > Cleverness`

已批准的场景目标、剧情结果、角色事实和固定对白是只读Canon。用户没有授权改剧情时，只修改台词表达、必要微动作和停顿。

## 运行模式

### FAST

用于1–6句、小修、单句角色化和局部去AI味。

加载：本文件 + 已有Voiceprint。执行：`Voice → Intent → Knowledge → Naturalness → Final`。

### STANDARD（默认）

用于普通场景对白。按需读取：

- [core-craft-rules.md](core-craft-rules.md)
- [scene-function-router.yaml](scene-function-router.yaml)
- 命中的一个 `scene-functions/*.md`

三人以上且群戏结构真实影响策略或联盟时，可额外加载 `scene-functions/group-dialogue.md` 作为modifier。STANDARD只使用一个primary function。

### DEEP

用于首次登场、审问、秘密揭露、重大冲突、关系转折、群戏高潮、名场面或用户要求精修。

额外按需读取：

- [voiceprint-schema.yaml](voiceprint-schema.yaml)
- [dialogue-rubric.md](dialogue-rubric.md)
- [continuity-ledger.yaml](continuity-ledger.yaml)

若可观察触发事件让对话机制真正改变，允许 `phase 1 primary → phase 2 primary`，最多一次切换；两个primary不得并行。

实验题材适配器位于 `experimental/genre-adapters/`，默认不加载。只有通用Core已成立且用户明确需要题材增强时，后置加载一个。

## 对话负荷

写作前分类：

- `FUNCTIONAL`：任务、确认、指令和必要信息；优先FAST，不强制冲突或潜台词。
- `INTERACTIVE`：有人物关系与微目标，但无重大对抗；使用轻量Scene Change和最小Beat。
- `DRAMATIC`：存在显著目标冲突、秘密、风险或关系变化；运行完整流程。

负荷只能由明确trigger改变。禁止把简单交流强行写成情绪高潮：`OVERDRAMATIZATION`。

## 十二项核心不变量

1. 角色不是作者传声筒，只能按身份、欲望、恐惧和当前状态说话。
2. 区分知道、相信、怀疑、听说、误信和愿意承认；观众知道不等于角色知道。
3. 重要台词必须执行行为：试探、拒绝、隐瞒、逼问、说服、安慰、挑衅、谈判或终止。
4. 先确定真实目的，再决定表层说法；潜台词不是机械说反话。
5. 戏剧对白需要阻力；无阻力则压缩。
6. 场景结束至少改变信息、信念、情绪、关系、权力、决定、行动或未解压力之一。
7. 可演性优先于文学性，允许短句、改口、打断、沉默和动作回应。
8. 画面和表演已表达的信息不由台词重复。
9. 对话复杂度与场景负荷相称。
10. 追踪“我认为对方知道/怀疑什么”，但只建模会影响当前策略的二阶认知。
11. 每个新回合必须回应上一回合的语言行为；有意无视也必须是策略。
12. 达到目标、阻断、延期、放弃或payoff后及时结束，删除解释性尾巴。

## 输入归一化

优先读取上游已有内容，不重复发明：

```yaml
scene:
  id:
  previous_event:
  scene_goal:
  start_state:
  required_end_state:
  required_information: []
  forbidden_information: []
characters:
  - name:
    stable_traits: []
    current_emotion:
    public_goal:
    hidden_goal:
    knowledge: []
    suspicions: []
    secrets: []
    speech_style:
dialogue_constraints:
  duration:
  tone:
  audience:
  output_mode:
```

非关键缺口采用最小假设。会改变角色动机、知识、关系、场景结果或受众边界的缺口，不得擅自补设定；提出一个窄问题或标记 `UPSTREAM_CONFLICT`。

## 核心流程

1. 判断 `FAST/STANDARD/DEEP` 与对话负荷。
2. 定义一句 `Scene Change`：结束时什么与开场不同。
3. 为主要说话者定义Want：想让对方做、相信、承认、停止、提供或隐藏什么。
4. 定义Resistance及其如何影响说话策略。
5. 建立Information Boundary：`KNOWN / SUSPECTED / UNKNOWN / LIED_ABOUT / FORBIDDEN_TO_REVEAL`。
6. 只为会影响策略的事实建立Listener Model。
7. 用 [scene-function-router.yaml](scene-function-router.yaml) 路由一个主要场景功能。
8. 先规划Beat再写句子；每拍改变策略、信息、压力或关系。
9. Actor Pass：人物、知识、动机、暴露程度、口吻和压力变形。
10. Director Pass：场景变化、策略变化、表演空间和画面重复。
11. Exit Check：payoff后压缩尾巴。
12. STANDARD过Light Gate；DEEP按Rubric定向修复，最多3轮，明确极致精修最多5轮。

## Beat最低字段

```yaml
beat:
  owner:
  visible_action:
  immediate_goal:
  hidden_goal:
  tactic:
  target:
  expected_response:
  actual_response:
  response_mode: answer | refuse | redirect | challenge | repair | ignore | misread | accept | escalate | deescalate
  information_change:
  emotional_shift:
  relationship_shift:
  next_pressure:
```

短场景可缩为 `Setup → Turn → Payoff`。

## 场景功能路由

路由按对话行为机制而非题材。可用primary：

- conflict
- concealment
- interrogation
- negotiation
- intimacy
- reconciliation
- exposition_delivery
- casual_exchange
- emotional_turn

`group_dialogue`只作为structural modifier。具体选择与冲突处理读取 [scene-function-router.yaml](scene-function-router.yaml)。

## Voiceprint

Voice不是口头禅列表。至少由信息选择、策略、句式、词汇、节奏、回避方式、情绪暴露方式、关系差异和压力变形共同构成。需要完整结构时读取 [voiceprint-schema.yaml](voiceprint-schema.yaml)。

## 逻辑重音

当一句台词存在否定纠正、明确对比、范围限定、身份/数量/时间强调、揭示、承诺、威胁或重音位置会改变句意时，读取 [logical-stress-contract.md](references/logical-stress-contract.md)。

逻辑重音属于 `DIALOGUE_CANON` 的语义层：先记录强调哪一段、为什么强调、与什么形成对比，再单独给出可选的停顿、语速、音高、音量或可见动作。普通功能性台词不标；不得把每句都写成“加重语气”。

## Gate与定向修复

以下任一出现即FAIL：

`KNOWLEDGE_LEAK / PERSONALITY_BREAK / MOTIVE_VOID / RESISTANCE_VOID / EXPOSITION_DUMP / VOICE_COLLAPSE / SCENE_STAGNATION / EMOTION_OVEREXPLAIN / VISUAL_REDUNDANCY / CONTINUITY_BREAK / UNPLAYABLE_PROSE / TACTIC_FLATLINE / FALSE_SUBTEXT / AUTHOR_SPEAK / OVERDRAMATIZATION / LISTENER_MODEL_BREAK / TURN_DECOUPLING / DECEPTION_CONTINUITY_BREAK`

`TAIL_DRIFT`是软失败，通常只压缩payoff后的冗尾。

DEEP评分读取 [dialogue-rubric.md](dialogue-rubric.md)。90分是内部修订门，不得宣称为客观质量证明。包内benchmark是spec-level和自评回归，不是独立盲测。

只修最低失败层：知识→Information Boundary；Voice→信息选择/句式/节奏；动机→Want；策略→Beat；连续性→Ledger；场景停滞→Scene Change；冗尾→Exit。

## 输出模式

- 纯台词：只输出可用对白。
- 影视剧本：角色名＋必要微动作＋台词。
- 台词诊断：原句／问题／修改／原因。
- 完整设计：Scene Change／Wants／Function／Beats／Final Dialogue／State Delta／Score。
- 批量场景：每场保留Scene Change／Function／Final Dialogue／Score／必要警告。

用户未指定时，默认输出最终可用内容，不展示完整内部推理。

## 系统交接

正式生产时读取 [references/system-integration.md](references/system-integration.md)。核心规则：

- 从角色层接收Voiceprint和关系变体；
- 从 `screenplay-master` 接收场景目标、Canon、信息边界和起止状态；
- 输出 `DIALOGUE_CANON`，下游分镜、配音、字幕和H3只读；
- 下游不得润色、压缩或翻译固定对白，除非有批准的Dialogue Change Request。

生产交接后运行：

```powershell
python "scripts/verify_dialogue_handoff.py" "dialogue_canon.json" "audio_timeline.json"
```

## 参考与来源

- 完整上游v2.1原文：[references/source-v2.1-full.md](references/source-v2.1-full.md)
- 通用工艺：[core-craft-rules.md](core-craft-rules.md)
- 逻辑重音与下游编译：[references/logical-stress-contract.md](references/logical-stress-contract.md)
- 评分规则：[dialogue-rubric.md](dialogue-rubric.md)
- 包验证记录：[VALIDATION.md](VALIDATION.md)
- 回归案例：`tests/`

本地入口为v2.2.0-local；上游ZIP与原始文件不被修改。
