# Complex project intake

Use this reference before drafting a complex production project: a script over five minutes, multi-episode work, an existing IP or locked characters, or any project intended for storyboards, animation, AI video, H3, reference assets, or continuity-controlled production.

## Goal

Confirm decisions that materially affect the screenplay without interrogating the user. Extract all known facts from the conversation first. Ask only for missing groups, with a maximum of five groups in one message.

## Orchestrated project-starter mode

When `short-drama-system` invokes this skill as part of user step 1, this intake is internal rather than a separate user checkpoint:

- consume known facts and the Foundation draft/audit;
- infer noncritical blanks as explicit proposals;
- generate the project brief seed, Story Contract draft, and episode-count-independent architecture in the same pass;
- return them to the orchestrator for inclusion in one `PROJECT_STARTER_PACKAGE`;
- never ask the user to approve the brief, Foundation, Story Contract draft, and episode architecture separately.

Only the orchestrator may present a Decision Packet, and it does so once at the end of the starter package. Formal screenplay drafting and `SCRIPT_CANON` still require approval.

## Required decision groups

1. **Deliverable** — outline, standard screenplay, novelized screenplay, revision, or production handoff.
2. **Runtime and frame** — target duration, episode count if applicable, and horizontal/vertical orientation when visual production follows.
3. **Audience and tone** — genre, intensity, age/audience intent, and reference qualities expressed as high-level traits rather than imitation.
4. **Canon constraints** — characters, world rules, plot events, dialogue, visual elements, or exclusions that cannot change.
5. **Production path** — whether the approved script will feed storyboard, animation, H3, or another production stage.

Ask only for groups that remain unknown. If duration is already precise but the frame is not relevant to the requested deliverable, do not ask about frame.

## Confirmation message

Use this shape, filling known facts and asking only for blanks:

```text
我先不直接开写，避免后面剧本、分镜和视频版本互相打架。

目前已确认：
- 交付物：____
- 时长/集数：____
- 已锁定内容：____

还需要你确认：
1. ____
2. ____

如果你希望我决定，回复“你定”即可；我会先给一页项目简报供你确认。
```

Do not present a multiple-choice menu unless the user asks for options.

## PROJECT_BRIEF

When the user supplies the missing information or says “you decide”, produce this compact brief and wait for approval:

```text
PROJECT_BRIEF
项目名：
交付物：
目标时长/集数：
画幅：
受众与调性：
核心主题：
不可修改项：
允许补充项：
后续生产链：
```

`不可修改项` are parent canon. `允许补充项` are the only areas where the screenplay may make creative assumptions.

## Fast-start exception

If the user explicitly requests a fast-start draft, proceed without approval. Start with a visible `FAST-START ASSUMPTIONS` block and mark the result as provisional, not `SCRIPT_CANON`.

## Production freeze

After the user approves a screenplay for storyboard or AI-video production:

- issue `SCRIPT_CANON` with a stable version and source hash;
- identify canonical dialogue separately from optional performance notes;
- pass the canon downstream read-only;
- require an explicit change request before altering plot, dialogue, character state, or scene order.

## Examples

**Simple:** “Write a one-sentence logline about a ghost bookstore.” Proceed after stating any needed assumption.

**Complex:** “Make an 18-minute animation episode that later becomes H3 clips.” Confirm the deliverable, frame, audience/tone, locked canon, and production path before outlining.
