# Screenplay Node Graph

| Node type | 输入端口 | 输出端口 |
|---|---|---|
| `source.ingest` | `idea/source/draft`, `constraints` | `source_map`, `locked_facts` |
| `story.contract` | `source_map` | `story_contract` |
| `cast.function` | `story_contract`, `locked_facts` | `cast` |
| `scene.outline` | `story_contract`, `cast` | `scenes` |
| `dialogue.pass` | `scenes`, `cast`, `knowledge` | `dialogue_canon` |
| `screenplay.assemble` | `scenes`, `dialogue_canon?` | `screenplay` |
| `screenplay.review` | `screenplay`, `story_contract` | `issues`, `revised_screenplay` |
| `canon.freeze` | `revised_screenplay`, `user_approval` | `script_canon` |

节点只拥有自己的字段。`dialogue.pass` 不重排场次，`screenplay.review` 不静默改变用户锁定事实，`canon.freeze` 必须有用户确认。单场快速写作可运行：

```text
source.ingest → scene.outline → dialogue.pass → screenplay.assemble
```

小说改编或长项目运行完整图。一个节点被修改时，只使直接依赖它的下游失效。
