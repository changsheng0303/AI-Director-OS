# Experimental Layer

本目录不是 Universal Dialogue Core v2.0 的默认运行依赖。

`genre-adapters/` 来自 v1.1 的题材增强实验。保留它们是为了未来在 Core 和 Scene Function 稳定后做后置增强与 A/B 测试。

默认规则：

1. Core 未通过，不得加载 Genre 修饰问题；
2. Scene Function 未明确，不得靠 Genre 决定对话机制；
3. 一次最多加载一个 Genre Adapter；
4. Genre 只能改变偏好，不得改变角色事实、知识边界、核心目标或既定场景结果；
5. Genre 的效果单独评测，不计入 Core v2.0 评分。
