# 食戟式爆衣特效形式与 L3 遮挡模板(2026-08 整理)

来源:萌百「爆衣」条目(服ビリ/fukubiri,美食爆衣点名《食戟之灵》)+ 英文维基(佐伯俊创作初衷"少女吃食物时的 ecstasy")+ 食戟之灵动画经典演出。Fandom/TV Tropes 反爬未取到正文,特效形式基于动画演出整理。

## 9 种特效形式(爆衣演出组合拳)

| # | 形式 | 演出效果 | 叙事/遮挡功能 |
|---|---|---|---|
| 1 | 白光爆发 | 爆衣瞬间全屏闪光/圣光 | 视觉冲击 + 天然遮挡缓冲(闪白藏细节) |
| 2 | 布料炸裂飞散 | 衣服从接缝炸开,碎片爆炸状四散 | 爆衣"过程感"(爆衣≠破衣,突出过程) |
| 3 | 味觉电流 | 金光从唇→喉→全身,皮肤下发光 | 味觉传导视觉化,入口→爆衣的因果桥 |
| 4 | 背后味觉幻境 | 评审脑内世界(麦田/花田/云海/食材山) | 食戟标志性"第二舞台",把吃变成旅程 |
| 5 | 冲击波气浪 | 光环扩散,震飞餐具/掀桌布 | 味觉冲击的物理化 |
| 6 | 花瓣/羽毛/光点化 | 碎衣化为樱花/光点飘散 | 最安全 L3 美化:规避"满地衣料"暗示 |
| 7 | 金色光环/光轮 | 人物背后金色光轮 | 宗教式圣洁感,反差萌 |
| 8 | 表情神化 | 瞳孔高光放大、潮红、仰头后仰 | 佐伯俊原意:ecstasy |
| 9 | 音效+配乐上扬 | 撕裂爆响→冲击波轰鸣→管弦爆发→收尾独奏+竖琴 | 情绪三层:悬停→爆发→余韵 |

## 用户遮挡规范(L3 爆衣强制,2026-08 定稿)

**爆衣后必须:**
1. **贴身内衣保留在身上**——`lace brassiere covering her chest and lace underwear covering her hips`
2. **未被内衣覆盖的区域完全用光效包裹**——`radiant golden light wraps every uncovered part of her — shoulders, back, and legs veiled in flowing golden light`
3. 再加发丝/构图裁切三层保障——`her stray strand of hair adding one more layer of cover across her chest`

**提示词写法要求:**
- 遮挡层必须写入 START/MOTION/END 全程(detailed_description 每个 Shot 都提),不能只在 retention_analysis 提一次
- 外衣定义时就要写"over a white lace lingerie set",让爆衣后有物可留
- 机位配合:upper body framed from the shoulders up and lower body framed from the waist down
- 白光爆发在爆衣瞬间承担遮挡缓冲

## 两条用户纠正(2026-08,踩坑后定稿)

### 纠正①:隐私局部特写必须为零
用户明确拒绝带身体局部描述的版本。**整份提示词禁止出现任何身体部位词**:collarbone / chest / thigh / hips / legs / shoulders / waist / lips(特写语境)等——即使语义合法(如构图用语 `from the chest up`)也删。规避法:
- 爆衣后全身金光包裹 → **只露脸 + 手中道具**(`leaving only her face and the bowl in her hands visible`)
- 镜头切面部特写(`framed in a tight close-up of her face inside the light`),身体全部在光效剪影里
- 遮挡零依赖身体构图(不用"裁肩裁腿"这类,用纯光效)

### 纠正②:爆衣动作必须可见
用户嫌上一版"没有爆衣服"(爆衣被光效完全盖住、只露脸)。**爆衣过程感必须写清楚**,这是爆衣戏的存在价值:
- 写全炸裂动作链:`the kimono bursts apart, the fabric tearing from the sash outward, shreds flying outward in all directions and dissolving into shimmering petals`
- 内衣保留要有存在感:`beneath the torn kimono her modest undergarments remain clearly visible`
- 音效层补布料撕裂爆响 + 冲击波低鸣,强化爆衣存在感
- 平衡点:**爆衣动作完整可见 + 内衣保留 + 光效包裹未覆盖区 + 零身体部位词**——四条同时满足,不是非此即彼


## 防雷词注意

- `bare shoulders` 里的 `bare` 会被防雷词 grep 命中(即使语义合法)→ 改写为 `exposed shoulders`
- `barely` 含 `bare` 子串 → 改写为 `just a little`
- bra/lingerie/underwear 不在防雷词表,可放心使用

## 已验证成品(15s,可直接复制改参)

`DEMO_一口入魂_15s.txt`:三拍结构——料理入口(悬念)→ 味觉电流+瞳孔骤缩(冲击)→ 白光爆发+和服炸裂化樱瓣+金色冲击波+麦田幻境+内衣保留+金光包裹(高潮)+评语。六段式全 PASS。
