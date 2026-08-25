# Shot Recipe Library V1.1

Recipe 是"镜头意图模板"，不是固定 Prompt。使用时必须填入项目角色、场景、动作、情绪、连续性，并按 anime-grammar.md §6 选定 Anime Treatment 演出类型。

命名：`family-01..09`。共 81 个基础 Recipe（9 类 × 9 条）。

## 类型 → 默认演出取向

| 类型 | 默认 Anime Treatment | 核心惯例 |
|---|---|---|
| acting | MOE / SYMBOLIC | 符号化情绪（红晕/汗滴/豆豆眼）、眼神高光、有限动画 |
| action | SAKUGA | 蓄力→爆发→冲击→回收、smear/冲击帧/速度线、Sakuga 占比 10-20% |
| cinematic | REALISTIC-ANIME | 克制符号、空气感背景、逆光轮廓、眼瞳高光 |
| comedy | COMEDY-SD | 预期→停顿→爆发、颜艺/SD化、吐槽位、重复梗 |
| fantasy-sci-fi | SAKUGA + SYMBOLIC | 能量可视化、Bank Shot 仪式镜头、中心对称爆发 |
| lifestyle | LIMITED + MOE | 有限动画主场、静物微动、生活噪音、治愈符号 |
| romance | MOE + REALISTIC-ANIME | 距离与微表情、光斑/花瓣/心跳、Level2+ 用光影构图 |
| sports | SAKUGA + LIMITED | 关键帧密度切换、得分白闪、轨迹线 |
| suspense | LIMITED + SYMBOLIC | 信息克制、阴影压眼、声音先入、屏息定格 |

每条 Recipe 的 `Anime Treatment` 为建议值，可按项目情绪与节奏调整（见 SKILL.md §5.7 与 references/anime-grammar.md §6）。
