# Shot Adjacency & Anti-Jump Rules V1.5

## 核心问题
“分镜跳脱”通常不是单个镜头不好，而是相邻镜头之间没有桥。

## Adjacency Types
`CONTINUE / REACT / REVEAL / CUTAWAY / BRIDGE / CONTRAST / SCENE_BREAK / TIME_JUMP`

## 70/30 Continuity Rule
相邻镜头默认至少 70% 状态继承、最多 30% 关键变量变化。超过 3 个关键变量变化必须标记 `HARD_CHANGE`。

## Six Anchors
相邻镜头至少共享三个：
`character / space / direction / gaze / prop / lighting / action_phase`

## Spatial Bridge
以下任一情况必须提供桥：
- 室内 ↔ 室外
- 左 ↔ 右方向反转
- 门口 ↔ 房间另一侧
- 站立 ↔ 坐下
- 近景 ↔ 新空间
- 新角色突然出现

桥可以是：
`movement / gaze / sound / object / neutral shot / match cut / explicit scene break`

## Coverage Ladder
默认覆盖顺序：
`ORIENT → RELATION → ACTION → REACTION → CONSEQUENCE`

对话：
`ESTABLISH SPACE → TWO SHOT/OTS → SPEAKER → LISTENER REACTION → RESULT`

动作：
`GEOGRAPHY → PREPARATION → ACTION → IMPACT → RECOVERY/RESULT`

悬念：
`SPACE → CLUE → REACTION → WITHHOLD → REVEAL → RECONTEXTUALIZE`

不允许为了“丰富镜头”打乱上述逻辑，除非 Camera Logic 明确说明为什么。

## Shot-to-Shot Test
对每一对相邻镜头问：
1. 我知道角色在哪里吗？
2. 我知道他刚才做了什么吗？
3. 我知道他为什么现在做这件事吗？
4. 我知道画面方向有没有变化吗？
5. 我知道这个 Cut 带来了什么新信息吗？

任一连续两个问题无法回答：`ADJACENCY_RISK`。
