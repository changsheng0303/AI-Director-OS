# AI Director OS

面向 Codex 的 AI 影视、动画与短剧制作 Skill 系统。

本仓库将创作方法与生产校验分开：用户通过简洁导演流程工作，内部按需调用剧本、角色、对白、场景资产、分镜和视频模型适配 Skill。

## 当前包含

- `skills/`：当前系统的 38 个自有/项目 Skill；
- `skills/short-drama-system/`：简洁导演入口、Canon-lite、Story Map、Shot 表和基础确定性校验；
- `docs/AI_Director_OS_v1.0_release/`：AI Director OS 分发说明、Manifest 与工作区模板；
- 各 Skill 自带的 references、schemas、scripts、examples 和本地校验工具。

完整系统架构、剧本审稿路由和38个Skills说明见：[AI Director OS 整体系统与 Skills 说明](docs/AI-Director-OS-系统与Skills说明.md)。

## 推荐入口

普通项目从 `short-drama-system` 开始。它支持：

```text
项目与剧本 → 审稿定稿 → 导演分镜 → 视觉资产与故事板 → 视频提示词与生成 → 成片交付
```

默认使用轻量 Canon、Story Map、Shot 表和基础校验；只有明确要求严格工程模式时，才启用完整 IR、Hash 或更重的交接结构。

小说改编模式还支持可选的原文证据、节拍认领、生成段 ID、资产锚点、状态和变体校验。

## 安装

将需要的 Skill 目录复制到 Codex Skills 目录，例如：

```text
<codex-skills>/short-drama-system/
<codex-skills>/screenplay-master/
<codex-skills>/ai-video-storyboard-compiler/
```

不建议把全部 Skill 一次性启用；同类入口可能造成自动路由竞争。H3 格式继续以官方 `h3-prompt-writing` 为权威，Seedance 与 Fafajing 使用各自 Adapter。

## 许可证与来源

这是一个混合许可证仓库，不存在一个覆盖所有目录的统一开源许可证。请先阅读根目录 `LICENSE.md`、`NOTICE.md` 和每个 Skill 的 frontmatter、LICENSE 或 README，再决定复制、修改或再分发。

公开仓库不包含用户项目、聊天附件、备份、缓存、生成素材或凭据。
