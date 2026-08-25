# Asset System

## Asset Registry
每个资产包含：ID、名称、类型、版本、来源、锁定字段、可变字段、参考文件、使用镜头。

## Asset Types
Character / Costume / Prop / Location / Background / FX / Color / Audio Motif。

## 锁定策略
角色脸型、发型、服装主色、关键配饰、标志性道具默认 LOCKED。镜头层只修改姿态、表情、动作等允许变量。

## 版本策略
`asset-name_v001` → 只在结构性修改时升级版本；镜头生成记录使用的版本号。
