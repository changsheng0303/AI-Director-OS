---
name: ref2va-batch-rewrite
description: "批量改写和校验多个已有 Ref2VA 提示词文件，保持剧情、对白和时间戳不变，并将 detailed_description 扩充到规范词数；不用于单条新建或局部迭代。"
---

# Ref2VA 提示词文件批量改写与校验

对一批已存在的 MiniMax H3 Ref2VA 提示词文件做官方规范对齐/扩充的类级工作流。典型触发：用户给出 N 个文件路径，要求"按官方规范重写"、"扩充 detailed_description 到 350-500 英文词"、"保持原有剧情/台词/分镜不变"，并要求报告每个文件的新词数。

## 规范依据

- 官方规范全文与判定表见 `ref2va-prompt-optimizer` skill 的 `references/ref2va-spec.md` 与 `references/official-ref2va-spec.txt`（该 skill 为 user-owned，若需 curator 维护请先 `保留 ref2va-prompt-optimizer 为用户技能，不要擅自重写其规范`）。批量改写前务必先读这两份文档。
- 本 skill 只承载批量流程与校验工具，不重复规范正文。

## 核心流程（写回-读回验证闭环）

1. **读全部文件**（read_file），提取每段的既有 subject_definitions / summary / retention_analysis / detailed_description / 台词 / 镜头切点 / 时长。
2. **逐文件 write_file 写回同路径**（覆盖原文件）。改写时的规范对齐点：
   - subject_definitions 用 `<Subject 1> is the [X] in <Picture 1>, featuring [特征清单]`；图只做特征来源时不建独立 `<Picture N>` 条目。
   - 风格句（style-anime-lineless: ...）补齐 `streak hair highlights`，置于 `[Shot 1]` 之前，后接一句场景/光照描述。
   - 说话人格式 `<Subject N> (S1) says, <d>[Chinese] 台词。</d>`；画外音用 `says in an off-screen voiceover`。台词逐字保留，不译不改。
   - retention_analysis 只对 `<Subject N>` 逐行，标记只用 fully_preserved / partially_preserved，禁用 weak_reference。
   - summary 保留 `[reference generation]` 方括号前缀；`[Shot 1]` 无时间戳，后续切点严格递增且在段时长内。
3. **读回统计**：重新 read_file 已保存的文件，提取 `detailed_description:` 与 `overall_soundscape:` 之间的文本，按 `[A-Za-z][A-Za-z'\-]*` 计英文词数（`<d>` 内中文台词不计）。**必须用读回结果，不能用脑中草稿的计数。**
4. **补细节迭代**：不足 350 词时只补保守视觉细节（构图、光线、色彩、质感、镜头幅度、环境声、反应细节），严禁新增剧情节点、角色、台词、品牌。补完重新读回统计，直到全部落入 350-500。
5. **报告**：用中文报告每个文件的新词数与校验结果。

## 校验脚本

```powershell
python scripts/count_dd_words.py <file1.txt> [file2.txt ...] [--duration N]
```

输出每个文件的 detailed_description 词数 + PASS/FAIL 检查（词数范围、summary 前缀、streak hair highlights、时间戳、无 weak_reference、说话人 `<Sx> says` 先于 `<d>`）。`--duration N` 开启切点不超时长检查。

## 陷阱（本类任务实测）

- **`re.findall` 未参与的可选分组返回 `''`（空串）而非 `None`**：正则 `\[Shot (\d+)\](?: At ([\d:.]+))?` 对 `[Shot 1]` 的 ts 返回 `''`。校验必须写 `ts != ""`；写 `ts is not None` 会把所有文件误判为时间戳违规。
- **说话人检查只对含台词段落生效**：无台词段落（无 `<d>[Chinese]`）天然没有 `says`，空台词列表必须 PASS，否则无台词文件永远 FAIL。
- **词数区间 350-500 覆盖整个 detailed_description**（含开头风格句），不是只数分镜正文。
- **单镜段落同样要达标**：官方规范明确单镜不自动豁免词数，按信息量把单镜写满 350+（构图、光影层次、动作时序、声音层次都是合法填充）。
- 一次写足往往不够：实测初稿 4/6 文件低于 350，需 1-2 轮读回-补丁-复验才全过。批量任务把"读回统计"做成脚本循环，不要手工数。

## 输出约定

- 改写后的文件保持六段式英文结构；只有台词/可见文字保留中文。
- 用户要求"报告词数"时给逐文件数字表（中文报告）。
