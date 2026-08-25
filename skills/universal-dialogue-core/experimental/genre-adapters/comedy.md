# Comedy Dialogue Adapter v1.0

## Mission

让笑点来自**人物目标、信息差和节奏**，而不是让角色突然变成段子手。

## Preferred Tactics

- misunderstanding：双方对同一信息拥有不同解释；
- wrong_focus：在大问题里认真关注一个荒谬小点；
- deadpan：角色保持认真，情境本身产生反差；
- escalation：同一策略连续升级但不能重复同一句式；
- reversal：预期回应被人物性格反转；
- callback：后文重新利用前文微小信息；
- status_flip：一句话改变场内谁占上风；
- delayed_reaction：反应晚半拍形成节奏差。

## Beat Bias

常用：

`Setup → Expectation → Misdirection → Reaction`

或：

`Normal → Tiny Error → Escalation → Callback Payoff`

不要每一拍都追求笑点。至少保留一个“正常拍”作为反差基线。

## Rhythm Rules

- 包袱前减少解释；
- punchline 后优先留反应，不立即补解释；
- 需要时使用短句、抢话、错误纠正；
- 一次笑点尽量只保留一个核心认知差；
- 同类笑法连续出现 3 次以上时必须变化机制。

## Subtext Rules

喜剧角色依然有真实目标。笑点不能抹掉：

- 自尊；
- 嫉妒；
- 紧张；
- 掩饰；
- 竞争；
- 亲密关系。

优先“角色认真完成自己的目标，结果自然好笑”。

## Anti-Patterns

- 角色主动解释笑点；
- 所有人都连续抖机灵；
- 为了笑点突然降低角色智力；
- 随机大喊、摔倒、重复词代替真正节奏；
- 把网络梗当人物口吻；
- punchline 后再补一句同义解释。

## Payoff Rule

至少一种成立：

- expectation broken；
- information gap exposed；
- callback completed；
- status flipped；
- character flaw revealed。

## Extra Checks

- 笑点移除后人物目标是否仍成立？若否，说明角色只是笑话工具。
- 换成另一个角色说是否一样好笑？若是，优先判 `VOICE_FAIL`。
- 是否为了“更搞笑”破坏前后连续性？
