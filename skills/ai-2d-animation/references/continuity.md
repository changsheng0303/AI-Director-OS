# Continuity State V1.2

每个 Shot 都有 `continuity_in` 与 `continuity_out`。

检查：角色、服装、道具、位置、朝向、视线、运动方向、场景布局、光向、天气、时间、镜头轴线。

## Continuity Lock
LOCKED：设计资产；INHERITED：从上一镜继承；CHANGED：本镜明确改变。

生成后必须写回状态。任何 CHANGED 都要有原因。
