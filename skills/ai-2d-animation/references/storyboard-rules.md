# Storyboard Rules V1.2

层级：Episode → Act → Scene → Beat → Shot Contract。

每个 Shot：Purpose / Story Info / Emotion / Acting / Action / Key Pose / Composition / Shot Size / Angle / Camera / Timing / Animation / Audio / Transition / Continuity / Acceptance Criteria。

## 分镜检查
- 每镜头一个主要任务
- 每个 Beat 至少有起始状态与变化
- 重要事件之后检查是否需要反应镜头
- 动作方向连续
- 视线连续
- 180°轴线有明确理由时才跨越
- 高潮前有建立，高潮后有结果
- 不用镜头炫技替代信息

## 故事层检查（story-craft.md）
- 前 3 镜内有关系线索镜头（relationship_hint）
- 情绪阶梯无跳级，每个跳级点有过渡节拍
- 每个 Beat 有动机来源（motivation）
- 身体接触晚于默许信号
- 15s 内信息点 ≤3、情绪级 ≤3
- 详细规则见 `references/story-craft.md`

## 原文落实检查（Coverage Gate）
每镜的 `Source` 必须指向剧本原文段落，且 `Coverage` 声明该段如何被落实：
- `covered`：一个剧本段落可以由多个镜头共同落实，但每个镜头只能有单一主任务。
- `intentional_repeat`：重复必须写明理由（表演节奏/强调），不允许无意识重复。
- `omitted_with_reason`：省略必须有理由（成本/节奏），不允许剧本内容凭空消失。
- `nonvisual_context`：仅供理解的内容不进镜头表。
- 对白、动作、画面文字、画外音或关键音效还没有着落时，不要先追求漂亮镜头。
- 一个剧本段落如果没有任何镜头落实（未 covered 也未合理省略），视为断链，QA Gate 1 不通过。

## 动漫演出检查（Anime Treatment Gate）
- 每个 Shot 已声明 `Anime Treatment` 类型（REALISTIC-ANIME / SYMBOLIC / LIMITED / SAKUGA / COMEDY-SD / MOE）
- 情绪是否有可见符号化表达（汗滴/青筋/速度线/豆豆眼/红晕/颜艺/SD化）而非只有形容词
- 有限动画约束是否明确（哪些在动、哪些静止）——对话/日常戏优先 LIMITED
- Sakuga 镜头是否只集中在 10-20% 的关键爆发位，且有"蓄力→爆发→结果"三帧结构
- 动漫视觉语言五要素（线稿/上色/阴影/高光/质感）是否在项目级锁定、镜头间未漂移
- 符号化夸张（SYMBOLIC/COMEDY-SD）与正剧写实（REALISTIC-ANIME）之间是否有节奏对比
- Level 2+ 暧昧场景是否用光影/构图/肢体替代符号化夸张（见 anime-grammar.md §8）
