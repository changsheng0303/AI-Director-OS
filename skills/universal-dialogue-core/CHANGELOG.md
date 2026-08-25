# Changelog

## v2.1.0

### Added

- U10 `Listener Model`：二阶认知 / perceived knowledge；
- U11 `Turn Coupling`：逐回合行为响应；
- U12 `Exit Discipline`：明确 payoff 与结束条件；
- Dynamic Dialogue Load Path；
- DEEP-only sequential Function Phase Transition；
- `response_mode`；
- conversational repair；
- claims / lies / denials / promises / unanswered questions ledger；
- Hard Failures：`LISTENER_MODEL_BREAK`、`TURN_DECOUPLING`、`DECEPTION_CONTINUITY_BREAK`；
- Soft Failure：`TAIL_DRIFT`；
- Acceptance T19–T26；
- 24-case adversarial benchmark；
- 8-case generation spot-check。

### Changed

- Rubric 从“信息边界”扩展到“信息边界 + 对他人知识状态的判断”；
- Scene Function 从永久 single-primary 升级为：STANDARD 单 Function；DEEP 最多一次顺序切换；
- Continuity Ledger 升级到 v2.1；
- Universal Template 增加 load path / listener model / exit / open loops；
- Light Gate 从 8 项升级为 10 项。

### Preserved

- Genre Adapter 继续保持 experimental、默认关闭；
- FUNCTIONAL 不强制潜台词/冲突；
- STANDARD 仍优先单 Function，避免 Token 膨胀；
- Scene Function 仍按行为机制而非题材路由。

## v2.0.0

- 建立 Universal Core / Scene Function / Genre optional / Project Character 四层架构；
- 引入 Dialogue Load；
- Genre 从默认链路降级；
- group_dialogue 改为 structural modifier。
