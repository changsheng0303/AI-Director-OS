# AI Director OS 分发包

版本：v1.0  
定位：可交给其他使用者安装的模块化 AI 影视导演 Skill。

## 它解决什么问题

AI Director OS 将创作任务拆成可验证的链路：

`输入分析 → 类型路由 → 冻结导演 Core → 类型模块 → Production 分镜 → 模型 Adapter → 生成 → 视频 QA → 失败记忆 → 回归验证`

它适用于：

- 动画、AI 2D 视频和连续分镜
- 剧本转导演分镜
- 已有视频的镜头逻辑诊断
- MiniMax H3 等视频模型的提示词编译
- 动作、荒诞喜剧及后续类型模块的质量评测

它不是单纯的提示词模板，也不会把所有类型规则混成一份长提示词。

## 包内结构

```text
AI_Director_OS_v1.0/
├─ README.md
├─ MANIFEST.yaml
├─ 安装说明.md
├─ skill/
│  └─ cinematic-ai-2d-director/
└─ workspace-template/
   └─ AI_Director_OS_CURRENT.md
```

## 能力状态

| 模块 | 状态 | 说明 |
|---|---|---|
| Director Core v3.1 | FROZEN | 通用导演决策底座 |
| Genre Router v0.1 | READY | 区分 Project Genre 与 Scene Mode |
| Comedy v1.0 | READY | 荒诞喜剧、节拍和视觉笑点 |
| Action v0.2 | EXPERIMENTAL | 已有规则 QA、静态分镜 QA 和单案例生成 QA，仍需 A/B 回归 |
| Emotion | NOT IMPLEMENTED | 暂不伪装成已完成模块 |
| Suspense | NOT IMPLEMENTED | 暂不伪装成已完成模块 |
| MiniMax H3 Adapter | EXPERIMENTAL | 可编译提示词，但生成结果仍需实际视频 QA |

## 安装

详见 [安装说明.md](安装说明.md)。最简单的方式是把 `skill/cinematic-ai-2d-director` 整个目录复制到使用者的 Codex Skills 目录，并把 `workspace-template/AI_Director_OS_CURRENT.md` 复制到项目工作区。

## 首次使用

让使用者直接输入：

> 使用 AI Director OS，分析这个项目的类型、场景模式和生产目标；先输出路由结果与缺失信息，再生成第一版可验证分镜。

对于正式生产，应要求输出：

- Scene Objective 与 Exit State
- Beat Chain
- Production Storyboard
- State Bible（包括 Relative Scale 和 Locked Features）
- 模型提示词
- PASS/FAIL、风险和返工目标

## 重要边界

- 只有用户确认或提供足够信息后，才进入正式生产；复杂项目先询问关键选项。
- Router 只负责选模块，不能替代导演设计。
- Adapter 只翻译已批准的 Production Schema，不能擅自新增剧情。
- 单个失败不能升级为 Core 规则。
- 没有实际生成视频时，不得声称通过 Generation QA。
- Action v0.2 仍是实验模块，不能作为稳定版能力宣传。

## 版本管理

使用者可以从 `AI_Director_OS_CURRENT.md` 查看当前状态、证据等级和下一步。每次升级应同时更新 MANIFEST、状态文件和 QA 证据，不要只改版本号。
