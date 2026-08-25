# MiniMax H3 Ref2VA local operational overlay

Official format authority is the installed read-only `h3-prompt-writing` skill, especially `references/ref-en.txt`. This file is a local implementation guide for conservative completion and validation. It must not override official field names, section order, labels, timing notation, task types, or examples. On conflict, follow the official skill.

## Contents

1. Input limits and numbering
2. Asset semantics
3. Fixed output structure
4. Section requirements
5. Timeline, camera, dialogue, and sound
6. Conservative completion rules
7. Final checklist

## 1. Input limits and numbering

- Accept at most 9 pictures.
- Accept at most 3 videos, each 2–15 seconds, with no more than 15 seconds total video duration.
- Accept at most 3 audio clips, each 2–15 seconds, with no more than 15 seconds total audio duration.
- Do not accept audio as the only reference input; require at least one picture or video.
- Accept no more than 12 mixed media files in total.
- If the input violates a limit or a media file cannot be inspected enough to determine its role, do not fabricate. Return one concise Chinese correction request.
- Number each category independently in attachment order. `<Picture 1>`, `<Video 1>`, and `<Audio 1>` can all exist and refer to different files.
- Keep every assigned tag semantically stable throughout the prompt.
- Use a duration supplied by the user or calling environment. Otherwise default to 5.00 seconds.

## 2. Asset semantics

### Subjects

`<Subject N>` is a visible content unit reused or transformed in the target: a person, animal, object, scene, background, wardrobe, prop, interface, effect, visual style, action, expression, or pose. It is not a source file.

- A subject may combine attributes from multiple assets. State the contribution of each asset.
- One asset may define multiple independently tracked subjects.
- Create only subjects that appear in the target video.
- Example: `<Subject 1> is the woman whose facial appearance comes from <Picture 1> and whose walking motion comes from <Video 1>.`

### Pictures

If a picture only provides appearance, environment, wardrobe, object identity, or style, cite it inside the relevant subject definition. Do not give it its own definition or retention line.

Define `<Picture N>` independently only when the image itself is an actual first frame, keyframe, last frame, editing keyframe, composition anchor, or storyboard reference. State the shot and its exact role.

### Videos

Use `<Video N>` for a whole-video relationship: source-video editing, continuation, or reference to camera path, cuts, rhythm, or temporal structure. Define people, objects, settings, actions, and effects inside the video as subjects when they must be tracked.

- A video used only as action or camera reference remains `reference generation`.
- `video editing` means the target is a modified version of the source video.
- `video continuation` means new content begins from or extends the source video's ending.
- A video's synchronized audio does not automatically create `<Audio N>`. Define it only if that track is enabled and actually reused or referenced.

### Audio

Use `<Audio N>` for an independent audio file or an explicitly enabled video soundtrack. State whether the target copies the signal or references characteristics such as music style, voice timbre, delivery, language content, sound texture, beat, or continuity.

When audio corresponds to a target speaker, reuse the speaker's global ID: `<Audio 1> is the voice-timbre reference for <Subject 1> (S1).` Speaker IDs come from first actual vocal occurrence in the target, not from asset order.

### Relationship decision table

| Actual use | Summary task type | Retention relationship |
|---|---|---|
| Picture is a real frame anchor | `keyframe completion` | Picture gets its own visual retention line |
| Assets guide identity, style, action, camera, or cuts | `reference generation` | Track subjects and any independently defined whole-video reference |
| Existing video is directly modified | `video editing` | Track the source video and modified subjects |
| New video extends an existing video's end | `video continuation` | Track source continuity and new content |
| Same audio waveform is kept in whole or part | `audio reuse` | `fully_copy` or `partially_copy` |
| Only audio characteristics or content are borrowed | `audio reference` | `reference` or `weak_reference` |

Combine actual task types in the summary prefix with ` + `, without duplicates.

## 3. Fixed output structure

Successful output contains exactly six English sections in this order:

```text
subject_definitions:
...

summary:
...

retention_analysis:
...

detailed_description:
...

overall_soundscape:
...

non_diegetic_music:
...
```

Only dialogue, lyrics, and actual visible text may remain in their source language. Do not add a title, analysis, translation, parameters, negative prompt, or Markdown fence.

## 4. Section requirements

### `subject_definitions`

Define only labels used later. Write one clear line per independently tracked label.

- `<Subject N>`: identify the content unit and what each reference supplies.
- `<Picture N>`: define only a real frame/composition/storyboard role and name its shot.
- `<Video N>`: define the whole-video relationship.
- `<Audio N>`: define copy versus reference and its exact audible role.

### `summary`

Write one concise paragraph covering the target event, main subjects, shot flow, and reference relationships. Begin with a bracketed prefix made only from:

- `keyframe completion`
- `reference generation`
- `video editing`
- `video continuation`
- `audio reuse`
- `audio reference`

For video editing, the sentence after the prefix must begin: `The target video is an edited version of <Video 1>.`

Do not introduce any label that is absent from `subject_definitions`.

### `retention_analysis`

Give exactly one line for every independently defined label. A picture or video mentioned only as a source inside a subject definition does not receive a separate line.

Allowed visual markers for subjects, pictures, and videos:

