# Shot Repair Workflow V1.2

1. Compare output against Shot Contract
2. Assign Failure Code
3. Freeze passed variables
4. Trace failure to the smallest variable
5. Create `repair_delta`
6. Recompile only affected Prompt segment
7. Re-render smallest possible unit
8. Re-run relevant QA Gate
9. Compare old/new artifact
10. Promote only if acceptance criteria pass
11. Write version + reason + evidence

禁止“失败 → 全 Prompt 重写 → 全片重生成”。
