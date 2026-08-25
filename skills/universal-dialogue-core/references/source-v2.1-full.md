# Universal Dialogue Core Skill v2.1

> 题材无关的影视 / 动画 / 短剧 / 连续剧台词母 Skill。
> 核心任务：在不知道作品属于恋爱、喜剧、悬疑、热血或任何具体题材的前提下，仍能稳定生成**人物成立、目标明确、信息受控、潜台词有效、节拍可演、场景发生变化**的对白。

## 0. Metadata

```yaml
name: universal-dialogue-core
version: 2.1.0
category: screenwriting.dialogue.core
language: zh-CN
default_mode: STANDARD
runtime_principle: core_first_function_second_genre_optional
roles:
  - dialogue_writer
  - actor_voice_checker
  - dialogue_director
  - dialogue_doctor
  - continuity_checker
```

### Trigger

写 / 补 / 改 / 优化台词或对白；角色口吻；潜台词；多人对话；台词自然化；对话攻防；台词诊断；dialogue / screenplay dialogue / character voice / dialogue doctor。

### Non-Goals

默认不负责：

- 重写世界观；
- 重做整集剧情结构；
- 改角色身份或核心人物设定；
- 决定完整分镜、机位或镜头调度；
- 为了“更有戏”擅自改变场景结局。

若台词问题根源来自上游，标记 `UPSTREAM_CONFLICT`，只给最小必要建议。

---

# 1. Architecture

固定四层：

```text
L1 Universal Core      通用台词机制，始终有效
        ↓
L2 Scene Function      当前这场对话正在做什么；STANDARD 0–1 个，DEEP 可顺序切换最多 2 个
        ↓
L3 Genre Adapter       可选实验层；默认不加载
        ↓
L4 Project / Character 项目规则与角色 Voiceprint
```

**优先级：**

`Safety > Character Truth > Knowledge Boundary > Listener Model > Turn Coupling > Scene Function > Continuity > Genre Style > Cleverness`

题材不得反向覆盖人物真实性。

---

# 2. Runtime Load Policy

目标：**让通用 Core 独立解决大多数任务，同时避免把所有规则常驻上下文。**

## FAST

适用：1–6 句、小修、单句角色化、局部去 AI 味。

加载：

- `SKILL.md`
- 已提供 Voiceprint（若有）

执行：

`Voice → Intent → Knowledge → Naturalness → Final`

不加载 Scene Function Pack，除非用户明确指定复杂功能。

## STANDARD（默认）

加载：

- `core-craft-rules.md`
- `scene-function-router.yaml`
- 命中的 **1 个 primary Scene Function Pack**
- `universal-dialogue-template.yaml` 仅在需要结构化输入/批处理时读取

默认只加载 1 个 primary function；三人以上且群戏结构真实影响策略/联盟时，可额外加载 `group_dialogue` 作为 structural modifier。若场景中途发生明确机制转折，STANDARD 仍保持单 Function；DEEP 才允许按顺序切换到第 2 个 primary function，禁止并行堆叠。

执行：

`Normalize → Scene Change → Wants → Resistance → Information → Function Route → Beats → Draft → Actor Pass → Director Pass → Gate → Final`

## DEEP

适用：首次登场、关系转折、重要冲突、审问、秘密揭露、群戏、情绪高潮、名场面、用户要求精修。

额外按需加载：

- `voiceprint-schema.yaml`
- `dialogue-rubric.md`
- `continuity-ledger.yaml`
- 最多顺序使用 `2 primary phases + 1 structural modifier` Scene Function Pack（只在存在明确机制转折时）

额外执行：

`Listener Model Audit → Turn Coupling Audit → Candidate Selection → Dialogue Doctor → Continuity Audit → Exit Audit → Full Score → Targeted Rewrite`

### Genre Policy

`experimental/genre-adapters/` **不属于默认运行链路**。

只有当：

1. Universal Core 已通过；
2. Scene Function 已明确；
3. 用户或项目明确需要题材风格增强；

才允许后置加载 1 个 Genre Adapter。

Genre 只调节表达偏好，不负责修复角色、动机、信息或场景结构问题。

---

# 3. Twelve Universal Laws

## U1｜Character Truth

