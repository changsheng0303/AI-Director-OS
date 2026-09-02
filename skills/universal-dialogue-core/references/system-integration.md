# System integration contract

## Position in the pipeline

```text
PROJECT_BRIEF
→ Foundation / Character Bible
→ Screenplay Scene Contract
→ Universal Dialogue Core
→ DIALOGUE_CANON
→ SCRIPT_CANON freeze
→ Narrative IR / Shot IR
→ Audio Timeline / Subtitle / H3
```

对白Core不替代编剧：上游决定场景为什么存在、发生什么、必须到达什么结果；对白Core决定人物如何在这个场景中说、避、问、拒绝、误解和改变策略。

## Input handoff

```yaml
source:
  project_id:
  source_script_hash:
  screenplay_version:
  scene_id:
scene_contract:
  scene_goal:
  conflict:
  start_state:
  required_end_state:
  required_information: []
  forbidden_information: []
character_inputs:
  voiceprint_ids: []
  stable_traits: {}
  current_states: {}
  relationship_states: {}
continuity_inputs:
  knowledge: {}
  listener_models: {}
  active_lies: []
  promises: []
  open_questions: []
constraints:
  target_duration_sec:
  canonical_lines: []
  change_permissions: []
```

## DIALOGUE_CANON output

```yaml
dialogue_canon:
  dialogue_id:
  dialogue_version:
  source_script_hash:
  scene_id:
  locked: true
  lines:
    - line_id:
      speaker:
      exact_text:
      language: zh-CN
      timing_estimate_sec:
      interrupt_target: null
      logical_stress:
        - span:
          role: corrective_focus | contrast | rejected_alternative | negation | exclusivity | identity | quantity | time | location | reveal | commitment | threat | concealment_leak
          strength: light | moderate | strong
          contrast_with: null
          reason:
      delivery:
        pause_before_ms: 0
        pause_after_ms: 0
        rate:
        pitch:
        volume:
        visual_cue:
      delivery_cue:
      optional_micro_action:
  scene_change:
  information_delta: []
  emotional_delta: {}
  relationship_delta: {}
  continuity_updates:
    claims: []
    lies: []
    promises: []
    open_questions: []
  unresolved_warnings: []
```

`exact_text`是唯一台词文本真源；`logical_stress`是句意焦点真源。`delivery`、表演提示和微动作是可替换的实现层，不得被误认为固定台词，也不得反向改变重音词或对比关系。

## Change control

下游发现时长、口型或镜头问题时，不得直接改台词。提交Dialogue Change Request：

```yaml
change_id:
affected_line_ids: []
reason: duration | lip_sync | clarity | censorship | performance
proposed_text: []
story_impact:
continuity_impact:
approval_status: proposed | approved | rejected
```

批准后生成新 `dialogue_version`，旧版保留可追溯。

## Downstream rules

- Storyboard：保留exact_text与logical_stress；只安排停顿、打断、反应和可选微动作，不重新判断重音。
- Audio Timeline：使用line_id、speaker、exact_text和时长估算。
- Subtitle：可分行，不改字；翻译另存translation track。
- H3：将exact_text原样放入官方允许的 `<d>[Language] ...</d>`；把重音转换为该引擎支持的自然语言表演说明，不得塞入不受支持的SSML。
- Voice/TTS：声线和表演参数来自Voiceprint；目标支持SSML时可把logical_stress编译为emphasis、break与prosody，但不能反向改变人物事实或exact_text。

## Invalidation

上游场景目标、结局、知识边界、人物关系或固定台词变化时，相关 `DIALOGUE_CANON` 标记stale并重编。仅镜头角度或画风变化不使对白失效。
