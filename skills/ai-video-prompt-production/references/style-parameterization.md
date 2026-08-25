# 风格参数化（Style Parameterization）— 参考风格 → 可锁定视觉语言

用户说"设计一个XX风格的画面/提示词"时，不要写"很有XX感"这种形容词——把风格拆成**五要素 + 色彩系统 + 演出规则**，产出可锁定的 Image Prompt 模板与 H3 提示词。2026-08 实测于高饱和平涂、罗小黑清新治愈两例。

## 核心方法

1. **判断加减法**：先定风格是"加法"还是"减法"，决定参数走向。
   - 加法（高饱和撞色/厚涂/粒子堆砌）→ 纯色块、高对比、无颗粒。
   - 减法（清新留白/极简线条/水墨）→ 低饱和、柔和阴影、大量留白、有限动画。
2. **填五要素表**（每要素给英文 Prompt 写法）：
   - lineart：粗细/闭合度/手绘感
   - coloring：平涂/赛璐璐/厚涂/渐变
   - shading：层数/软硬/阴影色
   - highlight：形状/颜色/位置
   - texture：颗粒/纸感/平滑
3. **定色彩系统**：主色板 3-4 色 + 饱和度档位 + 光影习惯（硬顶光/柔光/逆光/光斑）。
4. **定角色与背景规则**：造型倾向（圆润 Q 版/锐利）、留白比例（≥1/3）、构图习惯、动效（有限动画声明"哪些动哪些静"）。
5. **写一句话锁定短语（英文）**：嵌入 prompt 开头，同项目所有镜头复用 → 防 STYLE_DRIFT。

## 保饱和度两个关键

- 阴影用**降低明度的同类色**（红→暗红），禁用纯黑/灰阴影——黑阴影瞬间降饱和。
- **颗粒/噪点会降饱和**：高饱和平涂必须无颗粒；清新手绘风可容忍轻微纸感。

## IP 角色原创化

模仿风格可以，**角色不直接搬 IP**：保留视觉锚点（配色/标志物/形态），换名字与细节。罗小黑例 = 原创"黑猫+金瞳+白尾尖+红铃铛"而非直接使用 IP 角色名；风格提示词可注明"对标 XX 的视觉语言"。

## 范例 A：高饱和平涂撞色（加法）

```
minimal clean closed lineart, flat cel coloring with pure color blocks no gradients,
high-saturation three-color clash (vermilion #E63946 x gold #FFC300 x teal #1D3557),
2-layer hard-edge shadows in darkened same-hue tones, pure white streak hair highlights
and star eye highlights, no grain, midday direct top light, decorative symbolic elements
```
- AVOID：厚涂/水彩/渐变/灰调/噪点颗粒/真人写实皮肤质感。
- 适用：国风/战斗/插画向角色展示。

## 范例 B：罗小黑清新治愈风（减法）

```
minimal clean rounded lineart with natural hand-drawn weight variation,
flat cel coloring with soft subtle gradients, low-saturation natural palette
of forest green and earth tones, soft low-contrast warm-gray shadows,
sparse round eye highlights, hand-painted ink-wash background with generous
negative space, gentle natural light with dappled shadows, cozy healing atmosphere
```
- AVOID：厚涂质感/高饱和撞色/粒子堆砌/极端透视/暗黑氛围。
- 适用：日常治愈/动物系/慢节奏短片；演出用 LIMITED 有限动画+局部微动。

## 产出模板

- Image Prompt 走 ai-2d-animation 的 image-prompt.md 结构（LEVEL/ANIME TREATMENT/LOCKED 五要素/SHOT STATE/SYMBOLIC EMOTION/VISUAL LANGUAGE/CONTINUITY/AVOID）。
- H3 视频版：五要素写入 detailed_description 开头 1-2 句 + LOCKED 复用，其余走六段式。
- 交付时给：参数化五要素表 + 一句话锁定短语 + 可粘贴提示词 + AVOID 清单。