角色不是作者的传声筒。角色只能基于自己的身份、人格、关系、欲望、恐惧和当前状态行动。

## U2｜Knowledge Boundary

角色只能说自己：

- 知道的；
- 相信的；
- 怀疑的；
- 愿意承认的；
- 此刻有理由说的。

`怀疑 != 确认`，`听说 != 亲眼知道`，`观众知道 != 角色知道`。

## U3｜Dialogue Is Action

重要台词必须执行行为，而不是只“表达内容”。

可执行：试探、逼问、拒绝、隐瞒、转移、说服、拖延、安慰、挑衅、求证、拉近、推远、控制、示弱、谈判、终止话题、改变联盟等。

没有行为目的的句子：优先删、压缩或转动作。

## U4｜Surface ≠ Intent

默认 `真实目的 != 表层措辞`。

不是强制每句话“含蓄”，而是先明确角色真正想达到什么，再决定愿意说到什么程度。

## U5｜Resistance Creates Dialogue

对话成立必须有阻力。阻力可来自：目标冲突、信息差、自尊、秘密、误会、礼仪、身份差、第三人在场、时间压力、害怕暴露、价值观冲突。

没有阻力时，优先压缩对话。

## U6｜Scene Must Change

重要场景结束后，以下至少一项变化：

- information；
- belief；
- emotion；
- relationship；
- power；
- decision；
- action direction；
- unresolved tension。

## U7｜Playable > Literary

先让演员能自然说出口，再追求漂亮。允许短句、改口、停顿、不回答、打断、答非所问和动作回应。

## U8｜Image Carries Meaning Too

能由表演、动作、视线、停顿、物件和环境自然承担的信息，不用台词机械重复。

## U9｜Proportionality

不要为了“高级”给简单对白强加冲突、潜台词、停顿或金句。

对白复杂度必须与场景负荷匹配：功能性交流可以直接，互动性交流只需要微目标与微变化，戏剧性交流才运行完整攻防。

## U10｜Listener Model

角色不仅依据“客观上谁知道什么”说话，还依据**自己认为对方知道什么、怀疑什么、误会什么**来选择策略。

写关键台词前至少区分：

- `A knows X`；
- `A thinks B knows X`；
- `A thinks B suspects X`；
- `A is wrong about B's knowledge`。

隐瞒、试探、审问、谈判中若忽略这一层，会导致人物策略失真。

## U11｜Turn Coupling

对话不是两篇独立独白交替出现。除非角色有意无视，每个新回合都必须对上一回合的**语言行为**产生响应。

允许的响应包括：回答、拒答、转移、反问、纠正、挑战、误解、沉默、打断、接受、升级、降级、修复。

若连续多轮只是各说各的立场：`TURN_DECOUPLING`。

## U12｜Exit Discipline

对白必须知道什么时候结束。场景达到以下任一条件时优先收束：

- 目标达成；
- 目标被明确阻断；
- 决定被延后；
- 一方放弃当前策略；
- 代价超过继续谈的收益；
- Scene Change 已完成。

达到 payoff 后继续解释、总结、互相确认，会形成 `TAIL_DRIFT`。

---

# 4. Input Contract

优先读取上游已有内容，不重复发明。

```yaml
scene:
  id:
  location:
  time:
  situation:
  previous_event:
  scene_goal:
  start_state:
  required_end_state:
  required_information: []
  forbidden_information: []

characters:
  - name:
    identity:
    stable_traits: []
    relationship_to_others: {}
    current_emotion:
    public_goal:
    hidden_goal:
    fear:
    knowledge: []
    suspicions: []
    secrets: []
    behavior_logic:
    speech_style:
    forbidden_style: []

dialogue_constraints:
  duration:
  tone:
  audience:
  continuity_notes: []
  output_mode:
```

缺少非关键字段：做**最小推断**继续，不为了补模板而编造大量设定。

关键事实不确定：内部标记 `ASSUMPTION`，采用对已有剧情改动最小的解释。

---

# 5. Dialogue Load Classification

在规划 Beats 之前先判断对话负荷：

```yaml
dialogue_load:
  FUNCTIONAL: 纯任务/确认/指令/必要信息；目标清楚、阻力极低
  INTERACTIVE: 有人物关系和微目标，但没有强对抗
  DRAMATIC: 存在显著目标冲突、秘密、风险、关系转折或重大状态变化
```

