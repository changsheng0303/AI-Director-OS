# GitHub Director/Screenwriter Skill Benchmark V1.7

## 目的
本基准不是复制任何仓库的文本或风格，而是提取可迁移的工作流结构、质量门、状态管理和导演/编剧决策方法，用于优化本 Skill。

## 参考项目

| 项目 | 主要价值 | 吸收 | 不直接照搬 |
|---|---|---|---|
| RainLib/AI-Storyboard | Producer + Scriptwriter + Storyboard + Director + Animator，多阶段审批 | 分阶段 handoff、Director PASS/FAIL、9-beat→4-shot→motion | 固定 9 beat 不作为所有类型硬规则 |
| wuwangzhang1216/DirectorSKILL | Director's Book、blocking-first、shot-as-story-decision、QC repair | Blocking before framing、Audience Delta、失败码、修复阶梯 | 不复制具体导演作品镜头 |
| danjdewhurst/story-skills | Story Bible、characters、plot、continuity、questions/promises registry | Persistent canon、promise/payoff、plot registry、chapter/scene state | 文学项目结构不强行套到短视频 |
| JohnKeating1997/spark-video | premise→screenplay→storyboard→render→review、每 clip QA、可审计日志 | Per-clip QA、render/review DAG、prompt trace、项目可恢复性 | 不绑定单一供应商 CLI |
| kianaliang-dev/drama-director-skill | Scene Archetype Router、double-contrast cut、Seedance constraints | Scene Archetype Router、反差剪辑作为条件策略 | 不把“反差”变成万能剪辑 |
| aicontentskills/ai-video-storyboard-skill | Hook/build/payoff、shared theme layer、平台节奏 | Narrative arc layer、shared visual theme、platform cadence | 不用营销模板替代剧情 |
| Vincentwei1021/video-shotcraft | 大量 shot recipe cards、motion previews、生产模板 | Recipe Library + bounded examples + motion grammar | 不让 recipe card 直接决定剧情 |
| smixs/creative-director-skill | 方法论驱动创意、系统化评估 | Idea generation/evaluation separation、评分矩阵 | 不把广告奖项逻辑当成影视剧情标准 |
| AlterLab-IEU/AlterLab-FC-Skills | Cinema & Digital Media 多部门技能包 | Department separation、可组合专业 skill | 不增加不必要的 Agent 数量 |
| modelstudioai/skills / spark-video | 编排、screenwriter↔director、parallel render、per-clip QA | Scene-level writer/director review、并行任务与 QA | 不依赖其具体平台命令 |
| mantoufan/seedance-prompts-skill | idea→screenplay→AI-video-prompt、去 AI 味、资产提示词 | Prompt compiler 前置剧情锁、资产/镜头分离 | 不复制平台专属关键词 |

## V1.7 决策
### 必须吸收
1. **Blocking before Framing**：先确定人物如何在空间中行动，再决定景别与机位。
2. **Audience Delta**：每镜必须回答“观众现在比上一镜多知道什么”。
3. **Producer/Director gate**：创作 Agent 与审查 Agent 分离；Director 不在 QA 阶段重新写剧情。
4. **Persistent story state**：角色、道具、知识、未兑现承诺、伏笔和场景状态可追踪。
5. **Scene archetype routing**：不同场景先选择叙事机制，再选择镜头库。
6. **Per-clip QA + repair loop**：单个视频失败时先诊断 Contract，而不是无限重写 Prompt。
7. **Recipe library as bounded options**：镜头 recipe 只能提供可选语法，不得替代故事决策。
8. **Prompt compiler separation**：Prompt 层只翻译已锁定的 Story/Scene/Shot Contract。

### 明确拒绝
- 形容词堆叠式“电影感”。
- 用固定镜头数量保证剧情质量。
- 用固定结尾模板制造“电影感”。
- 先选导演风格再反推剧情。
- 用大量镜头覆盖来掩盖没有冲突的故事。

## SFNW 说明
截至本次公开 GitHub 检索，未能确认一个与本 Skill 明确对应、名称为“SFNW”的公开导演/编剧项目，因此本版本**不虚构 SFNW 的能力或内容**。
如果“SFNW”是用户已有的私有项目、附件或特定仓库简称，应在下一轮提供仓库 URL、ZIP 或准确仓库名后再做针对性融合。
