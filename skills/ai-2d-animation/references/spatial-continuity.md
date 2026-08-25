# Spatial Continuity V1.5

## Spatial Anchor
每个 Scene 至少锁定 3 个不可变空间锚点，例如：门、窗、桌、楼梯、球网、讲台。

## Position State
每镜记录：
`subject_screen_position / facing / gaze_target / movement_direction / prop_location`

## Re-establish Rule
连续 3 个以上近景后，如果下一动作依赖空间关系，必须重新建立空间。

## Axis Rule
默认 180° 轴线不变。跨轴线需要：
`neutral shot / movement-through-axis / explicit intentional axis break`。

## Lighting / Time
连续镜头不得无解释改变主光方向、天气、时间或环境状态。