长场景允许记录：

```yaml
load_path:
  start: INTERACTIVE
  peak: DRAMATIC
  transition_trigger: "某句新信息 / 行动 / 决定"
```

负荷只能由明确 trigger 改变，不得为了制造高潮提前升级。

规则：

- `FUNCTIONAL`：优先 FAST；允许直接表达，不强制潜台词、Resistance 或多 Beat；
- `INTERACTIVE`：使用最小 Scene Change + 微目标 + 轻量 Beat；阻力可只是注意力差异、习惯或小摩擦；
- `DRAMATIC`：执行完整 Wants / Resistance / Information / Function / Beats / Audit。

若为简单场景人为加入强冲突、过度含蓄或情绪高潮：`OVERDRAMATIZATION`。

---

# 6. Universal Dialogue State

重要场景前，至少内部维护：

```yaml
character_state:
  emotion:
  emotional_intensity: 0-5
  public_goal:
  hidden_goal:
  fear:
  current_tactic:
  knowledge_delta: []
  vulnerability: 0-5

relationship_state:
  distance: 0-5
  trust: 0-5
  suspicion: 0-5
  power_balance: -2..2
  unresolved_pressure: []

information_state:
  known_facts: []
  suspected_facts: []
  hidden_facts: []
  false_beliefs: []
  lies_in_play: []

listener_model:
  perceived_knowledge_by_pair: {}
  perceived_suspicion_by_pair: {}
  mistaken_assumptions: []

conversation_state:
  open_questions: []
  claims_in_play: []
  promises_in_play: []
  exit_condition: ""
```

稳定人格与当前状态必须分开：**Voiceprint 决定“这个人通常怎么说”，State 决定“今天为什么和平时不一样”。**

---

# 7. Core Pipeline

## Step 0｜Classify Dialogue Load

先判断 `FUNCTIONAL / INTERACTIVE / DRAMATIC`。

如果是 FUNCTIONAL，自动降级到 FAST 或最小 STANDARD，不运行完整戏剧流程。

## Step 1｜Define Scene Change

用一句内部陈述回答：

> 这场戏结束时，什么东西与开场不同？

若答案只是“他们聊了一会儿”：检查是否需要压缩或标记 `SCENE_STAGNATION`。

## Step 2｜Define Wants

对每个主要说话者定义：

> 我现在想让对方 **做 / 相信 / 承认 / 停止 / 提供 / 隐藏 / 改变** 什么？

禁止使用“聊天”“表达感受”这种无行动性的目标。

## Step 3｜Define Resistance

回答：

> 为什么角色不能直接得到想要的结果？

阻力必须能反过来影响说话策略。

## Step 4｜Build Information Boundary

对关键事实标注：

```text
KNOWN / SUSPECTED / UNKNOWN / LIED_ABOUT / FORBIDDEN_TO_REVEAL
```

写句子前先确定谁能说到什么程度。

## Step 5｜Route Scene Function

读取 `scene-function-router.yaml`。

Scene Function 按**这场对话的行为机制**选择，不按作品题材选择。

STANDARD 最多：

`1 primary + optional 1 structural modifier`

DEEP 若存在明确转折触发，可使用：

`phase 1 primary → phase 2 primary + optional 1 structural modifier`

两个 primary 只能**顺序切换**，不得并行加载。

如果 Core 已足够且没有明显特殊机制，可不加载任何 Function Pack。若两个主功能只是同时存在，按 Router 的 `conflict_resolution` 选真正推动 Scene Change 的一个，另一机制写进角色 tactic。只有当场景机制在某个清晰 trigger 后真正改变，DEEP 才允许 function phase transition。

## Step 5.5｜Build Listener Model

对会影响策略的关键事实，补一个最小二阶认知表：

```yaml
listener_model:
  A_thinks_B_knows: []
  A_thinks_B_suspects: []
  B_thinks_A_knows: []
  mistaken_assumptions: []
```

不要全量建模；只追踪会改变当前台词策略的事实。

## Step 6｜Plan Dialogue Beats

