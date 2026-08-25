# Long-form continuity contract

用于 2 分钟以上、8 段以上或明确要求可连续剪辑的 H3 项目。目标是让每段既可独立生成，又能在时间线中与相邻段对接。

## 1. 编译顺序

`Script Canon → Narrative IR → Runtime Map → Scene Geography → Visual Asset Pack → Shot IR → Manifest → Audio Timeline → H3 files`

若上游任何一层变化，下游全部标记为 stale，按顺序重编。禁止只在 Prompt 中临时补剧情或改变人物状态。

## 2. Runtime Map

每场至少记录 `scene_id / source_script_range / timeline_start_sec / timeline_end_sec / dialogue_sec / action_sec / reaction_hold_sec`。场次相加得到目标时长，不得反向用固定条数证明时长。

`generation_duration_sec` 可大于时间线占用以保留剪辑余量；`timeline_end_sec - timeline_start_sec` 才计入成片总长。

## 3. Scene Geography

每场定义稳定的门、窗、桌、书架、道路、楼梯、主要光源、对话/运动轴线、屏幕方向、出入口、初始站位及天气/服装/损伤/道具不变量。

空间变化只能来自镜头内可观察调度，或明确的省略剪辑依据。

## 4. Shot Contract 规则

每段只保留一个主要动作和一个主要摄影机响应。字段：

- `narrative_intent`: 本段新增信息或情绪。
- `locked_state`: 不得漂移的人物、服装、环境、道具和风格。
- `start_state`: 第一帧精确可见状态。
- `trigger`: 启动动作的事件。
- `primary_motion`: 唯一主动作。
- `acting_reaction`: 眼神、脸、手、重心、呼吸的必要反应链。
- `camera_response`: 摄影机为何移动；无理由则静止。
- `secondary_motion`: 雨、衣摆、纸页等，从属于主动作。
- `end_state`: 最后一帧状态，直接连接下一段。
- `bridge_type`: `action_match / eyeline_match / sound_bridge / prop_match / composition_match / light_match / scene_transition / none`。
- `continuity_method`: `A_frame_linked / B_shared_reference / C_text_only`。

相邻段硬锁：人物位置/朝向、道具持有与状态、光线/天气、屏幕方向。若不相同，必须是镜头内变化或 `scene_transition`，并填写 `bridge_reason`。

## 5. Manifest schema

```json
{
  "project_id": "book-mountain-ep01",
  "target_runtime_sec": 1080,
  "timeline_tolerance_sec": 0.05,
  "max_generation_clip_sec": 15,
  "asset_pack_file": "visual_asset_pack.md",
  "asset_ledger_file": "asset_ledger.json",
  "asset_binding_file": "asset_binding.md",
  "asset_binding_json_file": "asset_binding.json",
  "audio_timeline_file": "audio_timeline.json",
  "segments": [
    {
      "segment_id": "EP01-S01-001",
      "order": 1,
      "scene_id": "S01",
      "source_script_range": "00:00-00:12",
      "timeline_start_sec": 0,
      "timeline_end_sec": 12,
      "generation_duration_sec": 15,
      "prompt_file": "prompts/EP01-S01-001.txt",
      "narrative_intent": "建立暴雨中的临江城",
      "continuity_method": "C_text_only",
      "bridge_type": "sound_bridge",
      "bridge_reason": "钟声提前进入下一段",
      "required_assets": ["AS-SCENE-01", "AS-STYLE-01"],
      "start_state": {
        "location": "临江城高空",
        "subjects": {},
        "props": {
          "AS-SCENE-01": {"holder": null, "zone": "CITY_WIDE", "state": "rain_night"}
        },
        "light": "午夜冷蓝雨光",
        "screen_direction": "camera_descends",
        "action_state": "暴雨持续"
      },
      "end_state": {
        "location": "临江城旧街上空",
        "subjects": {},
        "props": {
          "AS-SCENE-01": {"holder": null, "zone": "OLD_STREET", "state": "rain_night"}
        },
        "light": "午夜冷蓝雨光",
        "screen_direction": "camera_descends",
        "action_state": "钟声开始"
      }
    }
  ]
}
```

## 6. Reference strategy

- `A_frame_linked`: 上一段尾帧回灌为下一段首帧或 video continuation；用于连续动作、近景、道具交接和形变。
- `B_shared_reference`: 每段重复同一角色/场景/道具参考并完整写状态；用于稳定对话与中景。
- `C_text_only`: 只用于空镜、抽象蒙太奇或允许轻微差异的过场。

## 7. Adjacent review

每一对相邻片段检查：END→START、人物位置和朝向、道具手别、视线与轴线、光线天气、损伤服装、声音连续、剧情 New State→下一 Trigger。

通过 Manifest 检查只代表计划可连续；最终仍需选片、尾帧回灌、失败段重抽和剪辑 QA。

## 8. Structured state schema

正式生产不得把 `subjects` 或 `props` 写成自然语言整句。使用对象：

```json
"subjects": {
  "AS-CHAR-01": {
    "zone": "B_COUNTER_RIGHT",
    "facing": "screen_left",
    "pose": "kneeling",
    "action_phase": "left_hand_hovering_above_book"
  }
},
"props": {
  "AS-PROP-01": {
    "holder": "AS-CHAR-01:left_hand",
    "zone": "B_COUNTER_RIGHT",
    "state": "closed_dry"
  }
}
```

相邻 END/START 必须逐字段相等；位置、朝向、手别或状态改变必须在当前片段的动作中完成，或使用明确场景转场。

## 9. Audio timeline

正式长片提供 `audio_timeline.json`，每项至少包含：`audio_id / type(dialogue|voiceover|ambience|sfx|music) / timeline_start_sec / timeline_end_sec / speaker / exact_text / bridge_to_next`。对白文本必须与 SCRIPT_CANON 一致，且区间不得超出所属片段。
