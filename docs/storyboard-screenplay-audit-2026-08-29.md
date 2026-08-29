# 分镜与剧本系统重构审计 · 2026-08-29

## 读取范围

本次在修改前完整读取了本地核心入口：

- 分镜：`storyboard-script-spec`、`director-mindset`、`ai-video-storyboard-compiler`、`ai-2d-animation`。
- 剧本：`screenplay-master`、`micro-drama-creation`、`anime-series-scripting`、`drama-script-iteration`、`screenwriter-review`、`universal-dialogue-core`。
- 总控与交接：`short-drama-system` 及现有 screenplay→storyboard 路由。

重点方法正文包括：旧版 2480 行 `full-ai-video-storyboard-method.md`、空间与轴线规范、视听转译、Shot Adjacency、Narrative Camera Logic、Director Method、Editing Rhythm、Shots Library、Coverage Audition、Screenplay Master 路由/格式/连续性/审稿资料。

GitHub 实际检索并读取：

- `Arch-Dog/video-prompt-engineer`：Skill、输入契约、叙事转译、镜头分组、动作因果和质量门。
- `AtlasCloudAI/awesome-seedance-2.5-prompts-skills`：通用视频 Prompt Skill、工作流、可验证末态和模型可移植性。
- `wyq030324-hub/StoryFlow-AI`：小说转剧本主链路和最小 YAML Scene Schema。
- `01011010/Multi-Agent-Studio-Pipeline`：多 Agent 评审与动态团队实验；因默认输出重、仍属 WIP，仅作反例/参考。
- `Aaryan-Kapoor/video-production-skill`：端到端视频生产 Skill 的任务边界和生产资产组织。

## 发现的结构问题

1. 四个 Skill 同时声称能输出分镜，镜号和时长权威冲突。
2. 旧分镜正文 2480 行，默认要求自检报告、两次前置询问、情绪锚点表、情境 ID、5–8 镜配额、每镜焦段/光圈/机位/构图/运镜、跨段十项卡，用户必须理解内部系统才能得到结果。
3. Shot 与 AI 生成 Clip 被混为同一粒度，导致过拆或硬塞。
4. 固定 3–4 秒平均镜长、固定 15 秒大分镜、固定 5–8 镜和实际对白/动作时长互相冲突。
5. 剧本工作被普通剧本、微短剧、18 分钟番剧、只加不改、红果审稿分割成多个入口，用户必须知道内部 Skill 名称和斜杠流程。
6. 大量项目实测偏好、成人内容、平台经验和通用剧作规则混在入口文件中，导致误触发和上下文污染。

## 重构决定

- `screenplay-master` 成为普通剧本创建、改编、改稿和审稿的统一入口。
- `ai-video-storyboard-compiler` 成为生产镜号、时长和镜头表的唯一入口。
- `director-mindset`、`storyboard-script-spec`、`drama-script-iteration`、`screenwriter-review` 改为显式专业视角。
- `ai-2d-animation` 仅在完整 2D 动画全流程时触发。
- Shot 与 Clip Group 分离；换引擎只重跑 Clip Group/Prompt 节点。
- 普通任务运行最小节点子图，不展示内部节点日志。
- 新增 Screenplay Graph、Storyboard Graph、验证器、正反例和自然语言触发回归用例。

## 借鉴而非照搬

从 GitHub 方案吸收：自然语言触发、音频账本、先锁固定资产、动作因果链、可观察末态、基础字段与扩展字段分离、P0/P1/P2 质量门。

没有照搬：固定 Seedance 时长、特定服务商、多人 Agent 报告堆叠、模型营销语、仓库尚未实现或声明为 WIP 的功能。