先做最小 Beat Skeleton，再写句子：

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
  information_change:
  emotional_shift:
  relationship_shift:
  response_mode: answer | refuse | redirect | challenge | repair | ignore | misread | accept | escalate | deescalate
  next_pressure:
```

每个 Beat 至少改变：策略 / 信息 / 压力 / 关系中的一项。

除非 `response_mode=ignore` 且“无视”本身是策略，否则当前 Beat 必须能指出它在响应上一 Beat 的哪一个 move。

短场景可缩为：

`Setup → Turn → Payoff`

## Step 7｜Generate Draft

每句关键台词检查：

1. 为什么是这个角色说？
2. 为什么现在说？
3. 这句话想让对方发生什么？
4. 角色为什么选择这种说法，而不是更直接的说法？
5. 对方听完后，局面发生了什么变化？

其中 2 项以上答不上来：重写或删除。

## Step 8｜Actor Pass

检查角色自身真实性：

- 我真的会这样说吗？
- 我真的知道这些吗？
- 我现在真的有理由说吗？
- 这个表达强度符合当前状态吗？
- 换成另一个主要角色说，是否几乎不需要修改？

最后一项成立：`VOICE_COLLAPSE`。

## Step 9｜Director Pass

只检查四项：

1. 这段对白是否改变场景？
2. 人物是否过度配合，策略有没有变化？
3. 台词是否给表演留下空间？
4. 是否重复了画面已经提供的信息？

## Step 9.5｜Exit Check

内部明确：

```yaml
exit_condition:
  achieved: false
  blocked: false
  deferred: false
  abandoned: false
  payoff_reached: false
```

一旦 Scene Change 已完成，优先收束。删除 payoff 后的解释性尾巴、重复确认和主题总结。

## Step 10｜Universal Gate

STANDARD：执行轻量 Gate。

DEEP：读取 `dialogue-rubric.md`，必须 `>= 90/100` 且无 Hard Failure。

---

# 8. Scene Function Interface

Scene Function Pack 只能定义“这类对话机制如何运作”，不得写题材风格。

统一输出：

```yaml
function_output:
  core_problem:
  preferred_tactics: []
  beat_patterns: []
  information_rules: []
  pressure_rules: []
  payoff_conditions: []
  anti_patterns: []
  extra_checks: []
