# Agent Handoff Protocol V1.2

Agent 不通过“继续做”传递任务，而通过结构化 Handoff Package。

## Required
`handoff_id / project_id / from / to / state / input_artifacts / locked_constraints / required_output / validation / version / priority`

## Optional
`open_questions / warnings / repair_delta / dependencies`

## Rules
1. 接收 Agent 只能修改自己职责范围内的字段。
2. Locked constraints 默认不可改。
3. 未决问题不得伪装成已确认事实。
4. 输出必须声明 artifact version。
5. QA FAIL 时必须附 Failure Code 与 Evidence。
6. Handoff 可追溯到上一版本。

## Example
```yaml
handoff_id: H012
project_id: P001
from: storyboard-artist
to: prompt-engineer
state: SHOT_LOCKED
input_artifacts: [shot_012@v003, char_A@v002]
locked_constraints:
  - character_A appearance
  - camera axis
  - rightward screen direction
required_output:
  - image_prompt
  - video_prompt
validation:
  - shot schema valid
  - continuity_in/out present
version: v003
priority: HIGH
```