- `fully_preserved`: every feature inside the label's defined scope is retained.
- `partially_preserved`: the reference remains recognizable but defined features change or only partly appear.
- `attribute_transfer`: defined attributes move to another recognizable target subject.
- `weak_reference`: only broad style, category, composition, or atmosphere remains.

Allowed audio markers:

- `fully_copy`: the entire source signal becomes the complete final soundtrack 1:1.
- `partially_copy`: only a time range or layer is copied, or the copied signal is mixed or altered.
- `reference`: no signal is copied; concrete traits are borrowed.
- `weak_reference`: only a broad category or atmosphere is similar.

Use: `<Subject 1> (appears in [Shot 1], [Shot 3]): fully_preserved - ...`

New actions, story beats, and background details do not automatically reduce reference preservation. The marker must match the role declared in `subject_definitions`.

### `detailed_description`

Start with 1–2 English sentences defining the overall visual style, light, and color. Then describe the complete playable timeline.

For each shot, cover composition, visible subject appearance and position, environment, light, action and state change, camera behavior, current sound, and where reference content becomes effective.

- Pure generation usually needs 350–500 English words, but prioritize exact timing and complete dialogue over word count.
- Introduce important reference traits when a subject first appears; do not redefine the subject every shot.
- Write frame relations naturally: `the shot begins from <Picture 1>`, `the shot's keyframe corresponds to <Picture 2>`, or `the shot ends on <Picture 3>`.
- Mention video and audio tags where their declared relationship actually takes effect.

### `overall_soundscape`

Write one English paragraph for ambient sound, physical action sounds, and nonverbal vocal sounds. Do not repeat dialogue or lyrics. State any copied or referenced environmental/audio effect relationship. Use `N/A` only for explicitly absolute silence.

### `non_diegetic_music`

Describe audience-only score with instrumentation, tempo, rhythm, and dynamic change. State audio reuse or reference precisely. Music audible to characters belongs in `detailed_description`. Use `N/A` when there is no non-diegetic score.

## 5. Timeline, camera, dialogue, and sound

### Shots and timestamps

- `[Shot 1]` has no timestamp.
- Each later shot uses a strictly increasing cut point inside the target duration: `[Shot 2] At 00:03.000, the camera cuts to...`
- Use ordinary cuts or natural transitions unless the user explicitly requests a dissolve, fade, or wipe.
- Every cut must introduce a meaningful change in subject, space, state, angle, or time. Use continuous movement for minor framing changes.

### Camera

Integrate camera language into prose. State movement type and, where useful, amplitude and speed. Supported patterns include Zoom In/Out, Push In/Pull Out, Pan Left/Right, Truck Left/Right, Tilt Up/Down, Pedestal Up/Down, Arc Shot, Tracking Shot, Static Shot, Shake Slightly/Strongly, POV, and Roll Clockwise/Counterclockwise.

### Speakers, dialogue, lyrics, and visible text

- Assign `(S1)`, `(S2)`, and later IDs by first real vocal event in the target.
- Combine visible subject and speaker ID when a referenced subject speaks: `<Subject 2> (S1)`.
- Use a stable voice description plus ID for a speaker without a subject.
- Keep identity, ID, action, and delivery outside `<d>`. Put only language label and exact utterance inside: `<d>[Chinese] 原话</d>`.
- Preserve user-provided dialogue, lyrics, punctuation, and visible text verbatim. Do not translate or polish them.
- Write `[unclear]` for unintelligible source speech; never guess.
- Referencing timbre or delivery does not authorize copying source dialogue.
- Reused background audio does not create a speaker ID. Assign IDs only to actual character, narrator, or singer events.
- For voiceover, state `says in an off-screen voiceover` and clarify that visible lips remain closed.
- Use `<scenetrans>` when dialogue continues across a cut and `<cutoff>` only for an intentional end truncation.
- Enclose visible on-screen text in English double quotes while preserving its original content.

## 6. Conservative completion rules

Internally extract the user's fixed intent: event, relationship, preserved and changed content, ending beat, dialogue, audio use, camera, and style.

Fill only noncritical gaps: physical transitions, small environmental motion, reaction details, camera continuity, ambient sound, and score. Keep a short video centered on one clear event.

Do not add unrequested characters, brands, dialogue, lyrics, on-screen text, major twists, or asset relationships.

Resolve conflicts in this order:

1. Explicit user instruction
2. Concrete keyframe or source-video structure
3. Subject identity consistency
4. Style and atmosphere

If all requirements cannot coexist, downgrade the affected relationship honestly in `retention_analysis`.

## 7. Final checklist

- Exactly six sections appear in the required order and use English prose.
- Every tracked label is defined before use and retains one meaning.
- A picture source is not mistaken for a frame anchor.
- A video reference is not mistaken for editing or continuation.
- Audio characteristic reference is not mistaken for signal reuse.
- The summary prefix contains every and only actual task type.
- Every independently defined label has exactly one compatible retention line.
- The timeline is shootable, timestamps increase, and every cut lies inside target duration.
- Speaker IDs follow first vocal occurrence and remain stable.
- Explicit dialogue, lyrics, and visible text are unchanged.
- Ambient sound and non-diegetic music are correctly separated.
- No analysis, extra explanation, parameters, negative prompt, or Markdown fence surrounds a submission-ready result.