```

允许的 Pack 见 `scene-function-router.yaml`。`group_dialogue` 属于 structural modifier，不与审问、隐瞒、冲突、谈判等主功能竞争。

**Function 不得：**

- 重写角色人格；
- 修改世界观；
- 改场景既定结局；
- 注入“恋爱味 / 悬疑味 / 热血味”等题材语言；
- 取代 Core 的 Character / Knowledge / Motivation 检查。

---

# 9. Voiceprint Contract

Voice 不是“口头禅列表”。

稳定区至少覆盖：

- 句长；
- 直接度；
- 情绪暴露度；
- 礼貌；
- 词汇层级；
- 节奏；
- 幽默方式；
- 攻击方式；
- 犹豫方式；
- 回避方式；
- 不同关系下的变化；
- 压力下语言变化。

需要完整模板时读取 `voiceprint-schema.yaml`。

角色差异必须体现于：

**信息选择 + 策略选择 + 句式 + 节奏 + 回避方式 + 情绪暴露方式**。

只靠“笨蛋 / 那个 / 其实 / 哼”等口头禅区分角色，不通过。

---

# 10. Hard Failures

任一出现，即使分数 > 90 也不得通过：

1. `KNOWLEDGE_LEAK`：角色说出超出知识边界的信息；
2. `PERSONALITY_BREAK`：为剧情突然改变稳定人格；
3. `MOTIVE_VOID`：关键台词没有行为目的；
4. `RESISTANCE_VOID`：重要对话没有任何有效阻力却被强行拉长；
5. `EXPOSITION_DUMP`：角色复述双方都知道的背景；
6. `VOICE_COLLAPSE`：主要角色语言高度同质；
7. `SCENE_STAGNATION`：重要场景无有效状态变化；
8. `EMOTION_OVEREXPLAIN`：关键情绪被角色完整总结，没有表演空间；
9. `VISUAL_REDUNDANCY`：台词机械重复画面信息；
10. `CONTINUITY_BREAK`：知识、关系、决定或状态与前文断裂；
11. `UNPLAYABLE_PROSE`：书面化、长句化到难以自然表演；
12. `TACTIC_FLATLINE`：遭遇阻力后人物仍机械重复同一种说法；
13. `FALSE_SUBTEXT`：为了显得高级而故意含糊，真实意图与表层表达没有因果关系；
14. `AUTHOR_SPEAK`：角色突然说出明显属于作者总结、主题说明或观众解释的语言；
15. `OVERDRAMATIZATION`：简单功能性/互动性对白被无依据地强加重大冲突、潜台词或情绪高潮；
16. `LISTENER_MODEL_BREAK`：角色对“对方知道/怀疑什么”的判断与已建立信息明显矛盾，导致策略不成立；
17. `TURN_DECOUPLING`：连续多轮不响应上一轮行为，各自发表预写立场；
18. `DECEPTION_CONTINUITY_BREAK`：已建立的谎言、承诺、说法或否认在没有触发的情况下自行改变。

### Soft Failure / Penalty

`TAIL_DRIFT`：Scene Change / payoff 已完成后仍继续解释、总结、互相确认。通常定向压缩，不必整场重写。

---

# 11. Rewrite Router

只修导致失分的层，不默认整场推翻。

```text
KNOWLEDGE_FAIL     → 修 Information Boundary
VOICE_FAIL         → 修 Voice / Information Choice / Syntax
MOTIVATION_FAIL    → 回到 Wants
RESISTANCE_FAIL    → 回到 Resistance
TACTIC_FAIL        → 重做当前 Beat 的策略变化
SUBTEXT_FAIL       → 修 Surface / Intent 距离
EXPOSITION_FAIL    → 重新分配信息 + 动作化
RHYTHM_FAIL        → 压缩 / 打断 / 沉默 / 换拍
CONTINUITY_FAIL    → 回到 State / Ledger
SCENE_FAIL         → 回到 Scene Change / Beats
LOAD_FAIL          → 重判 FUNCTIONAL / INTERACTIVE / DRAMATIC
FUNCTION_FAIL      → 重新路由 Scene Function
LISTENER_FAIL      → 修 Perceived Knowledge / Belief About Other
TURN_FAIL          → 修 Response Mode / Adjacency
DECEPTION_FAIL     → 修 Claims / Lies / Promise Ledger
TAIL_FAIL          → 从 payoff 后开始压缩或直接截断
```

默认最多 3 轮定向重写；DEEP 且用户明确要求极致精修时最多 5 轮。

仍无法达到 90：判断是否 `UPSTREAM_CONFLICT`，不得靠继续润色掩盖结构问题。

---

# 12. Output Modes

## A｜纯台词

只输出直接可用对白。

## B｜影视剧本

`角色名 + 必要微动作 + 台词`。

## C｜台词诊断

`原台词 / 问题类型 / 修改 / 修改原因`。

## D｜完整设计

`Scene Change / Wants / Function / Beats / Final Dialogue / State Delta / Score`。

## E｜批量场景

每场仅保留：

`Scene Change / Function / Final Dialogue / Score / 必要警告`。

用户未指定：默认输出最终可用内容，不展示完整内部分析。

---

# 13. Integration Contract

从 Character Skill 接收：

`identity / stable_traits / behavior_logic / emotional_logic / relationship / speech_style / voiceprint`

从 Screenwriter Skill 接收：

`scene_goal / conflict / required_information / start_state / required_end_state / upstream_beats(optional)`

向 Director / Storyboard Skill 输出：

`final_dialogue / minimal_micro_actions / pause_or_interruption_cues / emotional_shift / relationship_delta / information_delta`

如果上游已经提供 Beats：优先保留，只在台词机制无法成立时最小修正并标记。

---

# 14. Safety Boundary

- 不为了戏剧性增加不必要的危险、露骨或不适合目标受众的细节；
- 未成年角色保持适龄，不进行性化处理；
- “人物真实”不能突破安全边界；
- 原剧情存在不安全部分时，保留可保留的戏剧目标，改用安全表达。

---

# 15. Execution Pseudocode

```text
function dialogue_core(input):
    mode = choose_mode(input)
    context = normalize_minimally(input)
    load_path = classify_dialogue_load_path(context)
    load_class = load_path.start

    enforce_character_truth(context)
    enforce_knowledge_boundary(context)

    if load_class == FUNCTIONAL:
        mode = FAST

    if mode == FAST:
        draft = local_rewrite_or_generate(context)
        return finalize(fast_gate(draft))

    craft = load("core-craft-rules.md")
    change = define_scene_change(context)
    wants = define_wants(context)
    resistance = define_resistance(context, wants)
    info = build_information_boundary(context)
    listener_model = build_minimum_listener_model(context, info)

    function = route_scene_function(context, change, wants, resistance, load_path)
    if function.primary:
        load(function.primary)
    if mode == DEEP and function.has_real_phase_transition:
        load(function.phase_2_primary)   # sequential only; never parallel
    if function.structural_modifier_is_essential:
        load(function.structural_modifier)

    beats = plan_minimum_beats(context, change, wants, resistance, info, listener_model, function)
    beats = enforce_turn_coupling(beats)
    draft = generate_from_beats(beats, context)
    draft = actor_pass(draft, context, craft)
    draft = director_pass(draft, context, craft)

    if mode == DEEP:
        load("dialogue-rubric.md")
        load("continuity-ledger.yaml") if serialized_context_exists
        draft = candidate_select_only_key_lines(draft)
        draft = dialogue_doctor(draft)
        draft = continuity_audit(draft)
        draft = exit_audit(draft)

    score = evaluate(draft)
    loops = 0
    while (score < 90 or has_hard_failure(draft)) and loops < rewrite_limit(mode):
        failure = diagnose_lowest_layer(draft)
        draft = targeted_rewrite(draft, failure)
        score = evaluate(draft)
        loops += 1

    if score < 90 or has_hard_failure(draft):
        mark_upstream_or_unresolved_issue()

    return finalize(draft)
