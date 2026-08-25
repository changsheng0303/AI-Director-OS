# Ref2VA patterns and examples

## Contents

1. Appearance-only pictures
2. Video reference versus editing
3. Audio reuse versus reference
4. Complete compact example
5. Common repairs

## 1. Appearance-only pictures

User intent: picture 1 supplies the woman, picture 2 supplies the man. Neither picture is a literal frame of the target.

Correct:

```text
<Subject 1> is the young woman whose facial features, hairstyle, and overall visual appearance come from <Picture 1>.
<Subject 2> is the young man whose facial features, hairstyle, and overall visual appearance come from <Picture 2>.
```

Do not add independent lines such as `<Picture 1> is the reference image...`; the pictures are only subject sources. The summary type is `reference generation`, and retention contains subject lines but no picture lines.

If picture 1 is also the literal first frame of shot 1, add an independent definition:

```text
<Picture 1> is the exact first-frame and composition anchor for [Shot 1].
```

Now include `keyframe completion` and give `<Picture 1>` its own retention line.

## 2. Video reference versus editing

Motion/camera reference, source video remains untouched:

```text
<Subject 1> is the dancer whose appearance comes from <Picture 1> and whose spin timing references the performer in <Video 1>.
<Video 1> is the camera-path and cut-rhythm reference for [Shot 1] and [Shot 2].

summary:
[reference generation] The target video ...
```

Directly changing the original video:

```text
<Video 1> is the source video for the editing task.

summary:
[video editing] The target video is an edited version of <Video 1>. ...
```

Continuation from the original ending:

```text
<Video 1> is the source video whose final frame, motion state, and camera trajectory are continued by the target.

summary:
[video continuation] The target video continues from the ending of <Video 1>. ...
```

## 3. Audio reuse versus reference

Keep the original music signal under new dialogue:

```text
<Audio 1> is the synchronized soundtrack of <Video 1>, whose background music is reused beneath the new dialogue.
<Audio 1>: partially_copy - The source background-music layer is retained while new speech is added.
```

Borrow only a man's calm voice timbre:

```text
<Audio 2> is the voice-timbre and delivery reference for <Subject 1> (S1), without copying its original spoken content.
<Audio 2>: reference - The generated dialogue borrows the calm male timbre and measured delivery without copying the source signal or words.
```

## 4. Complete compact example

Input: two portrait pictures define a woman and a man. Generate an 8-second cinematic morning interaction with three shots. Dialogue must remain Chinese.

```text
subject_definitions:
<Subject 1> is the young woman whose facial features, hairstyle, and overall visual appearance come from <Picture 1>.
<Subject 2> is the young man whose facial features, hairstyle, and overall visual appearance come from <Picture 2>.

summary:
[reference generation] The target video portrays an intimate 8-second morning interaction in a modern apartment as <Subject 1> and <Subject 2> share coffee and quiet Chinese dialogue beside a sunlit balcony, progressing from a two-shot to alternating close-ups and a final shared frame.

retention_analysis:
<Subject 1> (appears in [Shot 1], [Shot 2], [Shot 3]): fully_preserved - Her facial structure, hairstyle, and recognizable visual identity from <Picture 1> remain consistent across all shots.
<Subject 2> (appears in [Shot 1], [Shot 2], [Shot 3]): fully_preserved - His facial structure, hairstyle, and recognizable visual identity from <Picture 2> remain consistent across all shots.

detailed_description:
The target uses realistic cinematic photography, warm golden morning light, restrained neutral colors, and shallow depth of field. Soft window highlights and natural skin texture keep the apartment intimate and believable.
[Shot 1] A medium two-shot frames <Subject 1> and <Subject 2> beside a floor-to-ceiling balcony window. <Subject 1> wears an oatmeal knit sweater with her hair loosely tied, while <Subject 2> wears a navy crewneck shirt and carries two steaming ceramic mugs. The camera slowly pushes in as he offers her one mug. <Subject 1> (S1) accepts it, glances toward the sunlight, then meets his eyes and says warmly, <d>[Chinese] 早啊，今天阳光真好。</d>
[Shot 2] At 00:02.700, the camera cuts to a close-up of <Subject 2> (S2). Steam crosses the foreground while he smiles and lightly covers her fingers around the mug handle. With a soft chuckle, he replies, <d>[Chinese] 是啊，等会儿想去哪里逛逛吗？</d> The camera remains nearly static, allowing only a subtle handheld drift and a small rack focus from their hands to his eyes.
[Shot 3] At 00:05.300, the shot cuts to a tight chest-up two-shot. <Subject 1> takes a small sip, leans against <Subject 2>'s arm, and whispers, <d>[Chinese] 哪儿都不去，就在家里陪你。</d> He lowers his forehead gently against hers. The camera makes a slow, small-amplitude arc to the right while both hold still in a relaxed smile through the final frame.

overall_soundscape:
Quiet apartment room tone blends with distant morning traffic, faint balcony air, ceramic contact, soft fabric movement, breathing, and subtle liquid motion inside the mugs.

non_diegetic_music:
A sparse felt-piano motif at a slow tempo is joined by lightly plucked acoustic guitar after [Shot 2], remaining low beneath the dialogue and resolving on one sustained chord at the end.
```

## 5. Common repairs

| Incorrect | Correct action |
|---|---|
| Define every uploaded image independently | Independently define only actual frame or composition anchors; cite appearance sources inside subjects |
| `[video editing]` for copied choreography | Change to `[reference generation]` and state the exact motion traits borrowed |
| `fully_copy` for voice cloning | Change to `reference`; timbre is a feature, not the original signal |
| Rewrite Chinese dialogue into smoother English | Restore the exact Chinese text inside `<d>[Chinese] ...</d>` |
| Start `[Shot 1] At 00:00.000` | Remove the timestamp from Shot 1 |
| Cut at `00:08.000` in an 8-second target | Move the final cut earlier; cut points must be inside the duration |
| Repeat dialogue in `overall_soundscape` | Keep complete speech only in `detailed_description` |
