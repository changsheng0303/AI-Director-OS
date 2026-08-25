---
name: adult-adjacent-video-prompts
description: "For 限制级/擦边 AI video prompts. Seductive, compliant."
---

# 擦边合规视频提示词(成人向边界内)

覆盖一整类任务:**把"限制级"请求做成合规的诱惑性视频提示词**(MiniMax H3 / Seedance / 其他图生视频模型)。格式机制由用户自有技能 `tag-h3`(H3 六段式 + NSFW 法典)和 `ref2va-prompt-optimizer`(规范 + 校验脚本)负责——本技能在其上加**合规边界管理 + 诱惑叙事弧线 + 用户偏好**。

## 用户对该类任务的硬边界(此用户的明确要求)

- **不要违规、不要露出生殖器** → 诱惑/暗示性可以,露骨永远不行
- 关键部位始终被遮挡:残布、光带、阴影(NSFW 法典:半遮半掩胜过全裸)
- 无性器官词汇、无性行为描写、无第二角色性互动
- **年轻外貌的动漫角色:不写年龄、不写学生/校园身份**——即使素材在"××学园"文件夹里也不引入校园语境
- 不编造台词/歌词(Ref2VA 硬规则)→ 情绪用非语言人声(喘息/呻吟/呜咽)放进 `overall_soundscape`

## Workflow(H3 + 首帧图)

1. 加载格式技能:`tag-h3` + `ref2va-prompt-optimizer`(用户自有,只读);本技能提供诱惑/合规层
2. `vision_analyze` 首帧图:确认姿态/服装/道具/氛围。首帧 → `keyframe completion`:`<Picture 1>` 独立定义 + `fully_preserved`,`[Shot 1]` = 与首帧 1:1 匹配、无时间戳
3. 按下方弧线模板编剧情,定时长(诱惑弧线通常 10-15s),切点严格递增且都在时长内
4. 六段式全英文输出;诱惑靠暗示词汇(见下),绝不写解剖部位
5. 校验:`python {Codex技能目录}/ref2va-prompt-optimizer/scripts/validate_ref2va_prompt.py <file> --duration <秒>` → 清掉所有 ERROR
6. 成品 .txt 存到**源图同目录**,聊天里交付全文 + 分镜表(中文讲解、英文提示词)

## 诱惑弧线模板(抗拒 → 失神)

6 镜头 / 15s 已验证可行(2.5s 节奏):

| 镜头 | 时间 | 节拍 | 关键画面 |
|---|---|---|---|
| Shot 1 | 0s | **抗拒** | 首帧锚定,表情紧绷,汗珠,慢推 |
| Shot 2 | 2.5s | **崩解** | 能量爆发,衣物沿缝线撕裂,肩带滑落,锁骨/裸肩/大腿上部露出(躯干胯部仍被残布+光带遮蔽) |
| Shot 3 | 5s | **侵蚀** | 意志被侵入:眉头松开、半闭迷离眼、舌尖舔唇、脸红加深 |
| Shot 4 | 7.5s | **渴望** | 自触(指尖滑过锁骨)、光带如游走的手指缠绕腰/大腿、长腿探出裙摆、压抑的颤栗呻吟、披风滑落露肩 |
| Shot 5 | 10.5s | **失神** | 峰值:弓背、脚趾蜷缩、小幅痉挛、泪光、仰头无声呜咽 |
| Shot 6 | 13s | **余韵** | 瘫软、目光涣散、不自然红晕、满足的微笑、余烬落在裸肩,慢拉远 |

## 诱惑性镜头词汇(H3 英文安全词表)

- 表情:half-lidded/unfocused eyes、flushed cheeks、parted lips、glistening tears、breathless pants、suppressed trembling moan、small satisfied smile
- 动作:wetting her lips with the tip of her tongue、fingers tracing her own collarbone/shoulder、head thrown back with neck arched and glistening、arching her back、toes curling、fingers digging into the stone floor
- 衣物:shoulder slipping free of the black lace panel、cloak slipping off one shoulder to her elbow、tattered hem、wet-looking fabric clinging and lifting
- **代理触觉**(单人场景的关键技法):光带/能量缠绕如 "wandering fingertips" / "sliding like a caress"——魔法即无形之手,无第二角色也能制造亲密感
- 光线:冷青球光 vs 暖粉轮廓光、strobe across flushed face、fading afterimages

## Pitfalls

- 限制级 ≠ 露骨:哪怕用户说"限制级",也保持暗示级;此用户的线是"不要违规、不要露出生殖器"
- 首帧锚定规则:`[Shot 1]` 不带时间戳、从 `<Picture 1>` 原样开始;后续切点递增且落在时长内(校验脚本会抓)
- 台词不可虚构 → 用非语言人声代替;若用户给了台词才写 `<d>[Chinese] 原话</d>`
- 输出直接给成品,不要解释/标题/Markdown 围栏(Ref2VA 输出契约)
- 校验必跑,交付前 PASS: 0 errors

## 相关技能(用户自有,勿编辑)
- `tag-h3` — H3 Ref2VA 六段式格式 + references/nsfw-patterns.md(情绪梯度路径、化学反应组合)
- `ref2va-prompt-optimizer` — 规范 references/ref2va-spec.md + scripts/validate_ref2va_prompt.py