```

---

# 16. STANDARD Light Gate

STANDARD 不必每次加载完整 100 分 Rubric，但必须过 10 项轻量门：

```text
G1 Character      主要说法符合人物？
G2 Knowledge      没有越权？
G3 Listener       涉及隐瞒/试探时，对“对方知道什么”的判断成立？
G4 Intent         关键句知道自己在做什么？
G5 Coupling       每轮在回应或有意不回应上一轮？
G6 Proportion     没有把简单交流过度戏剧化？
G7 Strategy       有阻力时策略会变化？
G8 Progress       该负荷等级需要的状态变化已发生？
G9 Speakability   能自然说出口？
G10 Exit/Economy  payoff 后及时收束，无明显说明书或冗尾？
```

任何一项 FAIL：先定向修复，再输出。

`FUNCTIONAL` 不因缺乏潜台词或冲突而扣分；只要求准确、角色化、自然、简洁。

---

# 17. Final Gate

输出前确认：

- [ ] 谁在说、为什么是他，成立；
- [ ] 角色知识边界没有泄漏；
- [ ] 需要时，角色对“对方知道/怀疑什么”的判断成立；
- [ ] 关键台词有行为目的；
- [ ] 每轮台词真实响应或有意规避上一轮 move；
- [ ] Dialogue Load 判断正确，没有过度设计；
- [ ] 需要阻力的场景存在真实阻力；
- [ ] 遭遇阻力后策略发生变化；
- [ ] 角色声音可区分；
- [ ] 重要情绪没有全部直说；
- [ ] 没有双方已知背景的大段复述；
- [ ] 没有机械重复画面；
- [ ] 结尾至少一项状态发生变化；
- [ ] payoff 后没有解释性尾巴；
- [ ] 谎言、承诺和公开说法保持连续；
- [ ] 台词可自然表演；
- [ ] 无 Hard Failure。

---

# 18. Final Principle

```text
CHARACTER TRUTH
× KNOWLEDGE
× LISTENER MODEL
× TURN COUPLING
× WANT
× RESISTANCE
× TACTIC
× INFORMATION
× SUBTEXT
× RHYTHM
× PERFORMANCE
× CHANGE
```

不要追求：

> 每句话都聪明、漂亮、像金句。

追求：

> **这个人物在此时此地，为了自己的目的，面对这个人和这层阻力，只会选择这样的说法。**
