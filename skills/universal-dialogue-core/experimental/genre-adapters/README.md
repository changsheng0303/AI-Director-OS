# Genre Adapters

这些文件是 `dialogue-director` 的按需类型增强层。

规则：

1. 默认只加载一个主适配器。
2. 只有本场戏确实存在双重戏剧任务时才加载一个副适配器。
3. 类型规则永远不能覆盖 Character Fidelity、Knowledge Boundary、Continuity 和 Safety。
4. 适配器只修改台词策略、节拍、潜台词、节奏与 payoff，不重写上游剧情。
5. 场景结束后卸载，不把类型措辞强行延续到所有场景。
