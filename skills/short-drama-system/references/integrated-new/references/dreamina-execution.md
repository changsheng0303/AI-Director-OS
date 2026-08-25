# Dreamina CLI 执行契约

## 1. 实时预检

即梦 CLI 会更新，任何生成前都重新运行：

```bash
dreamina version
dreamina -h
dreamina <chosen-subcommand> -h
dreamina user_credit
```

从所选子命令帮助中读回模型值、时长、画幅、分辨率、输入数量和权限限制。若登录失效，报告需要登录；除非用户明确要求，不主动 `logout`、`relogin` 或清除现有会话。

Seedance 2.0 必须传用户确认分支对应的精确模型值；本技能默认映射为 `seedance2.0`。Seedance 2.5 映射为 `seedance2.5`。实时帮助不支持该组合时停止，不静默换成 fast、VIP、mini 或其他模型。

## 2. 选择子命令

- 无参考资产：`text2video`。
- 只有一张主图：`image2video`。
- 明确首尾帧：`frames2video`。
- 人物、场景、道具、视频或声音混合参考：优先 `multimodal2video`。
- `multiframe2video` 只用于多帧过渡叙事；它不暴露模型选择时，不得用于必须锁定 2.0/2.5 的请求。

以每组所需参考职责选择最小命令，不为了“功能更多”堆入无关参考。输入文件全部使用已锁定资产的绝对路径，顺序与正式提示词槽位一致。

## 3. 生成计划

`07-即梦生成计划.json`是内部执行清单：

```json
{
  "schemaVersion": 1,
  "kind": "video",
  "project": "项目名",
  "modelFamily": "seedance2.0",
  "requests": [
    {
      "id": "G001",
      "command": "multimodal2video",
      "modelVersion": "seedance2.0",
      "duration": 15,
      "ratio": "16:9",
      "resolution": "720p",
      "prompt": "本组完整提示词",
      "referenceImages": ["/absolute/CHAR-001.png", "/absolute/SCENE-001.png"],
      "referenceVideos": [],
      "referenceAudio": [],
      "outputDir": "09-视频/G001"
    }
  ]
}
```

每组提示词复制自已锁定的正式 Markdown；修改任一文本或参考文件后重新生成计划和指纹。运行：

```bash
/usr/bin/python3 scripts/request_fingerprint.py /absolute/project/07-即梦生成计划.json
```

## 4. 视频付费确认门

提交前向用户展示：总任务数、逐组 ID、精确子命令、`modelVersion`、时长、画幅、分辨率、提示词 SHA-256、参考文件名/大小/SHA-256、输出目录、逐组指纹和总指纹。

只有用户明确回复“提交视频”或对这一批逐项确认后才执行。以下情况使授权失效：任务数、提示词、模型、子命令、时长、画幅、分辨率、参考文件内容或顺序发生变化。

## 5. 提交与恢复

直接以参数数组调用 `dreamina`，不要用 `eval`、`source` 或把提示词拼进可执行 shell 代码。提交输出需要同时满足：

- 存在非空 `submit_id`；
- `gen_status` 是 `querying` 或 `success`。

若 `gen_status=fail`，记录 `fail_reason` 并停止该组。若命令退出但输出无法解析，不要立刻重提；先检查 `list_task --limit`，用时间、类型和计划指纹恢复可能已创建的任务。

每次提交立即写入 `08-生成审计.json`，至少记录请求指纹、精确参数、提交时间、`submit_id`、当前状态和失败原因。恢复执行时读取该文件，已有 `submit_id` 的组只查询，不重提。

出现 `AigcComplianceConfirmationRequired` 时，说明需要用户先在 Dreamina Web 完成一次性确认；保留计划和指纹，确认后再提交同一请求。

## 6. 查询、下载和技术验收

对 `querying` 任务有界轮询：

```bash
dreamina query_result --submit_id=<id> --download_dir=/absolute/project/09-视频/G001
```

只有查询到 `success` 并下载到真实媒体文件才进入验收。使用 `ffprobe`读回：

- 视频编码、宽高、显示比例、帧率、时长；
- 是否有音频流、音频编码、采样率和声道；
- 文件可解码且时长与请求允许误差相符。

实际内容还需检查人物身份、画面结构、动作方向、连续性、口型/画外音、异常文字、水印、黑帧、冻结、严重闪烁和音画异常。容器元数据通过不等于内容通过。

## 7. 多组合片

所有组单独验收后，才按 `G001...GNNN` 顺序合成新文件。保留 Dreamina 原始下载文件，不覆盖。若编码参数一致可使用 concat；不一致时显式转码为统一规格。合片后再次 `ffprobe`，验证总时长、分辨率、帧率、视频/音频流和可播放性，并把命令与结果写入审计。
