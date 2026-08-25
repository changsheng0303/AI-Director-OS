# 动漫风格全景清单（选风格查此表，写进提示词风格前缀）

> 来源：ai-2d-animation skill 三大预设 + anime-grammar 五要素参数化 + 业界流派（2026-08 整理）。
> 用途：用户问"动漫有哪些风格/换风格"时直接列出；选定后把对应英文关键词替换进 `detailed_description` 风格前缀，其余段落不动，改完重跑校验 + 防雷词扫描。

## 一、内置三大预设（可直接锁定）

| 风格 | 一句话特征 | Prompt 锁定写法 |
|---|---|---|
| ① 日漫无线平涂（默认） | 去描边赛璐璐：日漫脸+大眼，纯色块，无黑线轮廓，发丝条状高光+星形眼瞳高光 | `lineless anime illustration, no outlines, flat cel coloring with solid color blocks, hard-edged cel shadows, streak hair highlights, star eye highlights, medium-high saturation` |
| ② 现代扁平插画 | 设计感/剪纸风：几何化造型，无描边，色块撞色，3-5 色限制 | `lineless flat illustration, solid flat color blocks with clean paper-cut edges, hard-edged block shadows, high-saturation 3-5 color palette` |
| ③ 罗小黑清新治愈 | 做减法：极简圆润线稿+低饱和自然色+水墨留白+有限动画，Q版弹性 | `minimal clean rounded lineart, low-saturation natural palette, soft warm-gray shadows, ink-wash background, generous negative space, cozy healing atmosphere` |

## 二、按上色/作画技法分（五要素：线稿×上色×阴影×高光×质感）

| 流派 | 线稿 | 上色 | 阴影 | 高光 | 代表 |
|---|---|---|---|---|---|
| 经典赛璐璐 | 细清线 | 平涂 | 硬边二分 | 发丝条状+星形眼高光 | 90s-10s 日漫动画 |
| 现代赛璐璐 | 细清线 | 平涂 | 2-3层硬边+局部软 | 高光丰富 | 鬼灭/咒术/JUMP系 |
| 无线平涂 | 无 | 色块 | 硬边 | 色块高光 | Pixiv 平涂插画 |
| 厚涂 Painterly | 无/弱 | 过渡涂抹 | 柔边渐变 | 少 | 插画立绘/游戏原画 |
| 水彩淡彩 | 弱线 | 透明晕染 | 柔和 | 水渍高光 | 治愈系插画 |
| 水墨风 | 笔触线 | 墨色渲染 | 浓淡 | 留白 | 罗小黑/国风动画 |
| 哑光柔光 | 细线 | 柔和高饱和 | 大块柔影 | 光晕感 | 新海诚系 |
| 粗犷手绘 | 粗抖线 | 平涂 | 随意硬边 | 少 | 扳机社/今石洋之 |

## 三、按制作公司/监督流派（业界风格锚点）

| 流派 | 核心特征 | AI 关键词 |
|---|---|---|
| 吉卜力风 | 手绘温暖、田园治愈、软线稿、水彩天空 | `soft hand-drawn lines, warm pastoral palette, watercolor sky` |
| 新海诚风 | 照片级背景+动漫角色、光晕丁达尔、高饱和云 | `hyper-detailed background, god rays, volumetric light` |
| 京阿尼风 | 萌系细腻、柔和光影、灵动发丝、精致日常 | `soft delicate shading, detailed hair strands, moe expressions` |
| ufotable风 | 特效粒子、摄影合成、光影华丽 | `dramatic particle effects, cinematic compositing` |
| 扳机社风 | 粗犷变形、夸张动作、美漫线条 | `bold rough lineart, exaggerated motion, impact frames` |
| SHAFT风 | 几何构图、极简背景、意识流 | `geometric composition, minimalist backgrounds` |
| MADHOUSE/细田守风 | 明亮色彩、日常奇幻、流畅表演 | `bright clean colors, fluid character acting` |

## 四、特殊形态

| 形态 | 说明 | Prompt 关键词 |
|---|---|---|
| Q版/SD | 2-3头身，搞笑/萌系 | `super-deformed chibi form, 2-3 head proportion` |
| SD化演出 | 正剧突然变Q版（喜剧节拍） | `sudden chibi deformation` |
| 剪纸贴纸风 | 扁平纸感边缘 | `paper-cut edge feel` |
| 有限动画 | 关键帧+停顿，动作克制 | `limited animation, keyframe holds` |

## 五、演出处理类型（anime_treatment，每镜必选）

- REALISTIC-ANIME：正剧/情感重场，写实表演+动漫造型，克制符号
- SYMBOLIC：喜剧/情绪爆发，颜艺/SD
- LIMITED：对话/对峙/日常，静态+局部动
- SAKUGA：战斗/高潮，高密度关键帧+冲击帧
- COMEDY-SD：搞笑桥段，Q版化+节奏停顿
- MOE：萌系日常，反应镜头+红晕+豆豆眼

## 六、实操注意

- 换风格 = 只替换 `detailed_description` 风格前缀，`subject_definitions`/`summary`/台词/镜头不动
- 用户说"无描边版" = ① 日漫无线平涂；若同时被 3D 渲染感困扰，叠加「反 3D 压制」前缀（见 SKILL.md 同章节）
- 参考图本身若带 3D 渲染感（体积光/AO/材质反射/景深/次表面散射），先换纯 2D 参考图再调提示词
