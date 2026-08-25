# Episode Workflow V1.2

1. Intake & Script Audit → `INTAKE`
2. Intent/Bible → `INTENT_LOCKED / BIBLE_LOCKED` → Human Gate A
3. Character / Costume / Prop / Scene Asset Lock
4. Episode Beat Sheet → `BEAT_LOCKED`
5. Scene Cards + Coverage Map
6. Shot Contracts → `SHOT_LOCKED` → Human Gate B
7. Key Pose / Motion Plan
8. Keyframe Generation → `ASSET_LOCKED`
9. Image QA
10. Prompt Compilation
11. Model Routing + Generation Budget → `ROUTE_READY`
12. Video Generation → `GENERATING`
13. Motion / Continuity QA
14. Repair failed shots only → `QA_REPAIR`
15. Hero/First-cut Human Gate C
16. Edit / Audio / Rhythm QA → `EDITING`
17. Final Director Review → `APPROVED / FINAL`

每一步都写入 Project State；失败只回退到最近一个仍然有效的状态。
